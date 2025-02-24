#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible
for writing Dictionary objects of \Type \Page
"""
import logging
from typing import Optional

from ptext.io.read.types import AnyPDFType, Dictionary, Name
from ptext.io.write.object.write_dictionary_transformer import (
    WriteDictionaryTransformer,
)
from ptext.io.write.write_base_transformer import WriteTransformerContext
from ptext.pdf.document import Document

logger = logging.getLogger(__name__)


class WritePageTransformer(WriteDictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Page
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents an \Page Dictionary
        """
        return isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Page"

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes a \Page Dictionary to a byte stream
        """
        assert isinstance(object_to_transform, Dictionary)
        assert (
            context is not None
        ), "A WriteTransformerContext must be defined in order to write Page objects."
        assert context.root_object is not None

        assert isinstance(context.root_object, Document)
        pages_dict = context.root_object["XRef"]["Trailer"]["Root"]["Pages"]

        # add \Parent reference to \Pages
        object_to_transform[Name("Parent")] = self.get_reference(pages_dict, context)

        # mark some keys as non-referencable
        for k in ["ArtBox", "BleedBox", "CropBox", "MediaBox", "TrimBox"]:
            if k in object_to_transform:
                object_to_transform[k].set_can_be_referenced(False)

        # delegate to super
        super(WritePageTransformer, self).transform(object_to_transform, context)
