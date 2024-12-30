class BookData:
    def __init__(self):
        # 章节目录
        self.chap_names = []
        # 章节目录所在位置
        self.chap_p2s = []
        # 这次是从第几个章节开始读的
        self.chap_n0 = 0
        # 现在是第几个章节
        self.chap_n = 0
        # 某章节的文本分割
        self.chap_txts = []
        # 某章节的文本分割所在位置
        self.chap_txt_p2s = [0]
        # 某章节的文本分割位置
        self.chap_txt_n = 0

    def set_chap_names(self, chap_names, chap_n, chap_p2s=None):
        
        self.chap_names = chap_names
        self.chap_n = chap_n
        self.chap_p2s = chap_p2s

