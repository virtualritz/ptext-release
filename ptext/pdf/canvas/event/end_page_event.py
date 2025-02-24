#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered right after the Canvas has been processed.
"""
from ptext.pdf.canvas.event.event_listener import Event
from ptext.pdf.page.page import Page


class EndPageEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has been processed.
    """

    def __init__(self, page: Page):
        self._page: Page = page

    def get_page(self) -> Page:
        """
        This function returns the Page that triggered this BeginPageEvent
        """
        return self._page
