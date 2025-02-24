#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <img> tags
"""
import xml.etree.ElementTree as ET

import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.image.image import Image
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.text.heading import Heading
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class ImgTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <img> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <h1> element,
        False otherwise
        """
        return html_element.tag == "img"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <img> tag to its corresponding LayoutElement
        """
        src: typing.Optional[str] = html_element.get("src")
        assert src is not None

        width_as_str: typing.Optional[str] = html_element.get("width")
        width: typing.Optional[Decimal] = None
        if width_as_str is not None:
            width = Decimal(width_as_str)

        height_as_str: typing.Optional[str] = html_element.get("width")
        height: typing.Optional[Decimal] = None
        if height_as_str is not None:
            height = Decimal(height_as_str)

        # TODO: do something with alt text
        alt_as_str: typing.Optional[str] = html_element.get("alt")

        # add Image
        layout_element.add(  # type: ignore[union-attr]
            Image(src, width=width, height=height)
        )
