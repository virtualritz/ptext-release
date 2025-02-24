#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <main> tags
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


class MainTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <main> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <main> element,
        False otherwise
        """
        return html_element.tag == "main"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <main> tag to its corresponding LayoutElement
        """

        # find BodyTagTransformer
        body_tag_transformer: typing.Optional[BaseTagTransformer] = next(
            iter(
                [
                    x
                    for x in self.get_root_tag_transformer().get_children()
                    if x.__class__.__name__ == "BodyTagTransformer"
                ]
            ),
            None,
        )
        assert body_tag_transformer is not None

        # tail of html_element should be process by whoever is processing <main>

        # process
        body_tag_transformer.transform(html_element, parent_elements, layout_element)
