import pandas as pd
from datetime import datetime
import datetime as dd
import numpy as np
import re
import json
import time  # todo check why this is not used
import os
from os.path import getmtime


# Methods
def read_file(file_path, sep, col_names, dtypes):
    if col_names is None:
        return pd.read_csv(file_path, sep=sep, dtype=dtypes)
    return pd.read_csv(file_path, sep=sep, names=col_names, dtype=dtypes)


def read_ctrl_m_records(mbot_settings):
    tx_ctrl_m_df = read_file(mbot_settings.tx_ctrl_m_file_path, mbot_settings.control_m_sep,
                             mbot_settings.tx_column_names, mbot_settings.dtypes)

    tx_metadata_df = read_file(mbot_settings.tx_metadata_file_path, mbot_settings.metadata_sep,
                               mbot_settings.tx_metadata_column_names, mbot_settings.dtypes)
    # ax_metadata_df = read_file(ax_metadata_file_path, metadata_sep, None) #todo have to remove ax related code

    return (tx_ctrl_m_df, tx_metadata_df)


def extract_required_cols(mbot_settings, tx_ctrl_m_df):
    tx_ctrl_m_df['SYSDATE'] = datetime.now()
    tx_ctrl_m_cols = tx_ctrl_m_df[mbot_settings.tx_selected_ctrl_m_cols]

    return tx_ctrl_m_cols


# Replace Null with Blanks
def pre_merge_formatting(mbot_settings, tx_ctrl_m_cols, tx_metadata_df):  # todo parameters can be changed
    tx_ctrl_m_cols = tx_ctrl_m_cols.replace(np.nan, ' ', regex=True)
    tx_metadata_df = tx_metadata_df.replace(np.nan, ' ', regex=True)

    return (tx_ctrl_m_cols, tx_metadata_df)


def add_custom_cols(mbot_settings, merged_df):
    # Here * unpacks the list into positional arguments
    return merged_df.reindex(columns=[*merged_df.columns.tolist(), *mbot_settings.custom_cols], fill_value=' ')


def post_merge_fill_cols(mbot_settings, merged_df):
    # Max ODATE
    max_odate = str(merged_df['ODATE'].max())
    max_odate = datetime.strptime(max_odate, mbot_settings.date_format3)
    max_odate = max_odate.date()

    # Fill Custom Cols
    for index, row in merged_df.iterrows():
        # Set Max Odate
        odate = max_odate
        if row['START_TIME'] != ' ' and row['END_TIME'] != ' ':
            # Update ACTUAL_RUN_TIME
            end_time = datetime.strptime(row['END_TIME'], mbot_settings.date_format1)
            start_time = datetime.strptime(row['START_TIME'], mbot_settings.date_format1)
            diff_in_mins = round((end_time - start_time).total_seconds() / 60)
            merged_df.loc[index, 'ACTUAL_RUN_TIME'] = diff_in_mins

            # Update RUN_TIME_DIFF
            if row['CRITICAL_LONG_RUN_JOBS_FLAG'] == 'Y' and row['STATUS'] != 'Ended Not OK':
                merged_df.loc[index, 'RUN_TIME_DIFF'] = diff_in_mins - row['THRESHOLD_RUN_TIME']

        elif row['START_TIME'] != ' ' and row['END_TIME'] == ' ':
            # Update ACTUAL_RUN_TIME
            start_time = datetime.strptime(row['START_TIME'], mbot_settings.date_format1)
            diff_in_mins = round((row['SYSDATE'] - start_time).total_seconds() / 60)
            merged_df.loc[index, 'ACTUAL_RUN_TIME'] = diff_in_mins

            # Update RUN_TIME_DIFF
            if row['CRITICAL_LONG_RUN_JOBS_FLAG'] == 'Y' and row['STATUS'] != 'Ended Not OK':
                merged_df.loc[index, 'RUN_TIME_DIFF'] = diff_in_mins - row['THRESHOLD_RUN_TIME']

        if row['CRITICAL_NOT_STARTED_JOBS_FLAG'] == 'Y' and row['THRESHOLD_START_TIME'] != ' ':
            # Update NEW_THRESHOLD_START_TIME
            th_time = datetime.strptime(row['THRESHOLD_START_TIME'], mbot_settings.date_format4)
            th_time = th_time.time()
            if mbot_settings.midnight <= th_time <= mbot_settings.four_oclock:
                odate = odate + dd.timedelta(days=1)
            merged_df.loc[index, 'NEW_THRESHOLD_START_TIME'] = datetime.combine(odate, th_time)

            # Update START_TIME_DIFF
            if row['START_TIME'] == ' ':
                diff_in_mins = round((row['SYSDATE'] - datetime.combine(odate, th_time)).total_seconds() / 60)
                merged_df.loc[index, 'START_TIME_DIFF'] = diff_in_mins

            # Update START_TIME_DIFF
            if row['START_TIME'] != ' ':
                start_time = datetime.strptime(row['START_TIME'], mbot_settings.date_format1)
                diff_in_mins = round((start_time - datetime.combine(odate, th_time)).total_seconds() / 60)
                merged_df.loc[index, 'START_TIME_DIFF'] = diff_in_mins

        (region, job_type, work_group) = tuple(mbot_settings.ctrl_m_region_map.get(row['ORDER_TABLE'], 'Not Found'))
        merged_df.loc[index, 'APPLICATION'] = 'TX'  # todo remember to replace AX for Ax job
        merged_df.loc[index, 'REGION'] = region
        merged_df.loc[index, 'JOB_TYPE'] = job_type
        merged_df.loc[index, 'DM_WORK_GROUP'] = work_group

    return merged_df


# Finds issues and write into alerts_df
def diagnose_batch_jobs(mbot_settings, merged_df, alerts_df):
    for index, row in merged_df.iterrows():
        # Max ODATE
        max_odate = merged_df['ODATE'].max()

        # CHECKS
        failed = row['STATUS'] == 'Ended Not OK' and row['EXCLUDE_JOBS_FLAG'] != 'Y' and row['ODATE'] == max_odate

        longrun = row['STATUS'] == 'Executing' and row['EXCLUDE_JOBS_FLAG'] != 'Y' and row['ODATE'] == max_odate and \
                  row['CRITICAL_LONG_RUN_JOBS_FLAG'] == 'Y' and row['RUN_TIME_DIFF'] > mbot_settings.buffer

        notstarted = row['STATUS'] != 'Ended OK' and row['EXCLUDE_JOBS_FLAG'] != 'Y' and row['ODATE'] == max_odate and \
                     row['CRITICAL_NOT_STARTED_JOBS_FLAG'] == 'Y' and row['STATUS'] != 'Held' and \
                     row['START_TIME'] == ' ' and row['START_TIME_DIFF'] > mbot_settings.buffer

        latestart = row['CRITICAL_NOT_STARTED_JOBS_FLAG'] == 'Y' and row['START_TIME'] != ' ' and \
                    row['EXCLUDE_JOBS_FLAG'] != 'Y' and row['ODATE'] == max_odate and \
                    row['START_TIME_DIFF'] > mbot_settings.buffer

        # Set FLAGS
        if failed:
            merged_df.loc[index, 'FAILED'] = 'Y'
            # Here the check should be for 'ALERTED' == 'Y'
            # check if alert is present in alerts_tst.csv file, if not then write the record
            chk = ((alerts_df['ALERTED'] == 'Y') &
                   (alerts_df['ORDER_ID'] == row['ORDER_ID']) &
                   (alerts_df['ODATE'] == row['ODATE']) &
                   (alerts_df['ISSUE_TYPE'] == 'FAILED') &
                   (alerts_df['JOB_NAME'] == row['JOB_NAME']) &
                   (alerts_df['ORDER_TABLE'] == row['ORDER_TABLE']) &
                   (alerts_df['INTERFACE_NAME'] == row['INTERFACE_NAME']) &
                   (alerts_df['REGION'] == row['REGION']) &
                   (alerts_df['APPLICATION'] == row['APPLICATION']) &
                   (alerts_df['JOB_TYPE'] == row['JOB_TYPE']) &
                   (alerts_df['DM_WORK_GROUP'] == row['DM_WORK_GROUP'])
                   ).any()
            if not chk:
                alerts_df = alerts_df.append({'ALERT_TIMESTAMP': datetime.now().strftime(mbot_settings.date_format5),
                                              'ALERTED': 'N',
                                              'ORDER_ID': row['ORDER_ID'],
                                              'ODATE': row['ODATE'],
                                              'ISSUE_TYPE': 'FAILED',
                                              'JOB_NAME': row['JOB_NAME'],
                                              'ORDER_TABLE': row['ORDER_TABLE'],
                                              'INTERFACE_NAME': row['INTERFACE_NAME'],
                                              'REGION': row['REGION'],
                                              'APPLICATION': row['APPLICATION'],
                                              'JOB_TYPE': row['JOB_TYPE'],
                                              'DM_WORK_GROUP': row['DM_WORK_GROUP']
                                              }, ignore_index=True)

        if longrun:
            merged_df.loc[index, 'LONG_RUN'] = 'Y'
            # Here the check should be for 'ALERTED' == 'Y'
            chk = ((alerts_df['ALERTED'] == 'Y') &
                   (alerts_df['ORDER_ID'] == row['ORDER_ID']) &
                   (alerts_df['ODATE'] == row['ODATE']) &
                   (alerts_df['ISSUE_TYPE'] == 'LONGRUN') &
                   (alerts_df['JOB_NAME'] == row['JOB_NAME']) &
                   (alerts_df['ORDER_TABLE'] == row['ORDER_TABLE']) &
                   (alerts_df['INTERFACE_NAME'] == row['INTERFACE_NAME']) &
                   (alerts_df['REGION'] == row['REGION']) &
                   (alerts_df['APPLICATION'] == row['APPLICATION']) &
                   (alerts_df['JOB_TYPE'] == row['JOB_TYPE']) &
                   (alerts_df['DM_WORK_GROUP'] == row['DM_WORK_GROUP'])
                   ).any()
            if not chk:
                alerts_df = alerts_df.append({'ALERT_TIMESTAMP': datetime.now().strftime(mbot_settings.date_format5),
                                              'ALERTED': 'N',
                                              'ORDER_ID': row['ORDER_ID'],
                                              'ODATE': row['ODATE'],
                                              'ISSUE_TYPE': 'LONGRUN',
                                              'JOB_NAME': row['JOB_NAME'],
                                              'ORDER_TABLE': row['ORDER_TABLE'],
                                              'INTERFACE_NAME': row['INTERFACE_NAME'],
                                              'REGION': row['REGION'],
                                              'APPLICATION': row['APPLICATION'],
                                              'JOB_TYPE': row['JOB_TYPE'],
                                              'DM_WORK_GROUP': row['DM_WORK_GROUP']
                                              }, ignore_index=True)

        if notstarted:
            merged_df.loc[index, 'NOT_STARTED'] = 'Y'
            # Here the check should be for 'ALERTED' == 'Y'
            chk = ((alerts_df['ALERTED'] == 'Y') &
                   (alerts_df['ORDER_ID'] == row['ORDER_ID']) &
                   (alerts_df['ODATE'] == row['ODATE']) &
                   (alerts_df['ISSUE_TYPE'] == 'NOTSTART') &
                   (alerts_df['JOB_NAME'] == row['JOB_NAME']) &
                   (alerts_df['ORDER_TABLE'] == row['ORDER_TABLE']) &
                   (alerts_df['INTERFACE_NAME'] == row['INTERFACE_NAME']) &
                   (alerts_df['REGION'] == row['REGION']) &
                   (alerts_df['APPLICATION'] == row['APPLICATION']) &
                   (alerts_df['JOB_TYPE'] == row['JOB_TYPE']) &
                   (alerts_df['DM_WORK_GROUP'] == row['DM_WORK_GROUP'])
                   ).any()
            if not chk:
                alerts_df = alerts_df.append({'ALERT_TIMESTAMP': datetime.now().strftime(mbot_settings.date_format5),
                                              'ALERTED': 'N',
                                              'ORDER_ID': row['ORDER_ID'],
                                              'ODATE': row['ODATE'],
                                              'ISSUE_TYPE': 'NOTSTART',
                                              'JOB_NAME': row['JOB_NAME'],
                                              'ORDER_TABLE': row['ORDER_TABLE'],
                                              'INTERFACE_NAME': row['INTERFACE_NAME'],
                                              'REGION': row['REGION'],
                                              'APPLICATION': row['APPLICATION'],
                                              'JOB_TYPE': row['JOB_TYPE'],
                                              'DM_WORK_GROUP': row['DM_WORK_GROUP']
                                              }, ignore_index=True)

        if latestart:
            merged_df.loc[index, 'LATE_START'] = 'Y'

    return (merged_df, alerts_df)


def generate_messages(mbot_settings, alerts_df):
    # Extract new alerts from alerts_df for every polling and sort them
    any_new_alerts_df = alerts_df[alerts_df.ALERTED == 'N'].sort_values(mbot_settings.sort_cols_new_alert_found)

    # todo once eveything is done, try to remove waring by pycharm that in grey-brown color .eg below line
    # AGG_LEVEL_1 : Aggregates Jobnames, Interface names and Table names based on 'ISSUE_TYPE', 'DM_WORK_GROUP', 'ODATE', 'REGION'
    agg_lvl_1 = any_new_alerts_df.groupby(['ISSUE_TYPE', 'DM_WORK_GROUP', 'ODATE', 'REGION'], as_index=False).agg(
        lambda x: ', '.join(set(x.dropna()))).sort_values(mbot_settings.sort_cols_new_alert_found)

    # Concatenate aggregated columns into simple msg
    agg_lvl_1['NEW_MSG'] = agg_lvl_1['ISSUE_TYPE'] + ' jobs are ' + agg_lvl_1['JOB_NAME'] + '(' + agg_lvl_1[
        'INTERFACE_NAME'] + ')'

    # Aggregates 'Simple msg', ISSUE_TYPE' and 'ORDER_TABLE' based on 'DM_WORK_GROUP', 'ODATE', 'REGION'
    agg_lvl_2 = agg_lvl_1.groupby(['DM_WORK_GROUP', 'ODATE', 'REGION'], as_index=False).agg(
        lambda x: ' and '.join(set(x.dropna())))[
        ['DM_WORK_GROUP', 'ODATE', 'REGION', 'ORDER_TABLE', 'APPLICATION', 'NEW_MSG'
         ]].sort_values(['ODATE', 'ORDER_TABLE'], ascending=False)

    # Get unique_id from json file
    with open(mbot_settings.unique_id_filename, 'r') as f_obj:
        unique_id = int(json.load(f_obj))

    # Removing duplicate table_names and generated Unique ID
    for index, row in agg_lvl_2.iterrows():
        words = set(re.findall(r'[^,\s]+', row['ORDER_TABLE']))
        tab_list = [i for i in words if i != 'and']
        tab_list.sort()
        agg_lvl_2.loc[index, 'ORDER_TABLE'] = ','.join(tab_list)
        print(unique_id)
        unique_id = int(unique_id) + 1
        agg_lvl_2.loc[index, 'UNIQUE_ID'] = row['DM_WORK_GROUP'] + str(unique_id)
        agg_lvl_2.loc[index, 'NEW_MSG'] = 'Date ' + str(row['ODATE']) + ', ' + row['NEW_MSG'] + ', TABLE_NAME = ' + \
                                          agg_lvl_2.loc[index, 'ORDER_TABLE'] + ', ID=' + agg_lvl_2.loc[
                                              index, 'UNIQUE_ID']

    with open(mbot_settings.unique_id_filename, 'w') as f_obj:
        json.dump(unique_id, f_obj)

    # Final message form for the issues identified, to be triggered
    return (any_new_alerts_df, agg_lvl_2)  # todo can try to give this varibable an appropriate name


def prepare_daily_alerts_log(mbot_settings):
    try:
        alerts_df = pd.read_csv(mbot_settings.alerts_log_file_path)
    except:  # todo pycharm suggestion/waring on the scroll bar
        alerts_df = pd.DataFrame(columns=mbot_settings.alerts_cols)
    alerts_df.to_csv(mbot_settings.alerts_log_file_path, index=False)

    return alerts_df


def check_between_timings(Start_Time, End_Time):
    # Start and End time
    # Convert Strings to required 'datetime format'
    formatted_Disable_Start_Time = datetime.strptime(Start_Time, '%I:%M:%S %p')  # todo replace hard code values
    formatted_Disable_End_Time = datetime.strptime(End_Time, '%I:%M:%S %p')  # todo replace hard code values

    # Get Current time
    current_time = datetime.now()
    # Convert datetime format to required 'string format'
    str_current_time = current_time.strftime('%I:%M:%S %p')  # todo replace hard code values
    # Convert String to required 'datetime format' for comparision
    formatted_Current_Time = datetime.strptime(str_current_time, '%I:%M:%S %p')  # todo replace hard code values

    # Save into variables
    curr_time = formatted_Current_Time.time()
    start_time = formatted_Disable_Start_Time.time()
    end_time = formatted_Disable_End_Time.time()

    if curr_time >= start_time and curr_time <= end_time:
        return True
    return False


# REST API connection to MIR3
def createNotif(msg_text, msg_group):
    nurl = "http://inwebservices.mir3.com/services/v1.2/mir3"
    payload = '<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://www.mir3.com/ws"> <x:Header/>     <x:Body>   <initiateNotifications xmlns="http://www.mir3.com/ws">         <apiVersion>4.7</apiVersion>         <authorization> <!-- Login credentials of the authorized user -->       <username>intuser</username>       <password>api2013</password>         </authorization>         <initiateOneNotification>       <notification>' + msg_group + '</notification>       <additionalText>' + msg_text + '</additionalText>         </initiateOneNotification>   </initiateNotifications>     </x:Body>       </x:Envelope>'

    # Uncomment below line to trigger call
    # response = requests.post(nurl, data=payload)  #todo uncomment this during PROD run, and write log entry here not in message func
    # print(response)

    print(msg_group, ' ', msg_text)  # todo remove print statements


def trigger_alert_protocol(mbot_settings, merged_df, alerts_df):
    # Generate Messages for Alerts
    (any_new_alerts_df, alert_ready_for_trigger_df) = generate_messages(mbot_settings, alerts_df)

    # Trigger Alert
    # Get Weekday  # todo test this using current day and time settings
    dt = datetime.now()
    weekday = dt.strftime("%A")  # todo remove hard coding

    call_duty_manager = True

    # Call mir3 using REST API, using for-loop
    for index, row in alert_ready_for_trigger_df.iterrows():
        msg_text = row['NEW_MSG']
        msg_grp = row['DM_WORK_GROUP']

        if weekday == 'Friday':
            if (msg_grp == 'WETX' or msg_grp == 'CETX'):  # todo remove hard coding
                dont_call = check_between_timings(mbot_settings.Disable_Start_Time,
                                                  mbot_settings.Disable_End_Time)
                if dont_call:
                    call_duty_manager = False

        # Call MIR3
        if call_duty_manager:
            createNotif(msg_text, msg_grp)
            # todo remove below log enty and write it in createNotif func along with Response code
            with open(mbot_settings.today_mbot_run_log_filename, 'a') as f_obj:
                line = '\n' + datetime.now().strftime(mbot_settings.date_format5) + \
                       ': ' + msg_text + ' ' + msg_grp
                f_obj.write(line)
            # time.sleep(10)   #TODO Remove comment for PROD run

    # Mark the alerts triggered as sent (ALERTED = 'Y') in alerts_df log file
    alerts_df.loc[alerts_df.ALERTED == 'N', 'ALERTED'] = 'Y'

    # Save data to temp files
    alerts_df.to_csv(mbot_settings.alerts_log_file_path, index=False)
    any_new_alerts_df.to_csv(mbot_settings.any_new_alerts_file_path, index=False)
    alert_ready_for_trigger_df.to_csv(mbot_settings.alert_ready_for_trigger_file_path, index=False)
    # todo test this when files are deleted and also when someone opens the file during job execution

    # Save data to log files along with timestamp by merging 3 dataframes
    # Merge 3 Dataframes - any_new_alerts_df > merged_df > alert_ready_for_trigger_df
    # using intermediate merged_and_new_alerts_df
    merged_and_new_alerts_df = pd.merge(any_new_alerts_df[mbot_settings.new_alerts_log_cols],
                                        merged_df[mbot_settings.merged_log_cols], how='left',
                                        left_on=mbot_settings.merged_and_new_alerts_join_keys,
                                        right_on=mbot_settings.merged_and_new_alerts_join_keys)

    alerts_log_df = pd.merge(merged_and_new_alerts_df, alert_ready_for_trigger_df[mbot_settings.alert_trigger_log_cols],
                             how='left', left_on=mbot_settings.alerts_log_join_keys,
                             right_on=mbot_settings.alerts_log_join_keys)

    # Write everything to ALERTS_LOG_FILE
    # When log file is deleted, create the file and write col names
    try:
        chk_any_log_file_df = pd.read_csv(mbot_settings.final_alerts_log_file_path)
    except:
        write_cols_df = pd.DataFrame(columns=mbot_settings.alerts_log_cols)
        write_cols_df.to_csv(mbot_settings.final_alerts_log_file_path, index=False)

    # When there are no records, write dataframe with header, else append records
    # NOTE: For some reason, if you just delete/clear the records in 'alerts_log_tst.csv' and run the job
    # we get Unamed cols, this is due to index. In such case delete the rows in excel instead of clearing the cells
    chk_any_log_rec_df = pd.read_csv(mbot_settings.final_alerts_log_file_path, index_col=[0])
    if chk_any_log_rec_df.empty:
        alerts_log_df.to_csv(mbot_settings.final_alerts_log_file_path, index=False)
    else:
        with open(mbot_settings.final_alerts_log_file_path, 'a') as f:
            alerts_log_df.to_csv(f, header=False, index=False)


def check_data_miner(mbot_settings):
    filename = mbot_settings.tx_ctrl_m_file_path

    last_modified_time = getmtime(filename)  # todo remove hard coding in below line
    get_ctm_tx_last_refresh_df = datetime.fromtimestamp(last_modified_time).strftime('%d-%m-%Y %H:%M:%S')

    fmt = '%d-%m-%Y %H:%M:%S'  # todo remove hard coding
    data_miner_not_working = False
    curr_time = datetime.now().strftime(fmt)

    formatted_curr_time = datetime.strptime(curr_time, fmt)
    formatted_ctm_tx = datetime.strptime(get_ctm_tx_last_refresh_df, fmt)

    ctm_tx_diff = int((formatted_curr_time - formatted_ctm_tx).seconds / 60)

    if ctm_tx_diff >= 45:
        data_miner_not_working = True

    if data_miner_not_working:
        # Have write into daily logfile
        # f = open(mbot_settings.log_filename, 'a')

        # todo remove hard coding for messages to, this requires new logic
        msg_text = 'CRITICAL!! DATA MINER FOR TX IS NOT WORKING, Last Loaded Tx = ' + str(ctm_tx_diff) + ' mins ago'
        msg_grp = 'TFM_TXAX'  # todo remove hard coding

        # todo write in generic func
        with open(mbot_settings.today_mbot_run_log_filename, 'a') as f_obj:
            line = '\n' + datetime.now().strftime(mbot_settings.date_format5) + ': ' + msg_text + ' ' + msg_grp
            f_obj.write(line)

        createNotif(msg_text, msg_grp)
        return False
    else:
        return True


def update_master_ctrl_m_log_file(mbot_settings, tx_ctrl_m_df, merged_df, master_ctrl_m_log_df):
    # Here we have to check and update master log using 2 files, one from merged ( it has max odate records)
    # the other from actual dmt records (it can contain other odate records

    print('tx_ctrl_m_df ', tx_ctrl_m_df.shape)
    print('merged_df ', merged_df.shape)
    print('master_ctrl_m_log_df ', master_ctrl_m_log_df.shape)
    print('master_ctrl_m_log_df col values ', master_ctrl_m_log_df.columns.values)

    # Extract Unique ODATE and ORDER_ID from daily ctrl_m refresh data and extract subset of Master data
    subset_master_log_df = \
        master_ctrl_m_log_df[(master_ctrl_m_log_df.ODATE.isin(merged_df['ODATE'].drop_duplicates().sort_values())) &
                             (master_ctrl_m_log_df.ORDER_ID.isin(
                                 merged_df['ORDER_ID'].drop_duplicates().sort_values()))][
            mbot_settings.tx_column_names]

    print('subset_master_log_df ', subset_master_log_df.shape)

    # For these subset_master_log (ODATE and ORDER_ID), update Master Log from Daily Log
    # Take (ODATE and ORDER_ID) that are common in both Master and Daily, UPDATE master_log with daily_log
    new_df = subset_master_log_df.merge(merged_df, indicator=True, how="left", )[
        lambda x: x._merge == 'left_only'].drop('_merge', 1)
    print('\nRecords that require UPDATES')
    print(new_df[['ODATE', 'ORDER_ID']].drop_duplicates().sort_values(by=['ODATE', 'ORDER_ID']))
    print(new_df.shape)

    # tx_ctrl_m_df['LOG_CAPTURED_TIMESTAMP'] = datetime.now()

    for index, row in new_df.iterrows():
        # Set Max Odate
        odate = row['ODATE']
        order_id = row['ORDER_ID']

        master_ctrl_m_log_df.loc[(master_ctrl_m_log_df['ODATE'] == odate) &
                                 (master_ctrl_m_log_df['ORDER_ID'] == order_id),
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
                                  'GROUP_NAME',
                                  'SYSDATE',
                                  'CTRLM_TABLE_NAME',
                                  'JOBNAME',
                                  'SCRIPT_NAME',
                                  'DESCRIPTION',
                                  'INTERFACE_NAME',
                                  'CRITICAL_LONG_RUN_JOBS_FLAG',
                                  'THRESHOLD_RUN_TIME',
                                  'CRITICAL_NOT_STARTED_JOBS_FLAG',
                                  'FROMTIME',
                                  'THRESHOLD_START_TIME',
                                  'EXCLUDE_JOBS_FLAG',
                                  'RESTATMENT_RUN_TIME',
                                  'RESTATMENT_START_TIME',
                                  'FISCAL_YEAR_END_RUN_TIME',
                                  'FISCAL_YEAR_END_START_TIME',
                                  'ACTUAL_RUN_TIME',
                                  'RUN_TIME_DIFF',
                                  'NEW_THRESHOLD_START_TIME',
                                  'START_TIME_DIFF',
                                  'LATE_START',
                                  'FAILED',
                                  'LONG_RUN',
                                  'NOT_STARTED',
                                  'REGION',
                                  'APPLICATION',
                                  'JOB_TYPE',
                                  'DM_WORK_GROUP'
                                  ]] = [datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'ELAPSED_RUNTIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'DELETE_FLAG'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'AVG_START_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'AVG_RUNTIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'TIME_ZONE'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'PRIORITY'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'CYCLIC'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'MAX_RERUN'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'END_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'START_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'FROM_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'STATUS'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'STATE'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'MEMNAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'JOB_NAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'ORDER_TABLE'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'JOB_ID'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'GROUP_NAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'SYSDATE'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'CTRLM_TABLE_NAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'JOBNAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'SCRIPT_NAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'DESCRIPTION'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'INTERFACE_NAME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df[
                                                    'ORDER_ID'] == order_id), 'CRITICAL_LONG_RUN_JOBS_FLAG'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'THRESHOLD_RUN_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df[
                                                    'ORDER_ID'] == order_id), 'CRITICAL_NOT_STARTED_JOBS_FLAG'].values[
                                            0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'FROMTIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'THRESHOLD_START_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'EXCLUDE_JOBS_FLAG'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'RESTATMENT_RUN_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'RESTATMENT_START_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'FISCAL_YEAR_END_RUN_TIME'].values[
                                            0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df[
                                                    'ORDER_ID'] == order_id), 'FISCAL_YEAR_END_START_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'ACTUAL_RUN_TIME'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'RUN_TIME_DIFF'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'NEW_THRESHOLD_START_TIME'].values[
                                            0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'START_TIME_DIFF'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'LATE_START'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'FAILED'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'LONG_RUN'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'NOT_STARTED'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'REGION'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'APPLICATION'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'JOB_TYPE'].values[0],
                                        merged_df.loc[(merged_df['ODATE'] == odate) & (
                                                merged_df['ORDER_ID'] == order_id), 'DM_WORK_GROUP'].values[0]
                                        ]

    # These Daily Log records that are extracted, should be inserted into Master_Log
    # Take (ODATE and ORDER_ID) from Daily and Insert into Master_Log
    r_new_df = merged_df.merge(subset_master_log_df, indicator=True, how="left", left_on=['ODATE', 'ORDER_ID'],
                               right_on=['ODATE', 'ORDER_ID'])[
        lambda x: x._merge == 'left_only'].drop('_merge', 1)
    print('\nRecords that should be INSERTED')
    print(r_new_df[['ODATE', 'ORDER_ID']].drop_duplicates().sort_values(by=['ODATE', 'ORDER_ID']))
    print(r_new_df.shape)

    for index, row in r_new_df.iterrows():
        odate = row['ODATE']
        order_id = row['ORDER_ID']

        master_ctrl_m_log_df = master_ctrl_m_log_df.append(
            {'LOG_CAPTURED_TIMESTAMP': datetime.now().strftime(mbot_settings.date_format5),
             'ELAPSED_RUNTIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'ELAPSED_RUNTIME'].values[0],
             'DELETE_FLAG': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'DELETE_FLAG'].values[0],
             'AVG_START_TIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'AVG_START_TIME'].values[0],
             'AVG_RUNTIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'AVG_RUNTIME'].values[0],
             'TIME_ZONE': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'TIME_ZONE'].values[0],
             'PRIORITY': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'PRIORITY'].values[0],
             'CYCLIC': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'CYCLIC'].values[0],
             'MAX_RERUN': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'MAX_RERUN'].values[0],
             'END_TIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'END_TIME'].values[0],
             'START_TIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'START_TIME'].values[0],
             'FROM_TIME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'FROM_TIME'].values[0],
             'STATUS': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'STATUS'].values[0],
             'STATE': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'STATE'].values[0],
             'ODATE': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'ODATE'].values[0],
             'MEMNAME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'MEMNAME'].values[0],
             'JOB_NAME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'JOB_NAME'].values[0],
             'ORDER_TABLE': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'ORDER_TABLE'].values[0],
             'ORDER_ID': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'ORDER_ID'].values[0],
             'JOB_ID': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'JOB_ID'].values[0],
             'GROUP_NAME': merged_df.loc[(merged_df['ODATE'] == odate) & (
                     merged_df['ORDER_ID'] == order_id), 'GROUP_NAME'].values[0]},
            ignore_index=True)

    master_ctrl_m_log_df.to_csv(mbot_settings.master_ctrl_m_log_filename, index=False)


def dataframe_anaylsis(mbot_settings, tx_ctrl_m_cols, tx_metadata_df, merged_df, alerts_df, any_new_alerts_df,
                       alert_ready_for_trigger_df):
    print('=======ANALYSIS START===========')  # todo save this code in another file as it has key pandas tricks

    print('\nSHAPE')
    print('tx_ctrl_m_cols.shape = ', tx_ctrl_m_cols.shape)
    print('tx_metadata_df.shape = ', tx_metadata_df.shape)
    print('merged_df.shape = ', merged_df.shape)
    print('alerts_df.shape = ', alerts_df.shape)
    print('any_new_alerts_df.shape = ', any_new_alerts_df.shape)
    print('alert_ready_for_trigger_df.shape = ', alert_ready_for_trigger_df.shape)

    # print('\nCOL NAMES')
    # print(merged_df.columns.values)
    print('\nmerged_df\n', merged_df.dtypes)
    print('\nalerts_df\n', alerts_df.dtypes)
    print('\nany_new_alerts_df\n', any_new_alerts_df.dtypes)
    print('\nalert_ready_for_trigger_df\n', alert_ready_for_trigger_df.dtypes)

    # print(tx_ctrl_m_cols.columns.values)
    # print(tx_metadata_df.columns.values)
    #
    # print('\nHEAD')
    # print(merged_df[['JOB_NAME','ORDER_TABLE','FROM_TIME','JOBNAME','CTRLM_TABLE_NAME','FROMTIME']].head(20))
    # print(tx_ctrl_m_cols[['JOB_NAME','ORDER_TABLE','FROM_TIME']].head(20))
    # print(tx_metadata_df[['JOBNAME','CTRLM_TABLE_NAME','FROMTIME']].head(20))

    # print(merged_df['THRESHOLD_START_TIME'].value_counts())

    print('\nOUTPUT - EXCEL')
    tx_ctrl_m_cols.to_excel('tx_tst.xlsx', index=False)
    tx_metadata_df.to_excel('meta_tst.xlsx', index=False)
    merged_df.to_excel('merge_tst.xlsx', index=False)
    alerts_df.to_csv('alerts_tst.csv', index=False)
    any_new_alerts_df.to_csv('any_new_alerts_tst.csv', index=False)
    alert_ready_for_trigger_df.to_csv('alert_ready_for_trigger_tst.csv', index=False)
    print('COMPLETED - Data written to EXCEL')

    # print('\nDataframe contents')
    # print('any_new_alerts_df\n', any_new_alerts_df.to_string())

    # To get Columns with Null Values
    # print('\nNULL Values - merged_df ')
    # null_columns = merged_df.columns[merged_df.isnull().any()]
    # # print('\nmerged_df Null Columns = ', null_columns)
    # print(merged_df[null_columns].isnull().sum())

    # print(merged_df[merged_df.FAILED == 'Y'].groupby(['FAILED']).count())

    # Multiple 'where' condition and multiple selected cols - with index off
    # print(merged_df[(merged_df.FAILED == 'Y') | (merged_df.LATE_START == 'Y') | (merged_df.LONG_RUN == 'Y') | (
    #         merged_df.NOT_STARTED == 'Y')][
    #           ['JOB_NAME', 'REGION', 'JOB_TYPE', 'FAILED', 'LATE_START', 'LONG_RUN', 'NOT_STARTED']].to_string(index=False))

    # Multiple 'where' condition and multiple selected cols
    # print(merged_df[(merged_df.FAILED == 'Y') | (merged_df.LATE_START == 'Y') | (merged_df.LONG_RUN == 'Y') | (
    #         merged_df.NOT_STARTED == 'Y')][
    #           ['JOB_NAME', 'REGION', 'JOB_TYPE', 'FAILED', 'LATE_START', 'LONG_RUN', 'NOT_STARTED']])

    # Where condn with selected cols
    # print(merged_df[merged_df.FAILED == 'Y'][['JOB_NAME','ORDER_TABLE']])

    # Group by on a col
    # print(merged_df['LATE_START'].value_counts())

    # count(*) on FAILED column where FAILED == 'Y'
    # print(int(merged_df[merged_df.FAILED == 'Y'].groupby(['FAILED']).size()))

    # Group by on a col
    # print(merged_df.groupby('ORDER_TABLE').size())

    # Distinct count of LATE_START col
    # print(merged_df['LATE_START'].nunique())

    # Group by LATE_START and give count in all cols
    # print(merged_df.groupby('LATE_START').count())

    # non-NaN values in each column
    # print(merged_df.count())

    # non-NaN values in each row
    # print(merged_df.count(axis=1))

    # Gives count of all records
    # print(merged_df[['LATE_START', 'FAILED', 'LONG_RUN', 'NOT_STARTED']].count())

    # Group by and Having condn
    # print((merged_df.groupby(['STATE', 'STATUS'], as_index=False)['STATE'].agg({'count': 'count'}).query(
    #      "STATE == ' '")))

    print('\n\n=======ANALYSIS END===========')
