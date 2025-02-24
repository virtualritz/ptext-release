#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Restore the graphics state by removing the most recently saved
state from the stack and making it the current state (see 8.4.2,
"Graphics State Stack").
"""
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class PopGraphicsState(CanvasOperator):
    """
    Restore the graphics state by removing the most recently saved
    state from the stack and making it the current state (see 8.4.2,
    "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("Q", 0)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the Q operator
        """
        canvas = canvas_stream_processor.get_canvas()
        assert (
            len(canvas.graphics_state_stack) > 0
        ), "Stack underflow. Q operator was applied to an empty stack."
        canvas.graphics_state = canvas.graphics_state_stack.pop(-1)
