def convert_price_string(price):
    lookup = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    unit = price[-1]
    try:
        number = float(price[:-1])
    
        if unit in lookup:
            return lookup[unit] * number
    
        return int(price)
    
    except ValueError:
        return None
            
def make_price_string(price):
    lookup = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if price > lookup['B']:
        return str(price/lookup['B'])+'B'
    if price > lookup['M']:
        return str(price/lookup['M'])+'M'
    if price > lookup['K']:
        return str(price/lookup['K'])+'K'
    return price
