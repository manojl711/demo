import pandas as pd
from mj_settings import Settings
import mj_functions as mbot
import time
import os
from datetime import datetime

# Measure time (For performance)
start = time.time()  # todo Remove this code during PROD run

# Set Env of M-Bot
mbot_settings = Settings()

# Outside infinite for loop
# By default it will be considered as new run
# And all prerequisites should be met/initialized here

# Creating Daily Log file and Write First Line with Timestamp
mbot_settings.today_mbot_run_log_filename = mbot_settings.daily_mbot_run_log_filename + \
                                            datetime.now().strftime(mbot_settings.date_format1) + '.txt'
# todo try to create a generic function to write daily run logs
with open(mbot_settings.today_mbot_run_log_filename, 'a+') as f_obj:
    line = '\n' + datetime.now().strftime(mbot_settings.date_format5) + ': Program Started, Before Infinite Loop'
    f_obj.write(line)

# Clearing Daily_Alerts file
f = open(mbot_settings.alerts_log_file_path, "w+")
f.close()

# Infinite loop starts
while True:
    # Check Time between 3:55 AM and 04:10 AM
    reset = mbot.check_between_timings(mbot_settings.Reset_Start_Time, mbot_settings.Reset_End_Time)
    if reset:
        # Creating Daily Log file and Writing First Line with Timestamp
        mbot_settings.today_mbot_run_log_filename = mbot_settings.daily_mbot_run_log_filename + \
                                                    datetime.now().strftime(mbot_settings.date_format1) + '.txt'
        # todo add to generic func
        with open(mbot_settings.today_mbot_run_log_filename, 'a+') as f_obj:
            line = '\n' + datetime.now().strftime(mbot_settings.date_format5) + ': New Day Run Started, Initialization'
            f_obj.write(line)

        # Clearing Daily_Alerts file
        f = open(mbot_settings.alerts_log_file_path, "w+")
        f.close()

        # If any file should be cleared, do it here
        # todo find files that qualifies here

        # Sleep for 25 mins (ctrl -refresh is in progress)
        # time.sleep(25)  # todo uncomment this during PROD run

    # Read control-m details using telnet (this should be outside reset scope.
    # Load data into .txt file #todo call dataminer load function

    # Check whether Data Miner is working or not
    data_miner = True
    data_miner = mbot.check_data_miner(mbot_settings)

    if data_miner:
        # Read Files Ctrl_M and Metadata records
        # Make sure metadata table has FROM_TIME in the format 0005 and not 5
        # todo add this formatting instruction in the document
        (tx_ctrl_m_df, tx_metadata_df) = mbot.read_ctrl_m_records(mbot_settings)

        # Extract required columns
        tx_ctrl_m_cols = mbot.extract_required_cols(mbot_settings, tx_ctrl_m_df)

        # Pre-Merge Data Formatting
        (tx_ctrl_m_cols, tx_metadata_df) = mbot.pre_merge_formatting(mbot_settings, tx_ctrl_m_cols, tx_metadata_df)

        # Merge Control_M and Metadata
        # todo this is original code which used limited cols
        # merged_df = pd.merge(tx_ctrl_m_cols, tx_metadata_df, how='left', left_on=mbot_settings.tx_ctrl_m_join_keys,
        #                      right_on=mbot_settings.tx_metadata_join_keys)

        # this uses all cols, changed tx_ctrl_m_cols to tx_ctrl_m_df
        merged_df = pd.merge(tx_ctrl_m_df, tx_metadata_df, how='left', left_on=mbot_settings.tx_ctrl_m_join_keys,
                             right_on=mbot_settings.tx_metadata_join_keys)

        # Concatenate New Columns to store Calculated values
        merged_df = mbot.add_custom_cols(mbot_settings, merged_df)

        # Post Merge Data Formatting
        merged_df = mbot.post_merge_fill_cols(mbot_settings, merged_df)

        # Prepare daily alerts_log file
        # Make sure 'alerts_tst.csv' file is empty for a fresh run. It should not have any headers
        # alerts_df : this dataframe should get refreshed every start of the run
        # todo add this bug/risk in document
        alerts_df = mbot.prepare_daily_alerts_log(mbot_settings)

        # Find Issues in Batch Jobs (DIAGNOSE BATCH JOBS)
        (merged_df, alerts_df) = mbot.diagnose_batch_jobs(mbot_settings, merged_df, alerts_df)

        # Check any new alerts found
        new_alerts_found = len(alerts_df[alerts_df.ALERTED == 'N'].index)

        # Here the count should be written to log file along with timestamp
        # todo add this to generic func, this should be called in next if statement (trigger_alert_protocol)
        with open(mbot_settings.today_mbot_run_log_filename, 'a') as f_obj:
            line = '\n' + datetime.now().strftime(mbot_settings.date_format5) + ': Issues Found = ' \
                   + str(new_alerts_found)
            f_obj.write(line)
        print('\nNew Issues Found = ', new_alerts_found)

        if new_alerts_found:
            mbot.trigger_alert_protocol(mbot_settings, merged_df, alerts_df)

        # todo master log entry logic to be added here
        # # Update merge data to file and Read Master Log File
        # merged_df.to_excel('merge_tst.xlsx', index=False)
        # write to .csv
        merged_df.to_csv('merge_tst.csv', index=False)
        # master_ctrl_m_log_df = pd.read_csv(mbot_settings.master_ctrl_m_log_filename, sep=mbot_settings.metadata_sep, dtype=mbot_settings.dtypes)
        # # Update Master Log file
        # master_ctrl_m_log_df = mbot.update_master_ctrl_m_log_file(mbot_settings, tx_ctrl_m_df, merged_df, master_ctrl_m_log_df)

        # if (any changes to ctrl_m file - be it update or insert)
        #     do
        #     it
        #     here
        #     to
        #     Master
        #     Log
        #     file

    #################################################################################################

    # Prepare script for Ax jobs  # todo other todo stuff, but setting up for Ax is critical

    # Additional Features
    # Friday No Alerts Logic - completed  # todo this should be tested by changing values to current day and time
    # Other functionalities present in Current system
    # Handle Diff Th Values (Daily, Monthly, Weekend for same job)
    # Days Logic (1,2,3,4,5,6,7) (Daily, Monthly, Weekend for same job)
    # Different Shifts based on Sysdate
    # Alert Inbound and Outbound Files (Create separate program for Files as this is exclusively for Batch Monitoring)

    ######################### TESTING SPACE #########################################################

    #################################################################################################

    # mbot.dataframe_anaylsis(mbot_settings, tx_ctrl_m_cols, tx_metadata_df, merged_df, alerts_df, any_new_alerts_df,
    #                         alert_ready_for_trigger_df)

    # todo remove all the below code
    print('\n\nProgram Ended')
    end = time.time()
    print('Elapsed Time = {:.2f}s'.format(end - start))

    key_press = input('\nFor continue press y, else press any other key = ')
    start = time.time()
    if key_press != 'y':
        break

print('\n\nExit from Program')
# todo need to populate Interface Names for both Tx and Ax Metadata files - save the files with 0000 format
# todo make sure you have covered all logic present in PL/SQL, Unix and Python in old version
