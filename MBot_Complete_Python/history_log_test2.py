import pandas as pd
from mj_settings import Settings
from datetime import datetime

mbot_settings = Settings()

# Read and Daily and Master data
daily_log_df = pd.read_csv('daily_log_tst.csv', sep=mbot_settings.metadata_sep,
                           dtype=mbot_settings.dtypes2)

master_log_df = pd.read_csv('master_log_tst.csv', sep=mbot_settings.metadata_sep,
                            dtype=mbot_settings.dtypes2)

# tx_ctrl_m_df.to_csv('master_log_tst.csv', index=False)

print('\ndaily_log_df ', daily_log_df.shape)
print('master_log_df ', master_log_df.shape)

# Extract Unique ODATE and ORDER_ID from daily ctrl_m refresh data and extract subset of Master data
subset_master_log_df = master_log_df[(master_log_df.ODATE.isin(daily_log_df['ODATE'].drop_duplicates().sort_values())) &
                                     (master_log_df.ORDER_ID.isin(
                                         daily_log_df['ORDER_ID'].drop_duplicates().sort_values()))][
    mbot_settings.tx_column_names]

print('subset_master_log_df ', subset_master_log_df.shape)

# For these subset_master_log (ODATE and ORDER_ID), update Master Log from Daily Log
# Take (ODATE and ORDER_ID) that are common in both Master and Daily, UPDATE master_log with daily_log
new_df = subset_master_log_df.merge(daily_log_df, indicator=True, how="left", )[
    lambda x: x._merge == 'left_only'].drop('_merge', 1)
print('\nRecords that require UPDATES')
print(new_df[['ODATE', 'ORDER_ID']].drop_duplicates().sort_values(by=['ODATE', 'ORDER_ID']))
print(new_df.shape)

# tx_ctrl_m_df['LOG_CAPTURED_TIMESTAMP'] = datetime.now()


for index, row in new_df.iterrows():
    # Set Max Odate
    odate = row['ODATE']
    order_id = row['ORDER_ID']

    master_log_df.loc[(master_log_df['ODATE'] == odate) &
                      (master_log_df['ORDER_ID'] == order_id),
                      ['LOG_CAPTURED_TIMESTAMP',
                       'ELAPSED_RUNTIME',
                       'DELETE_FLAG',
                       'AVG_START_TIME',
                       'AVG_RUNTIME',
                       'TIME_ZONE',
                       'PRIORITY',
                       'CYCLIC',
                       'MAX_RERUN',
                       'END_TIME',
                       'START_TIME',
                       'FROM_TIME',
                       'STATUS',
                       'STATE',
                       'MEMNAME',
                       'JOB_NAME',
                       'ORDER_TABLE',
                       'JOB_ID',
                       'GROUP_NAME'
                       ]] = [datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'ELAPSED_RUNTIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'DELETE_FLAG'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'AVG_START_TIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'AVG_RUNTIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'TIME_ZONE'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'PRIORITY'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'CYCLIC'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'MAX_RERUN'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'END_TIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'START_TIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'FROM_TIME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'STATUS'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'STATE'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'MEMNAME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'JOB_NAME'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'ORDER_TABLE'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'JOB_ID'].values[0],
                             daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                     daily_log_df['ORDER_ID'] == order_id), 'GROUP_NAME'].values[0]
                             ]

# These Daily Log records that are extracted, should be inserted into Master_Log
# Take (ODATE and ORDER_ID) from Daily and Insert into Master_Log
r_new_df = daily_log_df.merge(subset_master_log_df, indicator=True, how="left", left_on=['ODATE', 'ORDER_ID'],
                              right_on=['ODATE', 'ORDER_ID'])[
    lambda x: x._merge == 'left_only'].drop('_merge', 1)
print('\nRecords that should be INSERTED')
print(r_new_df[['ODATE', 'ORDER_ID']].drop_duplicates().sort_values(by=['ODATE', 'ORDER_ID']))
print(r_new_df.shape)

for index, row in r_new_df.iterrows():
    odate = row['ODATE']
    order_id = row['ORDER_ID']

    master_log_df = master_log_df.append({'LOG_CAPTURED_TIMESTAMP': datetime.now().strftime(mbot_settings.date_format5),
                                          'ELAPSED_RUNTIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'ELAPSED_RUNTIME'].values[0],
                                          'DELETE_FLAG': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'DELETE_FLAG'].values[0],
                                          'AVG_START_TIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'AVG_START_TIME'].values[0],
                                          'AVG_RUNTIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'AVG_RUNTIME'].values[0],
                                          'TIME_ZONE': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'TIME_ZONE'].values[0],
                                          'PRIORITY': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'PRIORITY'].values[0],
                                          'CYCLIC': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'CYCLIC'].values[0],
                                          'MAX_RERUN': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'MAX_RERUN'].values[0],
                                          'END_TIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'END_TIME'].values[0],
                                          'START_TIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'START_TIME'].values[0],
                                          'FROM_TIME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'FROM_TIME'].values[0],
                                          'STATUS': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'STATUS'].values[0],
                                          'STATE': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'STATE'].values[0],
                                          'ODATE': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'ODATE'].values[0],
                                          'MEMNAME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'MEMNAME'].values[0],
                                          'JOB_NAME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'JOB_NAME'].values[0],
                                          'ORDER_TABLE': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'ORDER_TABLE'].values[0],
                                          'ORDER_ID': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'ORDER_ID'].values[0],
                                          'JOB_ID': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'JOB_ID'].values[0],
                                          'GROUP_NAME': daily_log_df.loc[(daily_log_df['ODATE'] == odate) & (
                                                  daily_log_df['ORDER_ID'] == order_id), 'GROUP_NAME'].values[0]},
                                         ignore_index=True)

master_log_df.to_csv('master_log_tst.csv', index=False)
##################################################################################################
