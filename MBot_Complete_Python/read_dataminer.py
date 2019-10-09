import pandas as pd
from datetime import datetime

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
control_m_sep = '|'

# Metadata Tables
tx_metadata_file_path = 'Tx Metadata - Latest.txt'
ax_metadata_file_path = 'Ax Metadata - Latest.txt'
metadata_sep = ','


# Methods
def read_file(file_path, sep, col_names):
    if col_names is None:
        return pd.read_csv(file_path, sep=sep)
    return pd.read_csv(file_path, sep=sep, names=col_names)


# Read Files
tx_ctrl_m_df = read_file(tx_ctrl_m_file_path, control_m_sep, tx_column_names)
ax_ctrl_m_df = read_file(ax_ctrl_m_file_path, control_m_sep, ax_column_names)

tx_metadata_df = read_file(tx_metadata_file_path, metadata_sep, None)
ax_metadata_df = read_file(ax_metadata_file_path, metadata_sep, None)

# Merge Control_M and Metadata

# current_time = datetime.now()

tx_ctrl_m_df['SYSDATE'] = datetime.now()

tx_ctrl_m_cols = tx_ctrl_m_df[['SYSDATE', 'ORDER_ID',
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

ax_ctrl_m_df['SYSDATE'] = datetime.now()
ax_ctrl_m_cols = ax_ctrl_m_df[['SYSDATE', 'ORDER_ID',
                               'ODATE',
                               'JOB_NAME',
                               'JOB_NAME',
                               'ORDER_TABLE',
                               'STATUS',
                               'STATE',
                               'START_TIME',
                               'END_TIME',
                               'CPU_TIME',
                               'FROM_TIME',
                               'CYCLIC',
                               ]]

print('tx_ctrl_m_cols.head() = ', tx_ctrl_m_cols.head())
print('ax_ctrl_m_cols.head() = ', ax_ctrl_m_cols.head())

print('tx_ctrl_m_cols.dtypes = ', tx_ctrl_m_cols.dtypes)
print('ax_ctrl_m_cols.dtypes = ', ax_ctrl_m_cols.dtypes)

print('==============================')

# From Merged Data Extract Failed, Long Run and Not Started
# Failed


# Long Run


# Not Started


###################################################################################

# To display all file


# TX Ctrl_m
print('\ntx_ctrl_m_df.shape = ', tx_ctrl_m_df.shape)
print('\ntx_ctrl_m_df.columns.values')
print(tx_ctrl_m_df.columns.values)
print(tx_ctrl_m_df['ORDER_TABLE'].value_counts())

# AX Ctrl_m
print('\nax_ctrl_m_df.shape = ', ax_ctrl_m_df.shape)
print('\nax_ctrl_m_df.columns.values')
print(ax_ctrl_m_df.columns.values)
# print(ax_ctrl_m_df['ORDER_TABLE'].value_counts())


# TX Metadata
print('\ntx_metadata_df.shape = ', tx_metadata_df.shape)
print('\ntx_metadata_df.columns.values')
print(tx_metadata_df.columns.values)
print(tx_metadata_df['CTRLM_TABLE_NAME'].value_counts())

# AX Metadata
print('\nax_metadata_df.shape = ', ax_metadata_df.shape)
print('\nax_metadata_df.columns.values')
print(ax_metadata_df.columns.values)
# print(ax_metadata_df['CTRLM_TABLE_NAME'].value_counts())
