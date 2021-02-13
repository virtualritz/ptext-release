import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import Paragraph, Justification
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestAddSimpleTable(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../table/test-add-simple-table")

    def test_write_hello_world(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        t = Table(number_of_rows=5, number_of_columns=2)
        t.add(
            Paragraph(
                "Language",
                font_color=X11Color("SteelBlue"),
                font_size=Decimal(20),
                justification=Justification.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=X11Color("SteelBlue"),
                font_size=Decimal(20),
                justification=Justification.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.set_border_width_on_all_cells(Decimal(0.2))

        table_rect = t.layout(
            page,
            bounding_box=Rectangle(
                Decimal(20), Decimal(600), Decimal(500), Decimal(200)
            ),
        )

        Paragraph(
            text="**Data gathered from Stackoverflow.com on 10th of february 2021",
            font_size=Decimal(8),
            font_color=X11Color("Gray"),
            justification=Justification.FLUSH_RIGHT,
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(20), table_rect.y - 40, table_rect.width, Decimal(20)
            ),
        )

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
