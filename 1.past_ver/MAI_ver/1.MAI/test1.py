import F_getHoga as hoga


sell_ls = [50,50,50,50,50,50]
buy_ls = [10,560,50,3000,3,5]




def analyze(buy,sell):
    ls=[]
    for i in range(len(buy_ls)):
        print(buy_ls[i])
    
    print('\n')


    for i in range(len(buy_ls)):
        print(sell_ls[i])
        
    print('\n\n\n')


    for i in range(len(buy_ls)):
        print(buy[i]-sell[i])
         




analyze(buy_ls,sell_ls)

