#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <section> tags
"""
import xml.etree.ElementTree as ET

import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from ptext.pdf.canvas.layout.text.heading import Heading
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class SectionTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <section> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <section> element,
        False otherwise
        """
        return html_element.tag == "section"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <section> tag to its corresponding LayoutElement
        """

        # newline (hack)
        layout_element.add(Paragraph(""))  # type: ignore [union-attr]

        # add elements
        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], layout_element
            )

        # newline (hack)
        layout_element.add(Paragraph(""))  # type: ignore [union-attr]
