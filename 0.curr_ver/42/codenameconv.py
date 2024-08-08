import FinanceDataReader as fdr
import pandas as pd


# dt = {}



df = fdr.StockListing('KRX')[['Name', 'Code']]

def get_name(code):
    return str(df[df['Code']==code]['Name'])


print(get_name("005930"))
