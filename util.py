import pandas as pd
import glob
import os
import re
import numpy as np

def extract_currency_value(x):
    price = float(re.findall('(\\d+[\\.\\d]*)', x)[0])
    if 'бум' in x and 'сая' not in x:
        return price * 1e3
    else:
        return price 
def extract_numeric_area_values(x):
    x = float(re.findall('(\d+[\.\d]*)', x)[0])
    return x

def get_district(x):
    try:
        x = re.findall('(Баянгол|Баянзүрх|Сүхбаатар|Сонгинохайрхан|Хан-Уул|Чингэлтэй|Налайх)', x)[0]
    except:
        x = 'province'
    return x

def get_khoroo(x):
    try:
        x = re.findall(r"(?<=Хороо)\s+(\d*)", x)
        if len(x) == 0: # this because no sublocation after district
            x = ""
        else:
            x = x[0]        
    except:
        pass
    return x

name_cols = {'Title' : 'title',
            'price' : 'price_total',
            'Date'  : 'date',
            'Time'  : 'time',
            'id'    : 'ad_id',
            'room'  : 'room_num',
            'loc'   : 'location',
            'message' : 'ad_text',
            'Шал:'  : 'floor_type',
            'Тагт:' : 'balcony_num',
            'Ашиглалтанд орсон он:' : 'date_op',
            'Гараж:': 'garage',
            'Цонх:' : 'window_type',
            'Барилгын давхар:' : 'floor_num',
            'Хаалга:' : 'door_type',
            'Талбай:' : 'size',
            'Хэдэн давхарт:'         : 'floor_at',
            'Лизингээр авах боломж:' : 'leasing',
            'Цонхны тоо:'            : 'window_num',
            'Барилгын явц:'          : 'progress_cons',
            'Төлбөрийн нөхцөл:'      : 'payment_terms',
            'Цахилгаан шаттай эсэх:' : 'lift',
            }

def filter_dataframe_by_column_range(df, column, min_value, max_value):
    df = df[(df[column] >= min_value) & (df[column] <= max_value)]
    return df