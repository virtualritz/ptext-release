#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the character spacing, Tc , to charSpace, which shall be a number
expressed in unscaled text space units. Character spacing shall be used
by the Tj, TJ, and ' operators. Initial value: 0.
"""
from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetCharacterSpacing(CanvasOperator):
    """
    Set the character spacing, Tc , to charSpace, which shall be a number
    expressed in unscaled text space units. Character spacing shall be used
    by the Tj, TJ, and ' operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tc", 1)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the Tc operator
        """
        assert isinstance(operands[0], Decimal), "Operand 0 of Tc must be a Decimal"
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.character_spacing = operands[0]
