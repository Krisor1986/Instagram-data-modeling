# Modelagem de dados do Instagram

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Exercício de modelagem com SQLAlchemy da 4Geeks Academy. A entrega inclui cinco modelos relacionados e um diagrama entidade-relacionamento; não exige implementar frontend nem API.

## Modelos

| Modelo | Finalidade |
| --- | --- |
| User | Nome de usuário e e-mail únicos, perfil, senha e estado ativo |
| Post | Legenda da publicação, data de criação e autor |
| Media | URL de imagem ou vídeo pertencente a uma publicação |
| Comment | Texto do comentário, autor e publicação |
| Follower | Relação direcionada entre dois usuários |

Um usuário tem várias publicações e comentários. Uma publicação tem várias mídias e comentários. Follower conecta usuários por duas chaves estrangeiras: a chave primária composta impede seguidores duplicados e uma restrição impede seguir a si mesmo. Media aceita apenas `image` ou `video`. Ao excluir uma publicação pelo ORM, suas mídias e comentários são excluídos. A serialização exclui a senha; uma implementação de autenticação deve armazenar seu hash.

## Execução local

Requisitos: Python 3.13, Pipenv e o executável nativo do Graphviz (`dot`) no PATH. O pacote Python `graphviz` não instala `dot`. Neste Mac, o Graphviz já está disponível no ambiente Pipenv do projeto.

```bash
pipenv install
pipenv run diagram
pipenv run test
```

Você também pode gerar o diagrama com `pipenv run python src/models.py`. O resultado é `diagram.png` na raiz. A geração e os testes não precisam de servidor de banco de dados nem de arquivo `.env`. Os testes usam SQLite real em memória com chaves estrangeiras habilitadas.

![Diagrama entidade-relacionamento](diagram.png)

Legenda: PK = chave primária, FK = chave estrangeira, UQ = único, * = obrigatório. As linhas representam relações um para muitos. As restrições do tipo de mídia e de seguidores estão em `src/models.py`.

## Fontes

Este repositório é um fork do [exercício oficial](https://github.com/breatheco-de/exercise-instagram-data-modeling). Os arquivos iniciais de Flask vêm do [template flask-rest-hello da escola](https://github.com/4GeeksAcademy/flask-rest-hello). O modelo segue o diagrama de referência com cinco entidades. Os arquivos de API, implantação e migrações do template foram preservados; estão fora do escopo desta entrega. Você não precisa de Codespace.
