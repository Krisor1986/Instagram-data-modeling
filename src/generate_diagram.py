"""Render the model metadata as a standalone entity relationship diagram."""

from html import escape
from pathlib import Path

from graphviz import Digraph


def generate_diagram(metadata):
    diagram = Digraph("Instagram", format="png")
    diagram.attr(rankdir="LR", bgcolor="white", pad="0.3", nodesep="0.6", ranksep="1.1", dpi="140")
    diagram.attr("node", shape="plain", fontname="Helvetica")
    diagram.attr("edge", fontname="Helvetica", fontsize="10", color="#64748b",
                 dir="both", arrowtail="tee", arrowhead="crow")

    for table in metadata.sorted_tables:
        rows = [f'<TR><TD COLSPAN="2" BGCOLOR="#075985"><FONT COLOR="white"><B>{escape(table.name)}</B></FONT></TD></TR>']
        for column in table.columns:
            markers = []
            if column.primary_key:
                markers.append("PK")
            if column.foreign_keys:
                markers.append("FK")
            if column.unique:
                markers.append("UQ")
            prefix = f"{' / '.join(markers)} " if markers else ""
            required = "" if column.nullable else " *"
            rows.append(
                f'<TR><TD PORT="{column.name}" ALIGN="LEFT">{escape(prefix + column.name + required)}</TD>'
                f'<TD ALIGN="LEFT"><FONT COLOR="#475569">{escape(str(column.type))}</FONT></TD></TR>'
            )
        diagram.node(table.name, label='<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="7">' + "".join(rows) + '</TABLE>>')

    for table in metadata.sorted_tables:
        for foreign_key in table.foreign_keys:
            diagram.edge(
                f"{foreign_key.column.table.name}:e",
                f"{table.name}:{foreign_key.parent.name}:w",
            )

    diagram.attr(label="Instagram Data Model | PK: primary key · FK: foreign key · UQ: unique · *: required", labelloc="b", fontname="Helvetica", fontsize="12")
    destination = Path(__file__).resolve().parents[1] / "diagram"
    diagram.render(filename=str(destination), cleanup=True)
    print(f"Diagram generated: {destination}.png")
