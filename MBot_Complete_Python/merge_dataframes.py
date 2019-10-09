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
export_filename = 'output.xlsx'
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
print(tx_ctrl_m_df.dtypes)
print(tx_metadata_df.dtypes)

tx_ctrl_m_df['FROM_TIME'] = tx_ctrl_m_df.astype({'FROM_TIME': str})
tx_metadata_df['FROM_TIME'] = tx_metadata_df.astype({'FROM_TIME': str})
print(tx_metadata_df.dtypes)

tx_merge_df = pd.merge(tx_ctrl_m_df, tx_metadata_df, left_on=('JOB_NAME')
                       , right_on=('JOB_NAME'))
#
print(tx_ctrl_m_df.shape)
print(tx_metadata_df.shape)
print(tx_merge_df.shape)
print(tx_merge_df.head())
print(tx_merge_df.columns.values)
