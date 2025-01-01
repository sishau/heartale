import requests
import time
from server.legado import legado
from tools import logger

class reader(legado):
    def __init__(self, conf):
        super().__init__(conf)
        self.base_url = "http://{}:{}/reader3".format(self.conf['host'], self.conf['port'])

    def _get_book_info(self, index: int=0):
        """Get the book info from shelf of the server.

        Args:
            index (int): the index of the book in the shelf.
        Returns:
            the book information in a dictionary.
        """
        url = f"{self.base_url}/getBookshelf"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()["data"]
            data.sort(key=lambda x: x["durChapterTime"], reverse=True)
            if index < len(data):
                return data[index]
            else:
                logger.error(f"Book index {index} out of range.")
        else:
            logger.error(f"Failed to get book info from server. Status code: {response.status_code}")

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
