from config import Settings
import mbot_functions
from datetime import datetime
from controlmtable import ControlMTable
from job import Job

# Monitoring Bot for Tx jobs

if __name__ == '__main__':
    try:
        c = Settings()
        print('Start @ ', datetime.now().strftime(c.date_format))

        # Extract from DataMiner and save into File and  Table
        df_list = []
        if mbot_functions.extract_and_load(c):
            # Load all Input Flat files into a List of Dataframes
            df_list = mbot_functions.read_input_files(c)
            df_list[2].loc[df_list[2].FROM_TIME.isnull(), 'FROM_TIME'] = ' '  # todo remove hard coded values
            df_list[1]['STATE'] = df_list[1]['STATE'].fillna(' ')
            print(f'{len(df_list)} Input files read successfully - FuncName: read_input_files()\n')

        print(datetime.now().strftime(c.date_format))

        # Create table objects
        active_tables_df = df_list[0].loc[df_list[0].Active == 'Y']
        tabs = mbot_functions.create_objects(active_tables_df, ControlMTable)
        print(f'Total table objects created - {ControlMTable.total_tables}')

        print('\n', datetime.now().strftime(c.date_format))

        # dataminer = df_list[1]
        # jobs_meta = df_list[2]
        # for index, dm_row in dataminer.iterrows():
        #     for index, m_row in jobs_meta.iterrows():
        #         if dm_row['JOB_NAME'] == m_row['JOB_NAME'] and dm_row['ORDER_TABLE'] == m_row['CTRLM_TABLE_NAME']:
        #             print(dm_row['ORDER_ID'], dm_row['FROM_TIME'], m_row['FROM_TIME'], m_row['SCRIPT_NAME'])

        # Create job objects
        jobs = mbot_functions.create_job_objects(df_list[1], Job, df_list[2], c)

        # Once all job objects are created, Get overall health of Tx jobs (includes all tables)
        print(f'Total job objects created - {Job.total_jobs}')
        print(f'Total jobs in Failed status - {Job.total_failed_jobs}')
        print(f'Total jobs in Long Running status - {Job.total_long_running_jobs}')
        print(f'Total jobs in Not Started status - {Job.total_not_started_jobs}')
        print(f'Total jobs in Late Started status - {Job.total_late_started_jobs}')
        print(f'Total jobs in Completed status - {Job.total_completed_jobs}')
        print(f'Total jobs in Hold status - {Job.total_held_jobs}')
        print(f'Total jobs in Executing status - {Job.total_executing_jobs}')
        print(f'Total jobs in Scheduled status - {Job.total_scheduled_jobs}')
        print()
        print(f'Total jobs with Long Run Flag as Y - {Job.total_long_run_flags}')
        print(f'Total jobs with Not Started Flag as Y - {Job.total_not_started_flags}')
        print(f'Total jobs with Fail Flag as Y - {Job.total_failed_flags}')
        print(f'Total jobs with Exclude Job Flag as Y - {Job.total_exclude_flags}')
        print()
        print(f'List of ODATEs - {Job.odate_list}')
        print(f'Max ODATE - {Job.max_odate}')

        print('\n', datetime.now().strftime(c.date_format))

        # Map job objects to table objects
        tabs = mbot_functions.map_jobs_to_tables(tabs, jobs, c)

        print('\n', datetime.now().strftime(c.date_format))

        # Get counts based on control-m table
        print('\nTable_Name - Total - Held - Completed - Executing - Scheduled - Odate_List - Max_Odate - Failed '
              '- Long_Running - Not_Started - Late_Started')
        for t in tabs:
            print(
                f'{t.table_name} - {t.total} - {t.held} - {t.completed} - {t.executing} - {t.scheduled} - '
                f'{t.odate_list} - {t.max_odate} - {t.failed} - {t.long_run} - {t.not_started} - {t.late_started}')

        # Get counts based on odate
        for t in tabs:
            t.get_counts(t.max_odate, c)  # Here we can pass any odate to get respective counts

        print('\nTable_Name - Server - Odate - Failed - Long_Running - Not_Started - Late_Started - '
              'Held - Completed - Executing - Scheduled - Total')

        # This where we can store the counts to dataframe/file/excel/database
        for t in tabs:
            print(
                f'{t.table_name} - {t.job_type} - {t.o_odate} - {t.o_failed} - {t.o_long_run} - {t.o_not_started} - '
                f'{t.o_late_started} - {t.o_held} - {t.o_completed} - {t.o_executing} - {t.o_scheduled} - {t.o_total}')







    except Exception as error:
        print(f'Error in Main function - {error}')
    finally:
        pass
        # close all connection here
