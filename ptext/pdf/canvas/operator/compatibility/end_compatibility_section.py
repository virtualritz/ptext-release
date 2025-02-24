#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(PDF 1.1) Begin a compatibility section. Unrecognized operators (along with
their operands) shall be ignored without error until the balancing EX operator
is encountered.
"""
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndCompatibilitySection(CanvasOperator):
    """
    (PDF 1.1) Begin a compatibility section. Unrecognized operators (along with
    their operands) shall be ignored without error until the balancing EX operator
    is encountered.
    """

    def __init__(self):
        super().__init__("EX", 0)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the EX operator
        """
        canvas_stream_processor.get_canvas().in_compatibility_section = False
