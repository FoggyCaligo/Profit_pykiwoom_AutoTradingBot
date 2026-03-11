#로그인/SendOrder/실시간데이터처리/잔고처리 등등 api 관련된 함수들 모아놓은 파일
import pandas as pd
import pykiwoom.kiwoom as kiwoom


class API:
    def __init__(self):
        super().__init__()
        self.kiwoom = kiwoom.Kiwoom()
        self.kiwoom.CommConnect(block=True)

    def connect_code(self, code):
        self.kiwoom.SetRealReg("1000", code, "41", 0)
