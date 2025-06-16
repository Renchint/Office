import pandas as pd 
import re
import numpy as np

name_cols = {'Title' : 'title',
            'price' : 'price_total',
            'Date'  : 'date',
            'Time'  : 'time',
            'id'    : 'ad_id',
            'loc'   : 'location',
            'message' : 'ad_text',
            'Талбай:' : 'size',
            'Барилгын явц:'          : 'progress_cons',
            'Төлбөрийн нөхцөл:'      : 'payment_terms',
            }


main_path = 'result'

# Load the data
df = pd.read_csv(main_path + '/ads_data_2025-06-16_16-27-22.csv')

df.columns # column names
df.head()  # first 5 rows
df.tail()  # last 5 rows

# Split the data into 3 parts
cols = df.columns
df[cols[:5]]
df[cols[5:10]]
df[cols[10:20]]
df[cols[20:]]

df.info() # data types and missing values
df['price']
df['Талбай:']

# fillna
# df['phone'] = df['phone'].fillna('99119911') 
df = df.drop(columns='phone')
df = df.drop(columns='Төлбөрийн нөхцөл:')
df = df.drop(columns='page_number')
df = df.drop(columns='ad_number')

## NA Check for missing values
df.isna()
df.isna().sum() # axis=0
df.isna().sum(axis=1)

# dropna
df.dropna(subset=['Талбай:','Барилгын явц:'],how='all')

# Duplicates
df.duplicated() # if duplicated
df.duplicated().sum() # number of unique duplicates

df[df.duplicated()] # duplicated rows
df[df.duplicated()]['id'].value_counts() # duplicated ids


df_dup = df[df.duplicated()] # duplicated rows
df_dup[df_dup['id'] == 8862403]
df[df['id'] == 8862403]

df.drop_duplicates(subset=['id', 'date'], keep='first',inplace=True)

# rename columns
df.rename(columns=name_cols, inplace=True)
df.drop(columns=['location:','Байршил:'], inplace=True)

# AREA and PRICE
df[['price_total','size']]

df['area'] = df['size'].apply(
    lambda x: float(re.findall(r'\d+[\.\d]*', str(x))[0]) if pd.notnull(x) and re.findall(r'\d+[\.\d]*', str(x)) else None
)
df[['area','size']]
df[['area','size']].dtypes

df['price'] = df['price_total'].apply(lambda x: re.findall(r'\d+[\.\d]*', x)[0]).astype(float)
df[['price','price_total']]
df[['price','price_total']].dtypes

# terbum
mask = df['price_total'].str.contains('бум', na=False) & (df['price'] < 10)
df.loc[mask, 'price'] = df.loc[mask, 'price'] * 1000

df['price'].describe()
df.sort_values(by='price', ascending=False)

# price interval
# interval
p_int = [-np.inf,15,50,100,200,300,500,1000,5000,np.inf]
df['p_int'] = pd.cut(df['price'], bins=p_int, include_lowest=True)
df[['price','p_int']].dtypes
df['p_int'].value_counts().sort_values()

df[df['p_int'] == pd.Interval(5000, np.inf, closed='right')]
df[df['p_int'] == pd.Interval(-np.inf, 15, closed='right')]
df[df['p_int'] == pd.Interval(15, 50, closed='right')]
df[df['p_int'] == pd.Interval(-np.inf, 2, closed='right')]
df[df['p_int'] == pd.Interval(10, 15, closed='right')]
df[df['p_int'] == pd.Interval(15, 20, closed='right')]


# correct price for 8797210
df[df['ad_id'] == 8797210]

df.loc[df['ad_id'] == 8797210,'price'] = 250


# area interval
a_int = [0, 10, 20, 50, 100, 400, np.inf]
df['a_int'] = pd.cut(df['area'], bins=a_int, include_lowest=True)
df[['area','a_int']]
df['a_int'].value_counts().sort_values()

df[df['a_int'] == pd.Interval(400, np.inf, closed='right')]
df[df['a_int'] == pd.Interval(-0.001, 10, closed='right')]

df.loc[df['ad_id'] == 8744513,'area'] = 50.65
df.loc[df['ad_id'] == 8746788,'area'] = 40.22


# remove outliers
df = df[df['area'] > 10]
df = df[df['area'] < 400]

df = df[(df['price'] < 15) | (df['price'] > 50)] # remove irregular prices, 15-50

# price per m2

df['price_m2'] = df['price']

mask = df['price'] > 15

df.loc[mask, 'price_m2'] = df.loc[mask, 'price'] / df.loc[mask, 'area']

df.sort_values(by='price_m2', ascending=False)[['price','price_m2','area','title','price_total']]

p_int = [-np.inf,1,2,5,10,15,np.inf]
df['p2_int'] = pd.cut(df['price_m2'], bins=p_int, include_lowest=True)
df['p2_int'].value_counts().sort_values()

df[df['price_m2']<=1][['price_total','price','area','price_m2','title','ad_id','ad_text']]

df.loc[df['ad_id'] == 8525257,'price'] = 994.4
df.loc[df['ad_id'] == 8706949,'price'] = 520
df.loc[df['ad_id'] == 8525257,'price_m2']
df.loc[df['ad_id'] == 8706949,'price_m2']


df[df['price_m2']>15][['price_total','price','area','price_m2','title','ad_id','ad_text']]

# remove outliers 
df = df[df['price_m2'] <= 15]


# location 
df_loc = pd.read_csv(main_path + '/input/location.csv')

df = df.merge(df_loc, how='left', on='location')

df['mylocation'].value_counts()
df['mylocation'].isna().sum()

df[df['mylocation'].isna()][['location','mylocation']]


df.groupby('mylocation').agg({'price_m2':['median','min','max','count']}).sort_values(by=('price_m2','median'), ascending=False)

df[(df['mylocation'] == 'Хүннү') & (df['price_m2'] < 5)][['ad_text','title','location','price_m2','area']]

df.to_csv("Clean.csv", index=False, encoding='utf-8-sig')