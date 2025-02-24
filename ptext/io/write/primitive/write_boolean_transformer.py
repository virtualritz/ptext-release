#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing booleans
"""
from typing import Optional

from ptext.io.read.types import AnyPDFType, Boolean
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteBooleanTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing booleans
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a Boolean object
        """
        return isinstance(any, Boolean)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes a Boolean to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Boolean)

        if bool(object_to_transform):
            context.destination.write(bytes("true", "latin1"))
        else:
            context.destination.write(bytes("false", "latin1"))
