from hmac import new

import pandas as pd

class Params:
    def __init__(self):
        df = pd.read_csv("./3_renual_ver_2026/data/csv/parameter.csv")
        self.vol_max = df.loc[0, "vol_max"]
        self.vol_min = df.loc[0, "vol_min"]
        self.price_max = df.loc[0, "price_max"]
        self.price_min = df.loc[0, "price_min"]
        self.search_stockamount = df.loc[0, "search_stockamount"]
        self.min_rev = df.loc[0, "min_rev"]
        pass

    def switch_params(self, new_params):
        self.vol_max = new_params["vol_max"]
        self.vol_min = new_params["vol_min"]
        self.price_max = new_params["price_max"]
        self.price_min = new_params["price_min"]
        self.search_stockamount = new_params["search_stockamount"]
        self.min_rev = new_params["min_rev"]

    def save_params(self):
        df = pd.DataFrame({
            "vol_max": [self.vol_max],
            "vol_min": [self.vol_min],
            "price_max": [self.price_max],
            "price_min": [self.price_min],
            "search_stockamount": [self.search_stockamount],
            "min_rev": [self.min_rev]
        })
        df.to_csv("./3_renual_ver_2026/data/csv/parameter.csv", index=False)


p = Params()

# new_params={
#     "vol_max": 10,
#     "vol_min": 3,
#     "price_max": 20000,
#     "price_min": 5000,
#     "search_stockamount": 200,
#     "min_rev": 0.4
# }
# p.switch_params(new_params)
# p.save_params()