#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a common base for all LayoutElement implementations
that attempt to represent tabular data.
"""
import typing
from decimal import Decimal
from math import ceil

from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.layout_element import LayoutElement, Alignment
from ptext.pdf.page.page import Page


class TableCell(LayoutElement):
    """
    This class represents a single cell of a table
    """

    def __init__(
        self,
        layout_element: LayoutElement,
        row_span: int = 1,
        col_span: int = 1,
        preferred_width: typing.Optional[Decimal] = None,
        preferred_height: typing.Optional[Decimal] = None,
        border_top: bool = True,
        border_right: bool = True,
        border_bottom: bool = True,
        border_left: bool = True,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        background_color: typing.Optional[Color] = None,
    ):
        super(TableCell, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            background_color=background_color,
        )
        self._layout_element = layout_element
        assert row_span >= 1
        assert col_span >= 1
        assert not isinstance(
            layout_element, TableCell
        ), "TableCell should not contain other TableCell LayoutElement(s)."
        assert not isinstance(
            layout_element, BaseTable
        ), "TableCell should not contain BaseTable LayoutElement(s)."

        # grid coordinates taken up by the TableCell
        self._row_span = row_span
        self._col_span = col_span
        self._table_coordinates: typing.List[typing.Tuple[int, int]] = []

        # width of the TableCell
        self._min_width: typing.Optional[Decimal] = None
        self._max_width: typing.Optional[Decimal] = None
        self._preferred_width: typing.Optional[Decimal] = preferred_width

        # height of the TableCell
        self._min_height: typing.Optional[Decimal] = None
        self._max_height: typing.Optional[Decimal] = None
        self._preferred_height: typing.Optional[Decimal] = preferred_height

    def calculate_min_and_max_width(self) -> None:
        """
        This method calculates the minimum and maximum width of the content
        in this TableCell. It uses an iterative process to gradually hone in on the
        minimum width, which can be quite labour-intensive.
        """
        max_bounding_box: Rectangle = self._calculate_layout_box(
            Page(),
            Rectangle(Decimal(0), Decimal(0), Decimal(2048), Decimal(2048)),
        )
        self._max_width = ceil(max_bounding_box.get_width()) + Decimal(1)
        self._min_height = ceil(max_bounding_box.get_height()) + Decimal(1)
        min_width_upper_bound: Decimal = self._max_width
        min_width_lower_bound: Decimal = Decimal(1)
        while (min_width_upper_bound - min_width_lower_bound) > 1:
            midpoint: Decimal = (
                min_width_upper_bound + min_width_lower_bound
            ) / Decimal(2)
            midpoint = Decimal(int(midpoint))
            try:
                # attempt layout
                self._calculate_layout_box(
                    Page(),
                    Rectangle(Decimal(0), Decimal(0), Decimal(midpoint), Decimal(2048)),
                )

                # check bounding box to see if layout made it
                bb: typing.Optional[Rectangle] = self.get_bounding_box()
                assert bb is not None
                self._max_height = ceil(bb.get_height()) + Decimal(1)
                if bb.get_width() > midpoint:
                    min_width_lower_bound = midpoint
                else:
                    min_width_upper_bound = midpoint
            except:
                min_width_lower_bound = midpoint

        # copy bounds
        self._min_width = min_width_upper_bound

    def _calculate_layout_box_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        return self._layout_element._calculate_layout_box(page, bounding_box)

    def layout(self, page: Page, layout_box: Rectangle) -> Rectangle:
        """
        This function calculates the layout box and performs layout for this LayoutElement.
        TableCell propagates the padding to its inner LayoutElement.
        """
        modified_layout_box: Rectangle = Rectangle(
            layout_box.x + self._padding_left,
            layout_box.y + self._padding_bottom,
            layout_box.width - self._padding_left - self._padding_right,
            layout_box.height - self._padding_top - self._padding_bottom,
        )
        returned_layout_box: Rectangle = self._layout_element.layout(
            page, modified_layout_box
        )

        modified_returned_layout_box: Rectangle = Rectangle(
            returned_layout_box.x - self._padding_left,
            returned_layout_box.y - self._padding_bottom,
            returned_layout_box.width + self._padding_left + self._padding_right,
            returned_layout_box.height + self._padding_top + self._padding_bottom,
        )
        self.set_bounding_box(modified_returned_layout_box)

        # return
        return modified_returned_layout_box

    def _draw_border(self, page: Page, border_box: Rectangle):
        # This method is purposefully blank, to ensure the parent (Table)
        # is the only element that gets to call the _draw_border_after_layout method
        # which properly renders the borders.
        pass

    def _draw_border_after_layout(self, page: Page):
        assert self.bounding_box is not None
        super(TableCell, self)._draw_border(page, self.bounding_box)

    def _draw_background(self, page: Page, border_box: Rectangle):
        # This method is purposefully blank, to ensure the parent (Table)
        # is the only element that gets to call the _draw_background_after_layout method
        # which properly renders the background.
        pass

    def _draw_background_after_layout(self, page: Page, border_box: Rectangle):
        super(TableCell, self)._draw_background(page, border_box)


class BaseTable(LayoutElement):
    """
    This class represents a common base for all LayoutElement implementations
    that attempt to represent tabular data.
    """

    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: Decimal = Decimal(0),
        margin_right: Decimal = Decimal(0),
        margin_bottom: Decimal = Decimal(0),
        margin_left: Decimal = Decimal(0),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        background_color: typing.Optional[Color] = None,
    ):
        super(BaseTable, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
        assert number_of_rows >= 1
        assert number_of_columns >= 1
        self._number_of_rows = number_of_rows
        self._number_of_columns = number_of_columns
        self._content: typing.List[TableCell] = []

    def set_background_color_on_all_cells(self, background_color: Color) -> "BaseTable":
        """
        This method sets the background Color on all TableCell objects in this BaseTable
        """
        for e in self._content:
            e._background_color = background_color
        return self

    def set_border_width_on_all_cells(self, border_width: Decimal) -> "BaseTable":
        """
        This method sets the border width on all TableCell objects in this BaseTable
        """
        assert border_width >= 0
        for e in self._content:
            e._border_width = border_width
        return self

    def set_border_color_on_all_cells(self, border_color: Color) -> "BaseTable":
        """
        This method sets the border color on all TableCell objects in this BaseTable
        """
        for e in self._content:
            e._border_color = border_color
        return self

    def set_padding_on_all_cells(
        self,
        padding_top: Decimal,
        padding_right: Decimal,
        padding_bottom: Decimal,
        padding_left: Decimal,
    ) -> "BaseTable":
        """
        This method sets the padding on all TableCell objects in this BaseTable
        """
        for e in self._content:
            e._padding_top = padding_top
            e._padding_right = padding_right
            e._padding_bottom = padding_bottom
            e._padding_left = padding_left
        return self

    def set_borders_on_all_cells(
        self,
        border_top: bool,
        border_right: bool,
        border_bottom: bool,
        border_left: bool,
    ) -> "BaseTable":
        """
        This method sets the border(s) on all TableCell objects in this BaseTable
        """
        for e in self._content:
            e._border_top = border_top
            e._border_right = border_right
            e._border_bottom = border_bottom
            e._border_left = border_left
        return self

    def no_borders(self) -> "BaseTable":
        """
        This method unsets the border(s) on all TableCell objects in this BaseTable
        """
        self.set_borders_on_all_cells(False, False, False, False)
        return self

    def outer_borders(self) -> "BaseTable":
        """
        This method unsets the border(s) on all TableCell objects in this BaseTable
        except for the borders that form the outside edge of the BaseTable
        """
        self.no_borders()
        for c in self._get_cells_at_row(0):
            c._border_top = True
        for c in self._get_cells_at_row(self._number_of_rows - 1):
            c._border_bottom = True
        for c in self._get_cells_at_column(0):
            c._border_left = True
        for c in self._get_cells_at_column(self._number_of_columns - 1):
            c._border_right = True
        return self

    def internal_borders(self) -> "BaseTable":
        """
        This method sets the border(s) on all TableCell objects in this BaseTable
        except for the borders that form the outside edge of the BaseTable
        """
        for tc in self._content:
            tc._border_top = True
            tc._border_right = True
            tc._border_bottom = True
            tc._border_left = True
        for c in self._get_cells_at_row(0):
            c._border_top = False
        for c in self._get_cells_at_row(self._number_of_rows - 1):
            c._border_bottom = False
        for c in self._get_cells_at_column(0):
            c._border_left = False
        for c in self._get_cells_at_column(self._number_of_columns - 1):
            c._border_right = False
        return self

    def even_odd_row_colors(
        self, even_row_color: Color, odd_row_color: Color
    ) -> "BaseTable":
        """
        This function colors the BaseTable with the classic "zebra stripes"
        e.a. one color for all even rows, and a contrasting color for the odd rows.
        This function returns self.
        """
        for r in range(0, self._number_of_rows):
            for tc in self._get_cells_at_row(r):
                if r % 2 == 0:
                    tc._background_color = even_row_color
                else:
                    tc._background_color = odd_row_color
        return self

    def _get_cells_at_column(self, column: int) -> typing.List[TableCell]:
        out: typing.List[TableCell] = []
        for t in self._content:
            if len([p for p in t._table_coordinates if p[1] == column]) > 0:
                out.append(t)
        return out

    def _get_cells_at_row(self, row: int) -> typing.List[TableCell]:
        out: typing.List[TableCell] = []
        for t in self._content:
            if len([p for p in t._table_coordinates if p[0] == row]) > 0:
                out.append(t)
        return out

    def add(self, layout_element: LayoutElement) -> "BaseTable":
        """
        This function adds the given LayoutElement to this Table.
        This function returns self.
        """

        # embed LayoutElement in TableCell (if needed)
        if not isinstance(layout_element, TableCell):
            layout_element = TableCell(layout_element)

        # add content
        self._content.append(layout_element)

        # set font_size
        inner_layout_element: LayoutElement = layout_element._layout_element
        if self._font_size is None:
            self._font_size = inner_layout_element.get_font_size()

        # determine gridpoints occupied by the new TableCell
        first_non_complete_row: int = min(
            [
                x
                for x in range(0, self._number_of_rows)
                if sum([y._col_span for y in self._get_cells_at_row(x)])
                < self._number_of_columns
            ]
        )
        first_empty_column: int = sum(
            [x._col_span for x in self._get_cells_at_row(first_non_complete_row)]
        )
        for i in range(0, layout_element._row_span):
            for j in range(0, layout_element._col_span):
                layout_element._table_coordinates.append(
                    (first_non_complete_row + i, first_empty_column + j)
                )

        # return
        return self
