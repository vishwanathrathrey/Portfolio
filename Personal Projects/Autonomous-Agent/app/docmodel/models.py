"""LLM-agnostic document representation between agent output and python-docx rendering.

This separation keeps the renderer deterministic and testable.
"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class BlockTypeEnum(str, Enum):
    """Supported document block types."""

    HEADING1 = "heading1"
    HEADING2 = "heading2"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    TABLE = "table"
    PAGE_BREAK = "page_break"


class TableColumn(BaseModel):
    """A table column definition."""

    header: str
    align: Literal["left", "center", "right"] = "left"


class TableData(BaseModel):
    """Tabular content for a table document block."""

    columns: list[TableColumn] = Field(min_length=1)
    rows: list[list[str]]

    @model_validator(mode="after")
    def validate_row_lengths(self) -> "TableData":
        column_count = len(self.columns)
        if any(len(row) != column_count for row in self.rows):
            raise ValueError("Each table row must contain one value per column.")
        return self


class Block(BaseModel):
    """A single typed unit of document content."""

    type: BlockTypeEnum
    text: str | None = None
    items: list[str] | None = None
    table: TableData | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "Block":
        populated_fields = {
            "text": self.text is not None,
            "items": self.items is not None,
            "table": self.table is not None,
        }
        expected_field = {
            BlockTypeEnum.HEADING1: "text",
            BlockTypeEnum.HEADING2: "text",
            BlockTypeEnum.PARAGRAPH: "text",
            BlockTypeEnum.BULLET_LIST: "items",
            BlockTypeEnum.NUMBERED_LIST: "items",
            BlockTypeEnum.TABLE: "table",
        }.get(self.type)

        if self.type is BlockTypeEnum.PAGE_BREAK:
            if any(populated_fields.values()):
                raise ValueError("Page break blocks cannot include content.")
            return self

        if expected_field is None or not populated_fields[expected_field]:
            raise ValueError(f"{self.type.value} blocks require {expected_field}.")
        if sum(populated_fields.values()) != 1:
            raise ValueError(f"{self.type.value} blocks accept only {expected_field}.")
        return self


class Section(BaseModel):
    """A titled collection of document blocks."""

    title: str
    blocks: list[Block] = Field(default_factory=list)


class Document(BaseModel):
    """The internal, renderer-independent representation of a document."""

    title: str
    subtitle: str | None = None
    author: str = "Autonomous Agent"
    doc_type: str = "business_report"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sections: list[Section] = Field(default_factory=list)

    def add_section(self, title: str) -> Section:
        """Append and return a new titled section."""
        section = Section(title=title)
        self.sections.append(section)
        return section

    def to_docx(self, output_path: Path) -> Path:
        """Raise until the Step 4 document renderer is available."""
        raise NotImplementedError("Renderer is in Step 4 — tools/docx_renderer.py")
