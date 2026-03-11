import datetime

import FinanceDataReader as fdr
import utils.time
import pandas as pd
import data.params

class StockList:
    def __init__(self, api, params):
        self.api = api
        self.params = params
        self.stockList = self.get_filtered_stock_list()

    def get_filtered_stock_list(self, price_min=None, price_max=None, vol_min=None, vol_max=None):
        kospi = fdr.StockListing('KOSPI')
        kospi.sort_values(by=['Marcap'], ascending=False)#시가총액 큰 순서대로 정렬
        top = kospi[:self.params.search_stockamount] #시가총액 상위 search_stockamount개 뽑기
        
        if(price_min is not None and price_max is not None and vol_min is not None and vol_max is not None):
            
            stock_list = fdr.StockListing('KRX')[['Name', 'Code']]
            stock_list = stock_list[stock_list['Code'].str.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
            filtered_stock_list = []
            for code in stock_list['Code']:
                try:
                    price = self.api.get_price(code)
                    vol = self.api.get_volatility(code)
                    if price_min <= price <= price_max and vol_min <= vol <= vol_max:
                        filtered_stock_list.append(code)
                except Exception as e:
                    print(f"Error fetching data for {code}: {e}")
            return pd.DataFrame(filtered_stock_list, columns=['Code'])


        stock_list = fdr.StockListing('KRX')[['Name', 'Code']]
        stock_list = stock_list[stock_list['Code'].str.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
        return stock_list
