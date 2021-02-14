import numpy as np
import pandas as pd
import QuantLib as ql
import math
import datetime
import matplotlib.pyplot as plt
import requests
import warnings

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 30)

from_date='20200402'
until_date='20201020'
chosen_matu = ['20201218']

folder1 = '/Users/pvamb/A7/Dispersion Volatility/processed'
folder2 = '/Users/pvamb/A7/Dispersion Volatility/parameters'
folder3 = '/Users/pvamb/A7/Dispersion Volatility/XY'
folder4 = '/Users/pvamb/A7/Dispersion Volatility/MLoutput'

# https://www.marketscreener.com/quote/index/EURO-STOXX-50-7396/components/col=7&asc=0

index_list = [('OESX', 3655.77, '', '', 'FESX')]

udl_list = [
    ('SAP', 108.47, 6.17, 'DE0007164600', ''),
    ('ASM', 460, 5.69, 'NL0010273215', ''),
    ('LIN', 257.37, 4.69, 'IE00BZ12WP82', ''),
    ('MOH', 528.7, 4.58, 'FR0000121014', ''),
    ('SNW', 80.01, 4.13, 'FR0000120578', ''),
    ('SIE', 133.06, 3.42, 'DE0007236101', ''),
    ('TOTB', 35.07, 3.16, 'FR0000120271', ''),
    ('ALV', 195.77, 2.89, 'DE0008404005', ''),
    ('LOR', 305.6, 2.89, 'FR0000120321', ''),
    ('AIR', 136.25, 2.74, 'FR0000120073', ''),
    ('IBE', 11.26, 2.57, 'ES0144580Y14', ''),
    ('SND', 124.6, 2.52, 'FR0000121972', ''),
    ('ENL5', 8.439, 2.45, 'IT0003128367', ''),
    ('BAY', 56.15, 2.21, 'DE000BAY0017', ''),
    ('ADS', 278, 2.2, 'DE000A1EWWW0', ''),
    ('BAS', 66.86, 2.02, 'DE000BASF111', ''),
    ('ADY', 1884.5, 1.86, 'NL0012969182', ''),
    ('PPX', 549, 1.81, 'FR0000121485', ''),
    ('SQU', 86, 1.71, 'FR0000125486', ''),
    ('ITK', 54.78, 1.64, 'BE0974293251', ''),
    ('DPW', 42.165, 1.63, 'DE0005552004', ''),
    ('DAI', 66.9, 1.61, 'DE0007100000', ''),
    ('PHI1', 47.08, 1.54, 'NL0000009538', ''),
    ('EAD', 93.42, 1.53, 'NL0000235190', ''),
    ('BSN', 53.34, 1.5, 'FR0000120644', ''),
    ('BNP', 53.595, 1.5, 'FR0000131104', ''),
    # ('PROSUS', 100.05, 1.44, 'NL0013654783', ''), no option
    ('ESL', 128.75, 1.44, 'FR0000121667', 'no stock on Xetra'),
    ('AXA', 19.204, 1.37, 'FR0000120628', ''),
    # ('KONE', 66.03, 1.29, 'FI0009013403', ''), no option
    ('MUV2', 233.5, 1.58, 'DE0008430026', ''),
    ('SEJ', 112.2, 1.26, 'FR0000073272', 'no stock on Xetra'),
    ('ANN', 55.53, 1.26, 'DE000A1ML7J1', ''),
    ('IES5', 2.059, 1.22, 'IT0000072618', ''),
    ('DB1', 136.4, 1.21, 'DE0005810055', ''),
    ('AHO', 23.35, 1.18, 'NL0011794037', ''),
    ('PER', 163.2, 1.15, 'FR0000120693', ''),
    ('IXD', 26.115, 1.12, 'ES0148396007', ''),
    ('BSD2', 2.774, 1.11, 'ES0113900J37', ''),
    ('VO3', 162.35, 1.07, 'DE0007664039', ''),
    ('CRG', 35.51, 1.05, 'US12626K2033', 'no stock on Xetra'),
    ('INN', 7.766, 0.99, 'NL0011821202', ''),
    ('AI3A', 56.37, 0.9, 'ES0109067019', 'no stock on Xetra'),
    ('VVU', 25.92, 0.87, 'FR0000127771', ''),
    ('BMW', 70.295, 0.83, 'DE0005190003', ''),
    ('NOA3', 3.495, 0.8, 'FI0009000681', ''),
    ('ENT5', 8.645, 0.7, 'IT0003132476', '')]

