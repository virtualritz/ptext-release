import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestAddCircleAnnotation(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_add_circle_annotation(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a circle annotation"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add annotation
        w: Decimal = pdf.get_page(0).get_page_info().get_width()
        h: Decimal = pdf.get_page(0).get_page_info().get_height()
        pdf.get_page(0).append_circle_annotation(
            rectangle=Rectangle(
                w / Decimal(2) - Decimal(32),
                h / Decimal(2) - Decimal(32),
                Decimal(64),
                Decimal(64),
            ),
            stroke_color=HexColor("86CD82"),
            fill_color=HexColor("72A276"),
        )

        # attempt to store PDF
        with open(self.output_dir / "output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # attempt to re-open PDF
        with open(self.output_dir / "output.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        return True
