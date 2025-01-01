#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .logger import logger
class BookData:
    def __init__(self, book_info: dict):
        self.name = book_info["name"]
        self.author = book_info["author"]
        self.bookUrl = book_info["bookUrl"]
        self.lastChapterIndex = book_info["durChapterIndex"]
        self.lastChapterPos = book_info["durChapterPos"]
        self.lastChapterTitle = book_info["durChapterTitle"]
        self.chapterList = []
        self.len_limit = 100

    def get_title_by_index(self, index: int) -> str:
        if index < 0 or index >= len(self.chapterList):
            return ""
        return self.chapterList[index]

    def split_text(self, text: str, chap_index: int= 0, position: int=0) -> list:
        result = [
            {
                "text": f"{self.name}...{self.chapterList[chap_index]}",
                "chapterIndex": chap_index,
                "position": position
            }
        ]
        cur_pos = 0
        this_line = ""
        for line in text.strip().split("\n"):
            cur_pos += len(line)
            if cur_pos < position:
                continue            
            this_line += line.strip()
            if len(this_line) > self.len_limit:
                result.append({"text": this_line, "chapterIndex": chap_index, "position": cur_pos})
                this_line = ""
                if self.len_limit < 500:
                    self.len_limit += 10
        if this_line:
            result.append({"text": this_line, "chapterIndex": chap_index, "position": cur_pos})
        return result
