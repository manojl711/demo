import pandas as pd
import re

alerts_df = pd.read_csv('group_alerts_tst.csv')
print('alerts_df.shape = ', alerts_df.shape)
print('\n', alerts_df.dtypes)
print(alerts_df.to_string())

# Aggregates Jobnames, Interface names and Table names base on 'STATUS', 'DM_WORK_GROUP', 'ODATE', 'REGION'
agg_lvl_1 = alerts_df.groupby(['STATUS', 'DM_WORK_GROUP', 'ODATE', 'REGION'], as_index=False).agg(
    lambda x: ', '.join(set(x.dropna()))).sort_values(['ALERT_TIMESTAMP', 'ODATE', 'STATUS', 'ORDER_TABLE', 'JOB_NAME'],
                                                      ascending=False)
print(agg_lvl_1.to_string())
# agg_lvl_1['New_msg'] = 'Date ' + agg_lvl_1['ODATE'].astype(str) + ' ' + agg_lvl_1['STATUS'] + ' jobs are ' + agg_lvl_1['JOB_NAME'] + '(' + agg_lvl_1[
#     'INTERFACE_NAME'] + ')'

# Concatenate aggregated columns into simple msg
agg_lvl_1['NEW_MSG'] = agg_lvl_1['STATUS'] + ' jobs are ' + agg_lvl_1['JOB_NAME'] + '(' + agg_lvl_1[
    'INTERFACE_NAME'] + ')'

# Aggregates 'Simple msg', STATUS' and 'ORDER_TABLE' based on 'DM_WORK_GROUP', 'ODATE', 'REGION'
agg_lvl_2 = agg_lvl_1.groupby(['DM_WORK_GROUP', 'ODATE', 'REGION'], as_index=False).agg(
    lambda x: ' and '.join(set(x.dropna())))[
    ['DM_WORK_GROUP', 'ODATE', 'REGION', 'ORDER_TABLE', 'APPLICATION', 'NEW_MSG'
     ]].sort_values(['ODATE', 'ORDER_TABLE'], ascending=False)

# get unique_id from json file
with open('unique_id.txt') as f:
    unique_id = f.read()

# Removing duplicate table_names
# print('ORDER_TABLE = ',agg_lvl_2['ORDER_TABLE'])

for index, row in agg_lvl_2.iterrows():
    words = set(re.findall(r'[^,\s]+', row['ORDER_TABLE']))
    tab_list = [i for i in words if i != 'and']
    tab_list.sort()
    agg_lvl_2.loc[index, 'ORDER_TABLE'] = ','.join(tab_list)
    unique_id = unique_id + 1
    agg_lvl_2.loc[index, 'UNIQUE_ID'] = row['DM_WORK_GROUP'] + str(unique_id)
    print(agg_lvl_2.loc[index, 'UNIQUE_ID'])
    agg_lvl_2.loc[index, 'NEW_MSG'] = 'Date ' + str(row['ODATE']) + ', ' + row['NEW_MSG'] + ', TABLE_NAME = ' + \
                                      agg_lvl_2.loc[index, 'ORDER_TABLE'] + ', ID=' + agg_lvl_2.loc[index, 'UNIQUE_ID']

# Generate final message by removing duplicate table_names and adding Unique ID
print('ORDER_TABLE = ', agg_lvl_2['ORDER_TABLE'])
#    re.findall(r'[^,\s]+', row['ORDER_TABLE'])


# unique_tables = agg_lvl_2['ORDER_TABLE']
# re.split('and',str)
# for
# agg_lvl_2['ORDER_TABLE'] = re.findall(r'[^,\s]+', agg_lvl_2['ORDER_TABLE'])

agg_lvl_2.to_csv('msg_tst_result.csv', index=False)
# s.str.cat(sep=', ')
