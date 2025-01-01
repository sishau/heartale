import requests
import time
from server.legado import legado
from tools import logger

class reader(legado):
    def __init__(self, conf):
        super().__init__(conf)

    def save_book_progress(self, chapter_index: int=None, chapter_pos: int=None):
        """Save the book progress to the server.

        Args:
            chapter_index (int): the index of the chapter to save.
        """
        url = f"{self.base_url}/saveBookProgress"
        curTimeStamp = int(time.time() * 1000)
        if chapter_index is None:
            chapter_index = self.cur_chapter_index        
        if chapter_pos is None:
            chapter_pos = self.cur_chapter_pos
        chapter_title = self.book_data.get_title_by_index(chapter_index)
        data = {
            "url": self.book_data.bookUrl,
            "index": chapter_index,
            "name": self.book_data.name,
            "author": self.book_data.author,
            "durChapterIndex": chapter_index,
            "durChapterPos": chapter_pos,
            "durChapterTitle": chapter_title,
            "durChapterTime": curTimeStamp
        }
        response = requests.get(url, json=data, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to save book progress. Status code: {response.status_code}")
