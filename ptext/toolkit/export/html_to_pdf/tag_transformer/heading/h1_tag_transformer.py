#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <h1> tags
"""
import xml.etree.ElementTree as ET

import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.text.heading import Heading
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class H1TagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <h1> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <h1> element,
        False otherwise
        """
        return html_element.tag == "h1"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <h1> tag to its corresponding LayoutElement
        """
        assert html_element.text is not None, "<h1> should have text"
        assert (
            len(html_element.getchildren()) == 0
        ), "<h1> children are currently not supported"
        layout_element.add(  # type: ignore[union-attr]
            Heading(html_element.text, font="Helvetica-Bold", font_size=Decimal(32))
        )
