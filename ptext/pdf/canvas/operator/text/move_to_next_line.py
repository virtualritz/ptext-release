#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move to the start of the next line. This operator has the same effect as the
code
0 -Tl Td
where Tl denotes the current leading parameter in the text state. The
negative of Tl is used here because Tl is the text leading expressed as a
positive number. Going to the next line entails decreasing the
y coordinate.
"""
import typing
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.io.read.types import Decimal as pDecimal
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveToNextLine(CanvasOperator):
    """
    Move to the start of the next line. This operator has the same effect as the
    code
    0 -Tl Td
    where Tl denotes the current leading parameter in the text state. The
    negative of Tl is used here because Tl is the text leading expressed as a
    positive number. Going to the next line entails decreasing the
    y coordinate.
    """

    def __init__(self):
        super().__init__("T*", 0)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the T* operator
        """
        move_text_position_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("Td")
        assert (
            move_text_position_op
        ), "Operator Td must be defined for operator T* to function."
        canvas = canvas_stream_processor.get_canvas()
        move_text_position_op.invoke(
            canvas_stream_processor, [pDecimal(0), -canvas.graphics_state.leading]
        )
