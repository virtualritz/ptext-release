#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <abbr> tags
"""
import xml.etree.ElementTree as ET

import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from ptext.pdf.canvas.layout.text.heading import Heading
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class AbbrTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <abbr> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <a> element,
        False otherwise
        """
        return html_element.tag == "abbr"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <abbr> tag to its corresponding LayoutElement
        """
        assert all(
            [self._contains_only_text_children(x) for x in html_element.getchildren()]
        )

        # font
        font_name: str = self._get_default_font_for_html_element(
            parent_elements + [html_element]
        )

        assert html_element.text is not None
        chunks_of_text: HeterogeneousParagraph = HeterogeneousParagraph([])
        chunks_of_text.add(ChunkOfText(html_element.text, font=font_name))

        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], chunks_of_text
            )

        # TODO: provide dotted underline + text annotation

        # correct spacing
        self._correct_spacing_for_chunks_of_text(chunks_of_text)

        # add to parent
        layout_element.add(chunks_of_text)  # type: ignore [union-attr]
