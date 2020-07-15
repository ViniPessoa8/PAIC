import math

def format_number(num):
    if (num < 1000):
        str_out = 'R$' + str(num)
    elif (num < 1000000 ):
        num     = math.trunc(num/1000)
        str_out = 'R$' + str(num) + 'K'
    elif (num < 1000000000):
        num     = math.trunc(num/1000000)  
        str_out = 'R$' + str(num) + 'M'
    elif (num > 1000000000000):
        num     = math.trunc(num/1000000000)   
        str_out = 'R$' + str(num) + 'B'

    return str_out