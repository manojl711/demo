from datetime import datetime
import datetime as dd


# Create Job objects

class Job:
    # These counts indicate sum of every job in all the Tx control m tables (dataminer extract)
    total_jobs = 0
    # Important status of the jobs
    total_failed_jobs = 0
    total_long_running_jobs = 0
    total_not_started_jobs = 0
    total_late_started_jobs = 0
    total_completed_jobs = 0
    total_held_jobs = 0
    total_executing_jobs = 0
    total_scheduled_jobs = 0

    # Flags from Metadata table
    total_long_run_flags = 0
    total_not_started_flags = 0
    total_failed_flags = 0
    total_exclude_flags = 0

    # List of Order dates and Max odate
    odate_list = []
    max_odate = None

    def __init__(self, nodegroup, order_id, job_name, order_table,
                 odate, status, from_time, state, start_time, end_time,
                 rerun_counter, cyclic, df, c):
        # From tx_profile
        self.order_id = order_id
        self.job_name = job_name
        self.order_table = order_table
        self.nodegroup = nodegroup
        self.odate = odate
        self.status = status
        self.from_time = from_time
        self.state = state

        # Convert Start and End Time to date format
        if start_time != ' ':
            self.start_time = datetime.strptime(start_time, c.date_format1)
        else:
            self.start_time = start_time
        if end_time != ' ':
            self.end_time = datetime.strptime(end_time, c.date_format1)
        else:
            self.end_time = end_time

        self.rerun_counter = rerun_counter
        self.cyclic = cyclic

        # Issues flags - all 3 issues are mutual exclusive
        # these flags indicate current/live status
        if status in c.fail_condition:
            self.fail = True
            Job.total_failed_jobs += 1
        else:
            self.fail = False
        self.long_running = False
        self.not_started = False

        # these flags indicate overall status of the job for one complete day
        self.failed = False  # todo find logic to set it once - save in file or db
        self.long_run = False  # todo these values should not change over multiple runs
        self.late_started = False

        # calculated fields
        # self.actual_runtime = None
        if self.start_time == ' ':
            self.actual_runtime = None
        elif self.start_time != ' ' and self.end_time == ' ':
            sys_date = datetime.now()
            self.actual_runtime = round((sys_date - self.start_time).total_seconds() / 60)
        elif self.end_time != ' ':
            self.actual_runtime = round((self.end_time - self.start_time).total_seconds() / 60)

        self.run_time_diff = None
        self.new_threshold_start_time = None
        self.start_time_diff = None

        # from job metadata
        self.script_name = None
        self.description = None
        self.interface_name = None
        self.long_run_flag = None
        self.threshold_run_time = None
        self.not_started_flag = None
        self.from_time_meta = None
        self.threshold_start_time = None
        self.new_threshold_start_time = None
        self.fail_flag = None
        self.exclude_flag = None
        self.team_name = None
        self.snow_work_group = None
        self.mir3_work_group = None
        self.region = None
        self.application = None
        self.job_type = None

        # Overall health of all the jobs in control-m extract
        Job.total_jobs += 1
        if self.status in c.completed_condition:
            Job.total_completed_jobs += 1
        if self.state.strip() in c.held_condition:
            Job.total_held_jobs += 1
        if self.status in c.executing_condition:
            Job.total_executing_jobs += 1
        if self.status in c.scheduled_condition:
            Job.total_scheduled_jobs += 1

        # if self.state is '':
        #     print('Test ', self.state)

        # Odate
        if self.odate not in Job.odate_list:
            Job.odate_list.append(self.odate)
        Job.max_odate = max(Job.odate_list)

        # if self.order_id in ['4hjsf']:
        #     print(self.order_id, self.job_name, self.start_time, self.end_time, self.actual_runtime, self.state)

        # Map Metadata
        self.add_metadata(df, c)

    def add_metadata(self, df, c):
        rec = df.loc[(df.CTRLM_TABLE_NAME == self.order_table) &
                     (df.JOB_NAME == self.job_name) &
                     (df.FROM_TIME == self.from_time), :]  # df.FROM_TIME = j.from_time

        if not rec.empty:
            self.script_name = rec.SCRIPT_NAME.values[0]
            self.description = rec.DESCRIPTION.values[0]
            self.interface_name = rec.DESCRIPTION.values[0]

            if rec.CRITICAL_LONG_RUN_JOBS_FLAG.values[0] == 'Y':
                Job.total_long_run_flags += 1
                self.long_run_flag = rec.CRITICAL_LONG_RUN_JOBS_FLAG.values[0]
                self.threshold_run_time = rec.THRESHOLD_RUN_TIME.values[0]
                if self.actual_runtime:
                    self.run_time_diff = self.actual_runtime - rec.THRESHOLD_RUN_TIME.values[0]
                    if self.run_time_diff > c.buffer:
                        self.long_running = True
                        Job.total_long_running_jobs += 1

            if rec.CRITICAL_NOT_STARTED_JOBS_FLAG.values[0] == 'Y':
                Job.total_not_started_flags += 1
                # print(f'{self.order_id}, {self.from_time}, {bool(self.from_time)}, {self.job_name}')
                # if self.from_time != ' ':
                #     print(f'{self.order_id}, {self.from_time}, {rec.THRESHOLD_START_TIME.values[0]}')
                self.not_started_flag = rec.CRITICAL_NOT_STARTED_JOBS_FLAG.values[0]
                self.from_time_meta = rec.FROM_TIME.values[0]
                self.threshold_start_time = rec.THRESHOLD_START_TIME.values[0]

                # print(self.order_id,self.job_name,self.order_table,self.threshold_start_time)
                if self.threshold_start_time != ' ':
                    self.threshold_start_time = datetime.strptime(self.threshold_start_time, c.date_format2).time()
                    odate = datetime.strptime(self.odate, c.date_format3).date()
                    # print(c.midnight <= self.threshold_start_time <= c.four_oclock, c.midnight,
                    #       self.threshold_start_time, c.four_oclock)
                    if c.midnight <= self.threshold_start_time <= c.four_oclock:
                        curr_odate = odate + dd.timedelta(days=1)
                        self.new_threshold_start_time = datetime.combine(curr_odate, self.threshold_start_time)
                    else:
                        self.new_threshold_start_time = datetime.combine(odate, self.threshold_start_time)

                    if self.start_time == ' ':
                        sys_date = datetime.now()
                        self.start_time_diff = round((sys_date - self.new_threshold_start_time).total_seconds() / 60)
                    elif self.start_time != ' ':
                        self.start_time_diff = round(
                            (self.start_time - self.new_threshold_start_time).total_seconds() / 60)

                    if self.start_time == ' ' and self.start_time_diff > c.buffer:
                        self.not_started = True
                        Job.total_not_started_jobs += 1
                        # print(self.job_name, self.odate, datetime.now(),  self.start_time, self.new_threshold_start_time, self.start_time_diff)

                    if self.start_time != ' ' and self.start_time_diff > c.buffer:
                        self.late_started = True
                        Job.total_late_started_jobs += 1

            if rec.FAIL_FLAG.values[0] == 'Y':
                Job.total_failed_flags += 1
                self.fail_flag = rec.FAIL_FLAG.values[0]

            if rec.EXCLUDE_JOBS_FLAG.values[0] == 'Y':
                Job.total_exclude_flags += 1
                self.exclude_flag = rec.EXCLUDE_JOBS_FLAG.values[0]

            self.team_name = rec.TEAM_NAME.values[0]
            self.snow_work_group = rec.SNOW_WORK_GROUP.values[0]
            self.mir3_work_group = rec.MIR3_WORK_GROUP.values[0]
            self.region = rec.REGION.values[0]
            self.application = rec.APPLICATION.values[0]
            self.job_type = rec.JOB_TYPE.values[0]
