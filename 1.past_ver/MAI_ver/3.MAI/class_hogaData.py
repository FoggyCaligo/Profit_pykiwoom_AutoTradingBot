from dataclasses import dataclass
from typing import List

@dataclass
class StockData:
    code : int
    buyamount: List[int]
    buyprice : List[int]
    sellamount:List[int]
    sellprice: List[int]

