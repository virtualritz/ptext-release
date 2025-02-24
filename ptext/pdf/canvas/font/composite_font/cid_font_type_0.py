#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    CID-keyed fonts provide a convenient and efficient method for defining multiple-byte character encodings and
   fonts with a large number of glyphs. These capabilities provide great flexibility for representing text in writing
    systems for languages with large character sets, such as Chinese, Japanese, and Korean (CJK).

    The CID-keyed font architecture specifies the external representation of certain font programs, called CMap
    and CIDFont files, along with some conventions for combining and using those files. As mentioned earlier, PDF
    does not support the entire CID-keyed font architecture, which is independent of PDF; CID-keyed fonts may be
    used in other environments.

    A Type 0 CIDFont contains glyph descriptions based on CFF
"""
import typing

from ptext.io.read.types import Decimal as pDecimal
from ptext.io.read.types import List, Name
from ptext.pdf.canvas.font.font import Font


class CIDType0Font(Font):
    """
    A Type 0 CIDFont contains glyph descriptions based on CFF
    """

    def __init__(self):
        super(CIDType0Font, self).__init__()
        self._width_cache: typing.Dict[int, pDecimal] = {}

    def get_width(self, character_identifier: int) -> typing.Optional[pDecimal]:
        """
        This function returns the width (in text space) of a given character identifier.
        If this Font is unable to represent the glyph that corresponds to the character identifier,
        this function returns None
        """

        # check cache
        if character_identifier in self._width_cache:
            return self._width_cache[character_identifier]

        # Default value: none (the DW value shall be used for all glyphs).
        dw: pDecimal = self["DW"] if "DW" in self else pDecimal(1000)
        if "W" not in self:
            return dw

        assert "W" in self
        assert isinstance(self["W"], List)
        i: int = 0
        cid: int = 0
        cid_width: int = 0
        while i < len(self["W"]):
            # <char_start_code> [<width>+]
            if (
                isinstance(self["W"][i], pDecimal)
                and i + 1 < len(self["W"])
                and isinstance(self["W"][i + 1], List)
            ):
                for j in range(0, len(self["W"][i + 1])):
                    cid = int(self["W"][i]) + j
                    cid_width = int(self["W"][i + 1][j])
                    self._width_cache[cid] = pDecimal(cid_width)
                i += 2
                continue
            # <char_start_code> <char_end_code> <width>
            if (
                isinstance(self["W"][i], pDecimal)
                and i + 2 < len(self["W"])
                and isinstance(self["W"][i + 1], pDecimal)
                and isinstance(self["W"][i + 2], pDecimal)
            ):
                for j in range(int(self["W"][i]), int(self["W"][i + 1]) + 1):
                    cid = j
                    cid_width = int(self["W"][i + 2])
                    self._width_cache[cid] = pDecimal(cid_width)
                i += 3
                continue

        # check cache
        if character_identifier in self._width_cache:
            return self._width_cache[character_identifier]

        # default
        return dw

    def get_ascent(self) -> pDecimal:
        """
        This function returns the maximum height above the baseline reached by glyphs in this font.
        The height of glyphs for accented characters shall be excluded.
        """
        assert "FontDescriptor" in self
        assert "Ascent" in self["FontDescriptor"]
        return self["FontDescriptor"]["Ascent"]

    def get_descent(self) -> pDecimal:
        """
        This function returns the maximum depth below the baseline reached by glyphs in this font.
        The value shall be a negative number.
        """
        assert "FontDescriptor" in self
        assert "Descent" in self["FontDescriptor"]
        return self["FontDescriptor"]["Descent"]

    def _empty_copy(self) -> "Font":
        return CIDType0Font()

    def __deepcopy__(self, memodict={}):
        # fmt: off
        f_out: CIDType0Font = super(CIDType0Font, self).__deepcopy__(memodict)
        f_out[Name("Subtype")] = Name("Type0")
        f_out._width_cache: typing.Dict[int, pDecimal] = {k: v for k, v in self._width_cache.items()}
        return f_out
        # fmt: on
