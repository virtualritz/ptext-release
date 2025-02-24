#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <h5> tags
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


class H5TagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <h5> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <h5> element,
        False otherwise
        """
        return html_element.tag == "h5"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <h5> tag to its corresponding LayoutElement
        """
        assert html_element.text is not None, "<h5> should have text"
        assert (
            len(html_element.getchildren()) == 0
        ), "<h5> children are currently not supported"
        layout_element.add(  # type: ignore[union-attr]
            Heading(html_element.text, font="Helvetica-Bold", font_size=Decimal(13))
        )
