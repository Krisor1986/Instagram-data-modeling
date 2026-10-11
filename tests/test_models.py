"""Validate model relationships and constraints against a real SQLite database."""
import sys
import unittest
from pathlib import Path

from flask import Flask
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from models import Comment, Follower, Media, Post, User, db


class ModelTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db.init_app(app)
        self.context = app.app_context()
        self.context.push()
        db.session.execute(text("PRAGMA foreign_keys=ON"))
        db.create_all()
        self.alice = User(username="alice", email="alice@example.com", password="sample-hash")
        self.bob = User(username="bob", email="bob@example.com", password="sample-hash")
        db.session.add_all([self.alice, self.bob])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def rejected(self, instance):
        db.session.add(instance)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_relationships(self):
        post = Post(author=self.alice, caption="First post")
        media = Media(post=post, media_type="image", url="https://example.com/photo.jpg")
        comment = Comment(post=post, author=self.bob, comment_text="Great photo")
        follow = Follower(follower=self.bob, followed=self.alice)
        db.session.add_all([post, media, comment, follow])
        db.session.commit()
        self.assertEqual(self.alice.posts, [post])
        self.assertEqual(post.media, [media])
        self.assertEqual(post.comments, [comment])
        self.assertEqual(self.bob.comments, [comment])
        self.assertEqual(self.bob.following, [follow])
        self.assertEqual(self.alice.followers, [follow])

    def test_unique_username_and_email(self):
        self.rejected(User(username="alice", email="new@example.com", password="hash"))
        self.rejected(User(username="new", email="alice@example.com", password="hash"))

    def test_follow_constraints(self):
        self.rejected(Follower(user_from_id=self.alice.id, user_to_id=self.alice.id))
        db.session.add(Follower(user_from_id=self.bob.id, user_to_id=self.alice.id))
        db.session.commit()
        self.rejected(Follower(user_from_id=self.bob.id, user_to_id=self.alice.id))

    def test_missing_author_is_rejected(self):
        self.rejected(Post(user_id=999, caption="Invalid author"))

    def test_media_type_constraint(self):
        post = Post(author=self.alice)
        db.session.add(post)
        db.session.commit()
        self.rejected(Media(post_id=post.id, media_type="audio", url="https://example.com/file"))

    def test_post_deletion_removes_media_and_comments(self):
        post = Post(author=self.alice)
        db.session.add_all([post, Media(post=post, media_type="video", url="https://example.com/video"),
                            Comment(post=post, author=self.bob, comment_text="Nice")])
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        self.assertEqual(db.session.query(Media).count(), 0)
        self.assertEqual(db.session.query(Comment).count(), 0)
        self.assertEqual(db.session.query(User).count(), 2)

    def test_password_is_not_serialized(self):
        self.assertNotIn("password", self.alice.serialize())


if __name__ == "__main__":
    unittest.main()
