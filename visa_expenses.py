import pandas as pd

from visa_utils import Item, Category, print_section


class col:
    need = 'need?'
    amount = 'amount'
    category = 'category'


file = 'D:/Users/johnm/OneDrive/money/visa_expenses.csv'
df = pd.read_csv(file)
df['need?'] = '-'
df['category'] = '-'
df = df.loc[df['Credit'].isna()]
df = df.drop('Credit', axis=1)
df = df.loc[~df['Debit'].isna()]
df = df.rename(columns={'Debit': 'amount'})
df['amount'] = df['amount'].str.replace('$', '').str.strip().astype(float)

items_str = [['SIMONS WEB', 'no', 'clothes'], ['PATTES ET GRIFFES', 'yes', 'dog'], ['A&W', 'no', 'restaurant'],
             ['CORDOVA', 'no', 'restaurant'], ['LA DIPERIE', 'no', 'restaurant'], ["LLOYDIE'S", 'no', 'restaurant'],
             ['RESTAURANT GREENSPOT', 'no', 'restaurant'], ['SQDC', 'no', 'weed'], ['UBER', 'no', 'restaurant'],
             ['AMZN', 'yes', 'amazon'], ['AMAZON', 'yes', 'amazon'],
             ['SUPER C', 'yes', 'groceries'],
             ['CLINIQUE VETERINAIRE', 'yes', 'muffin'],
             ['PURCHASE INTEREST', 'no', 'interest'],
             ['JEAN COUTU', 'yes', 'meds'],
             ['FLAIR DIRECT0000000000123', 'kinda', 'flight'],
             ['VRIT', 'no', 'unsure'],
             ['CAFE', 'no', 'restaurant'],
             ['BAR BARA', 'no', 'restaurant'],
             ['BAR BARA', 'no', 'restaurant'],
             ['BOARDGAMEBLISS', 'kinda', 'gift'],
             ['BRASSEUR DE MONTREAL', 'kinda', 'gift'],
             ['LUCKY MOBILE', 'yes', 'phone'],
             ['STM', 'no', 'transport'],
             ['DOLLARAMA', 'yes', 'snacks'],
             ['NETFLIX', 'no', 'subscription'],
             ['LEJEUNE ET FRERES', 'no', '-'],
             ['RUSTIQUE', 'no', 'snacks'],
             ['UNIBURGER', 'no', Category.restaurant],
             ['METRO ETS', 'no', 'transport'],
             ['BOUCHERIE', 'no', Category.restaurant],
             ['WHATNOT', 'kinda', 'gift'],
             ['BIXI', 'yes', 'transport'],
             ['CANNA CABANA', 'yes', 'weed'],
             ['SHELL', 'no', 'transport'],
             ['FLAIR TICKETING', 'no', Category.flight],
             ['HRBLOCK.CA', 'yes', 'taxes'],
             ['IGA BECK-NOTRE-DAME', 'yes', Category.groceries],
             ['SHOPPERS DRUG MART', 'yes', Category.meds],
             ['METTA YOGA CALGARY', 'no', Category.fun],
             ['7-ELEVEN STORE', 'no', Category.snacks],
             ["BRANCHE D'OLIVIER", 'yes', Category.groceries],
             ['CE GLENMORE SQUARE', 'no'],
             ['3730-MNTR GALLERIA REL', 'no'],
             ['AHS PLC PARKING LOTS', 'no', Category.parking],
             ['CORSO T3', 'no', Category.restaurant]
             ]
reimbursed = ['SL.NORD', 'PETROCAN', 'aliexpress', 'TWISTED ELEMENT']
df = df[~df['Description'].str.contains('|'.join(reimbursed))]

items = []
for item in items_str:
    item_obj = Item(*item)
    item.append(item_obj)
    df.loc[df['Description'].str.contains(item_obj.store), col.need] = item_obj.need
    df.loc[df['Description'].str.contains(item_obj.store), col.category] = item_obj.category
df_sum = df.groupby('need?').sum('amount')
df_sum['%'] = ((df_sum['amount'] / df_sum['amount'].sum() * 100).round()).astype(float)
df_sum = df_sum[['amount', '%']]
df = df.sort_values('amount', ascending=False)
df_uncategorized = df[df[col.need] == '-']

df_category = df.groupby('category').agg({'amount': 'sum', col.need: 'first'})
df_category['%'] = ((df_category['amount'] / df_category['amount'].sum() * 100).round()).astype(float)
df_category = df_category[['amount', '%', 'need?']]
df_category = df_category.sort_values('amount', ascending=False)
df.to_csv('expenses_analyzed.csv', index=False, header=True)

if not df_uncategorized.empty:
    print_section('needs categorized still', start=True)
    print(df[df[col.need] == '-'])
    print_section('needs categorized still', start=False)
print('----- Categories - Start -----')
print(df_category.to_string())
print('----- Categories - End -----')
print('----- Summary - Start -----')
print(df_sum.to_string())
print('----- Summary - End -----')
print('----- By Month - Start -----')
df_monthly = df.groupby(['need?', df['Date'].dt.month]).sum('amount')
print(df_monthly.to_string())
print('----- By Month - End -----')
