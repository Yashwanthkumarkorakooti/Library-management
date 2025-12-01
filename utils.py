from datetime import datetime 
from typing import Optional 

def parse_int(value: str) -> int:
    try:
        v = int(value)
        return v 
    except ValueError:
        raise ValueError(f'Invalid integer: {value}')
    
def parse_positive_int(value: str) -> int:
    v = parse_int(value)
    if v <= 0:
        raise ValueError('Value must be positive')
    return v 

def parse_datetime(value: str) -> datetime:
    fmts=['%Y-%m-%d %H:%M','%Y-%m-%d','%d-%m-%Y %H:%M', '%d-%m-%Y']
    for f in fmts:
        try:
            return datetime.strptime(value,f)
        except ValueError:
            continue
    raise ValueError(f'Invalid datetime. Expected formats like YYYY-MM-DD HH:MM')