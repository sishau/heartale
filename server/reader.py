import requests
import json
from server import Server
from tools import logger

class reader(Server):
    def __init__(self, conf):
        super().__init__(conf)

    def initialize(self):
        self.base_url = "http://{}:{}/reader3".format(self.conf['host'], self.conf['port'])
        book_info = self._get_book_info()

    def _get_book_info(self, index: int=0):
        """
        Get the book info from shelf of the server.
        :param index: the index of the book in the shelf.
        :return: the book information in a dictionary.
        """
        url = f"{self.base_url}/getBookshelf"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()["data"]
            if index < len(data):
                data.sort(key=lambda x: x["durChapterTime"], reverse=True)
                logger.info("Book {} is {}".format(index, data[index]["name"]))
                return data[index]
            else:
                logger.error(f"Book index {index} out of range.")
        else:
            logger.error(f"Failed to get book info from server. Status code: {response.status_code}")

