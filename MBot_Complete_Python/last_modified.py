import os
from mj_settings import Settings
from datetime import datetime
from os.path import getmtime

mbot_settings = Settings()
filename = mbot_settings.alerts_log_file_path

if os.path.exists(filename):
    last_modified_time = getmtime(filename)
    print(type(datetime.fromtimestamp(last_modified_time).strftime('%d/%m/%Y %H:%M:%S')), last_modified_time)
    print("Modification time: {}".format(datetime.fromtimestamp(last_modified_time).strftime('%d/%m/%Y %H:%M:%S')))
else:
    print('File does not exists')

filename = mbot_settings.alerts_log_file_path

if os.path.exists(filename):
    last_modified_time = getmtime(filename)
    get_ctm_tx_last_refresh_df = datetime.fromtimestamp(last_modified_time).strftime('%d-%m-%Y %H:%M:%S')
    # print("Modification time: {}".format(datetime.fromtimestamp(last_modified_time).strftime('%d/%m/%Y %H:%M:%S')))
else:
    print('Dataminer File does not exists')

fmt = '%d-%m-%Y %H:%M:%S'
data_miner_not_working = False
curr_time = datetime.now().strftime(fmt)

formatted_curr_time = datetime.strptime(curr_time, fmt)
formatted_ctm_tx = datetime.strptime(get_ctm_tx_last_refresh_df, fmt)

print(formatted_curr_time, formatted_ctm_tx)
ctm_tx_diff = int((formatted_curr_time - formatted_ctm_tx).seconds / 60)
print(ctm_tx_diff)

curr_time = datetime.now().strftime('%Y%m%d%H%M%S')
print(curr_time)
