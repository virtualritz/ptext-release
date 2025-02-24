import unittest
from datetime import datetime
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.image.image import Image
from ptext.pdf.canvas.layout.layout_element import Alignment
from ptext.pdf.canvas.layout.page_layout.browser_layout import BrowserLayout
from ptext.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestAddXLImage(unittest.TestCase):
    """
    This test creates a PDF with an Image in it, this is specified by a URL.
    The Image is too large, and an assert is triggered.
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

    def test_write_document_with_xl_image_001(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add PageLayout
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem[0:5]))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Image in it, this is specified by a URL. The Image is too large, and an assert is triggered."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # we know the image is too large to fit on the Page
        # we should get an assert from the MultiColumnLayout object
        with self.assertRaises(AssertionError):
            # add image
            layout.add(
                Image(
                    "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                    horizontal_alignment=Alignment.CENTERED,
                )
            )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_write_document_with_xl_image_002(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add PageLayout
        layout = BrowserLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem[0:5]))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Image in it, this is specified by a URL. The Image is too large, and an assert is triggered."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # we know the image is too large to fit on the Page
        # we should get an assert from the MultiColumnLayout object
        with self.assertRaises(AssertionError):
            # add image
            layout.add(
                Image(
                    "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                    horizontal_alignment=Alignment.CENTERED,
                )
            )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


if __name__ == "__main__":
    unittest.main()
