import pandas as pd
from datetime import datetime
import numpy as np

# Control M Table details
tx_column_names = ['ELAPSED_RUNTIME',
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
                   'ODATE',
                   'MEMNAME',
                   'JOB_NAME',
                   'ORDER_TABLE',
                   'ORDER_ID',
                   'JOB_ID',
                   'GROUP_NAME'
                   ]
ax_column_names = ['CPU_ID',
                   'NODEGROUP',
                   'ORDER_ID',
                   'JOB_NAME',
                   'ORDER_TABLE',
                   'ODATE',
                   'STATUS',
                   'FROM_TIME',
                   'STATE',
                   'START_TIME',
                   'END_TIME',
                   'RERUN_COUNTER',
                   'CYCLIC',
                   'CPU_TIME',
                   'CONFIRM_FLAG']

tx_ctrl_m_file_path = 'Opttx1p.txt'
ax_ctrl_m_file_path = 'Optax1p.txt'
export_filename = 'ctrl.xlsx'
export_filename2 = 'meta.xlsx'
control_m_sep = '|'

# Metadata Tables
tx_metadata_file_path = 'Tx Metadata - Latest.txt'
ax_metadata_file_path = 'Ax Metadata - Latest.txt'
metadata_sep = ','


# Methods
def read_file(file_path, sep, col_names):
    # When records have header, Consider col_names in the file
    if col_names is None:
        return pd.read_csv(file_path, sep=sep)
    return pd.read_csv(file_path, sep=sep, names=col_names)


# Read Files
# Data miner files
tx_ctrl_m_df = read_file(tx_ctrl_m_file_path, control_m_sep, tx_column_names)
ax_ctrl_m_df = read_file(ax_ctrl_m_file_path, control_m_sep, ax_column_names)
# Metadata tables
tx_metadata_df = read_file(tx_metadata_file_path, metadata_sep, None)
ax_metadata_df = read_file(ax_metadata_file_path, metadata_sep, None)

# Replace all blank cells to NaN
tx_ctrl_m_df = tx_ctrl_m_df.replace(r'^\s*$', np.nan, regex=True)
ax_ctrl_m_df = ax_ctrl_m_df.replace(r'^\s*$', np.nan, regex=True)
tx_metadata_df = tx_metadata_df.replace(r'^\s*$', np.nan, regex=True)
ax_metadata_df = ax_metadata_df.replace(r'^\s*$', np.nan, regex=True)

# Append SYSDATE
tx_ctrl_m_df['SYSDATE'] = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), format='%Y-%m-%d %H:%M:%S',
                                         errors='ignore')
ax_ctrl_m_df['SYSDATE'] = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), format='%Y-%m-%d %H:%M:%S',
                                         errors='ignore')

# Convert string to Datetime format
# Tx
tx_ctrl_m_df['ODATE'] = pd.to_datetime(tx_ctrl_m_df['ODATE'], format='%y%m%d', errors='ignore')
tx_ctrl_m_df['START_TIME'] = pd.to_datetime(tx_ctrl_m_df['START_TIME'], errors='coerce')
tx_ctrl_m_df['END_TIME'] = pd.to_datetime(tx_ctrl_m_df['END_TIME'], errors='coerce')
# tx_ctrl_m_df['FROM_TIME'] = pd.to_datetime(tx_ctrl_m_df['FROM_TIME'], format='%H%M').apply(pd.Timestamp)


# Combine ODATE and FROM_TIME
# tx_metadata_df['FROM_TIME'] = pd.to_datetime(tx_ctrl_m_df['Date'].apply(str)+' '+tx_metadata_df['FROM_TIME'])


# format='%Y%m%d%h%m%s'


tx_ctrl_m_df = tx_ctrl_m_df[['SYSDATE', 'ORDER_ID',
                             'ODATE',
                             'JOB_NAME',
                             'MEMNAME',
                             'ORDER_TABLE',
                             'STATUS',
                             'STATE',
                             'START_TIME',
                             'END_TIME',
                             'ELAPSED_RUNTIME',
                             'FROM_TIME',
                             'CYCLIC']]

print(tx_ctrl_m_df['SYSDATE'].head())
print(tx_ctrl_m_df['ODATE'].head())
# print(tx_ctrl_m_df['START_TIME'].head())

print(tx_ctrl_m_df[tx_ctrl_m_df['START_TIME'].notnull()][['ORDER_ID', 'START_TIME']].head(10))
# print(tx_ctrl_m_df[tx_ctrl_m_df['START_TIME'] != ' '][['ORDER_ID','START_TIME']].head(10))
print(tx_ctrl_m_df[tx_ctrl_m_df['END_TIME'].notnull()][['ORDER_ID', 'END_TIME']].head(10))
print(tx_ctrl_m_df.dtypes)

# print(tx_ctrl_m_df['END_TIME'].head())
# select ODATE + THRESHOLD_START_TIME from tx_metadata_df where CRITICAL_NOT_STARTED_JOBS_FLAG == 'Y'

# Select THRESHOLD_START_TIME where THRESHOLD_START_TIME is not null
# print(tx_metadata_df[tx_metadata_df['THRESHOLD_START_TIME'].notnull()]['THRESHOLD_START_TIME'].head())


# Select max(odate)
print('MAX ODATE = ', tx_ctrl_m_df['ODATE'].max())
max_odate_df = pd.DataFrame({'max_odate': [str(tx_ctrl_m_df['ODATE'].max())]
                             }
                            )

# pd.to_datetime(max_odate_df['max_odate'] + ' ' + tx_metadata_df[tx_metadata_df['CRITICAL_NOT_STARTED_JOBS_FLAG'] == 'Y']['THRESHOLD_START_TIME']))


# Select THRESHOLD_START_TIME where CRITICAL_NOT_STARTED_JOBS_FLAG == 'Y'
print('\nTHRESHOLD_START_TIME')
print(tx_metadata_df[tx_metadata_df['CRITICAL_NOT_STARTED_JOBS_FLAG'] == 'Y']['THRESHOLD_START_TIME'].head())
print(tx_metadata_df.dtypes)

tx_ctrl_m_df.to_excel(export_filename, index=False)
tx_metadata_df.to_excel(export_filename2, index=False)

print('\nExport Completed')
print('==============================')
