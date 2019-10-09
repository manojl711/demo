# Create table objects

class ControlMTable:
    total_tables = 0

    def __init__(self, table_name, application, region, job_type, active, description):
        # from Table_Metadata
        self.table_name = table_name
        self.application = application
        self.region = region
        self.job_type = job_type
        self.active = active
        self.description = description
        ControlMTable.total_tables += 1

        # date related fields
        self.odate_list = []
        self.max_odate = ''

        # issues count
        self.failed = 0
        self.long_run = 0
        self.not_started = 0
        self.late_started = 0

        # other stats
        self.held = 0
        self.completed = 0
        self.executing = 0
        self.scheduled = 0
        self.total = 0

        # jobs list
        self.jobs = []  # This should be a list of - type Job

        # odate specific counts
        self.o_odate = None
        self.o_failed = 0
        self.o_long_run = 0
        self.o_not_started = 0
        self.o_late_started = 0
        self.o_held = 0
        self.o_completed = 0
        self.o_executing = 0
        self.o_scheduled = 0
        self.o_total = 0

    def add_job(self, Job, c):
        self.jobs.append(Job)
        self.total += 1

        if Job.odate not in self.odate_list:
            self.odate_list.append(Job.odate)
        self.max_odate = max(self.odate_list)

        if Job.status in c.completed_condition:
            self.completed += 1
        if Job.state.strip() in c.held_condition:
            self.held += 1
        if Job.status in c.executing_condition:
            self.executing += 1
        if Job.status in c.scheduled_condition:
            self.scheduled += 1

        if Job.fail:
            self.failed += 1
        if Job.long_run:
            self.long_run += 1
        if Job.not_started:
            self.not_started += 1
        if Job.late_started:
            self.late_started += 1

    def get_counts(self, odate, c):
        self.o_odate = odate
        for j in self.jobs:
            if j.odate == odate:
                self.o_total += 1
                if j.status in c.completed_condition:
                    self.o_completed += 1
                if j.state.strip() in c.held_condition:
                    self.o_held += 1
                if j.status in c.executing_condition:
                    self.o_executing += 1
                if j.status in c.scheduled_condition:
                    self.o_scheduled += 1

                if j.fail:
                    self.o_failed += 1
                if j.long_run:
                    self.o_long_run += 1
                if j.not_started:
                    self.o_not_started += 1
                if j.late_started:
                    self.o_late_started += 1
