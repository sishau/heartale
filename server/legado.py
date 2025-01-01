import requests
import time
from tools.BookData import BookData
from tools import logger

class legado:
    def __init__(self, conf):
        self.conf = conf
        self.book_data = None
        self.base_url = None
        self.cur_chapter_index = 0
        self.cur_chapter_pos = 0
        self.base_url = "http://{}:{}".format(self.conf['host'], self.conf['port'])

    def __del__(self):
        self.save_book_progress()

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
            if index < len(data):
                return data[index]
            else:
                logger.error(f"Book index {index} out of range.")
        else:
            logger.error(f"Failed to get book info from server. Status code: {response.status_code}")

    def _get_book_chapters(self):
        """Get the book chapters from the server.
        Returns:
            the book chapters in a list.
        """
        url = f"{self.base_url}/getChapterList"
        params = {
            "url": self.book_data.bookUrl
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()["data"]
            return [d["title"] for d in data]
        else:
            logger.error(f"Failed to get book chapters from server. Status code: {response.status_code}")

    def _get_book_content(self, chapter_index: int=None):
        """Get the book content from the server.
        Args:
            chapter_index (int): the index of the chapter to read.

        Returns:
            the book content in a dictionary.
        """
        url = f"{self.base_url}/getBookContent"
        if chapter_index is None:
            chapter_index = self.cur_chapter_index
        params = {
            "url": self.book_data.bookUrl,
            "index": chapter_index
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            logger.error(f"Failed to get book content from server. Status code: {response.status_code}")

    def initialize(self):
        self.book_data = None        
        book_info = self._get_book_info()
        if not book_info:
            raise Exception("Failed to get book info from server.")
        self.cur_chapter_index = book_info["durChapterIndex"]
        self.cur_chapter_pos = book_info["durChapterPos"]
        self.book_data = BookData(book_info)

        chap_list = self._get_book_chapters()
        if not chap_list:
            raise Exception("Failed to get book chapters from server.")
        self.book_data.chapterList = chap_list

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
            "name": self.book_data.name,
            "author": self.book_data.author,
            "durChapterIndex": chapter_index,
            "durChapterPos": chapter_pos,
            "durChapterTitle": chapter_title,
            "durChapterTime": curTimeStamp
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to save book progress. Status code: {response.status_code}")

    def GenText(self):
        """Go to the next data to read.
        """
        while True:
            chapter_content = self._get_book_content(self.cur_chapter_index)
            logger.info(f"Generating text from chapter {self.book_data.get_title_by_index(self.cur_chapter_index)}")
            if not chapter_content:
                logger.error("Failed to get book content from server.")
            text_list = self.book_data.split_text(chapter_content, self.cur_chapter_index, self.cur_chapter_pos)
            for text in text_list:
                logger.info(f"Yielding {len(text["text"])} characters of text.")
                yield text
            self.cur_chapter_index += 1
            self.cur_chapter_pos = 0
