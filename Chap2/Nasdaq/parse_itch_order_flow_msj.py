import warnings
import matplotlib

warnings.filterwarnings('ignore')


import yfinance
import gzip
import shutil
from struct import unpack
from collections import namedtuple, Counter, defaultdict
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urljoin
from datetime import timedelta
from time import time

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

############################################################
### This exercise cant be done cause of Nasdaq paid data ###
############################################################

sns.set_style('whitegrid')

def format_time(t):
    """ Return a formatted time string 'HH:MM:SS based on a numeric time() value"""
    m, s = divmod (t, 60)
    h, m = divmod (m, 60)
    return f'{h:0>2.0f}:{m:0>2.0f}{s:0>2.0f}'


FTP_URL = 'https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/'
SOURCE_FILE = '10302019.NASDAQ_ITCH50.gz'

file_name = may_be_download(urljoin(FTP_URL, SOURCE_FILE))
date = file_name.name.split('.')[0]

data_path = Path('data')
itch_store = str(data_path / 'itch.h5')
order_book_store = data_path / 'order_book.h5'


def may_be_download(url):
    """Download & unzip ITCH data if not yet available"""
    if not data_path.exists():
        print('Creating directory')
        data_path.mkdir()
    else: 
        print('Directory exists')

    filename = data_path / url.split('/')[-1]        
    if not filename.exists():
        print('Downloading...', url)
        urlretrieve(url, filename)
    else: 
        print('File exists')        

    unzipped = data_path / (filename.stem + '.bin')
    if not unzipped.exists():
        print('Unzipping to', unzipped)
        with gzip.open(str(filename), 'rb') as f_in:
            with open(unzipped, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else: 
        print('File already unpacked')
    return unzipped


#The ITCH data needs to be converted from binary to structs

#Event Code
event_code = {
    'O': 'Start of Messages',
    'S': 'Start of System Hours',
    'Q': 'Start of Market Hours',
    'M': 'End of Market Hours',
    'E': 'End of System Hours',
    'C': 'End of Messages'
}

encoding = {
    'primary_market_maker': {'Y': 1, 'N': 0},
    'printable'           : {'Y': 1, 'N': 0},
    'buy_sell_indicator'  : {'B': 1, 'S': -1},
    'cross_type'          : {'O': 0, 'C': 1, 'H': 2},
    'imbalance_direction' : {'B': 0, 'S': 1, 'N': 0, 'O': -1}
}

formats = {
    ('integer', 2): 'H', # int of length 2 => format string 'H'
    ('integer', 4): 'I',
    ('integer', 6): '6s', # int of length 6 => parse as string, convert later
    ('integer', 8): 'Q',
    ('alpha', 1) : 's',
    ('alpha', 2) : '2s',
    ('alpha', 4) : '4s',
    ('alpha', 8) : '8s',
    ('price_4', 4): 'I',
    ('price_8', 8): 'Q',
}

#write a function to parse the data






