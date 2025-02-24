#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Decimal objects
"""
from typing import Optional

from ptext.io.read.types import AnyPDFType, Decimal
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteNumberTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Decimal objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a Decimal object
        """
        return isinstance(any, Decimal)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes a Decimal to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Decimal)

        is_integer = object_to_transform == int(object_to_transform)

        if is_integer:
            context.destination.write(bytes(str(int(object_to_transform)), "latin1"))
        else:
            context.destination.write(
                bytes("{:.2f}".format(float(object_to_transform)), "latin1")
            )
