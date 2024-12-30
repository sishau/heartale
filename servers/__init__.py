class Server:
    def __init__(self):
        self._book_name = ""
        self._conf = None

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, conf):
        self._conf = conf

    def next(self):
        """ 接下来要阅读的文本
        """
        pass

    def save(self):
        """ 保存当前阅读进度
        """
        pass

