#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(PDF 1.1) Same as CS but used for nonstroking operations.
"""
from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType, Name
from ptext.pdf.canvas.color.color import CMYKColor, GrayColor, RGBColor, Separation
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetColorSpaceNonStroking(CanvasOperator):
    """
    (PDF 1.1) Same as CS but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("cs", 1)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the cs operator
        """
        assert isinstance(operands[0], Name), "Operand 0 of cs must be a Name"
        color_space_name: Name = operands[0]
        color_space: List = []

        if color_space_name not in [
            "DeviceGray",
            "DeviceRGB",
            "DeviceCMYK",
            "CalGray",
            "CalRGB",
            "Lab",
            "ICCBased",
            "Indexed",
            "Pattern",
            "Separation",
        ]:
            color_space_name = canvas_stream_processor.get_resource(
                "ColorSpace", color_space_name
            )

        if not isinstance(color_space_name, Name) and isinstance(
            color_space_name, List
        ):
            assert isinstance(color_space_name[0], Name)
            color_space = color_space_name
            color_space_name = color_space_name[0]

        #
        # Device
        #
        canvas = canvas_stream_processor.get_canvas()
        if color_space_name == "DeviceGray":
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = GrayColor(Decimal(0))
            return

        if color_space_name == "DeviceRGB":
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = RGBColor(
                Decimal(0), Decimal(0), Decimal(0)
            )
            return

        if color_space_name == "DeviceCMYK":
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = CMYKColor(
                Decimal(0), Decimal(0), Decimal(0), Decimal(1)
            )
            return

        #
        # CIE-based
        #

        if color_space_name == "CalGray":
            # fmt: off
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = GrayColor(Decimal(0))
            return
            # fmt: on
        if color_space_name == "CalRGB":
            # fmt: off
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = RGBColor(Decimal(0), Decimal(0), Decimal(0))
            return
            # fmt: on
        if color_space_name == "Lab":
            canvas.graphics_state.non_stroke_color_space = color_space_name
            return
        if color_space_name == "ICCBased":
            # fmt: off
            canvas.graphics_state.non_stroke_color_space = color_space_name
            canvas.graphics_state.non_stroke_color = RGBColor(Decimal(0), Decimal(0), Decimal(0))
            return
            # fmt: on

        #
        # Special
        #

        if color_space_name == "Indexed":
            canvas.graphics_state.non_stroke_color_space = color_space_name
            return
        if operands[0] == "Pattern":
            canvas.graphics_state.non_stroke_color_space = operands[0]
            return
        if color_space_name == "Separation":
            # fmt: off
            canvas.graphics_state.non_stroke_color_space = color_space
            canvas.graphics_state.non_stroke_color = Separation(color_space, [Decimal(0)])
            # fmt: on
