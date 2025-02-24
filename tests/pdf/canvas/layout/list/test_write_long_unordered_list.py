import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.layout.list.unordered_list import UnorderedList
from ptext.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestWriteLongUnorderedList(unittest.TestCase):
    """
    This test creates a PDF with an unordered list in it.
    """

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

    def test_write_document(self):

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
            .add(Paragraph("This test creates a PDF with an unordered list in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # we know the List is too large to fit on the Page
        # we should get an assert from the MultiColumnLayout object
        with self.assertRaises(AssertionError):
            ul = UnorderedList()
            for _ in range(0, 6):
                ul.add(Paragraph(text="Lorem"))
                ul.add(Paragraph(text="Ipsum"))
                ul.add(Paragraph(text="Dolor"))
                ul.add(Paragraph(text="Sit"))
                ul.add(Paragraph(text="Amet"))
            layout.add(ul)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
