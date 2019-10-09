import pandas as pd
import telnetlib
import psycopg2
from controlmtable import ControlMTable
from job import Job


def extract_and_load(c):
    file_status = dataminer_ctrlm_extract(c)
    load_status = ctrlm_db_load(c)

    if file_status and load_status:
        print('Extract and Data Load completed - FuncName: extract_and_load()\n')
        return True
    else:
        print('Error encountered - extract_and_load()')
        return False


def read_file(file_info):
    df = pd.read_csv(file_info[0], sep=file_info[1], names=file_info[2], dtype=file_info[3])
    print(f'{df.shape} records loaded to dataframe from input file - {file_info[0]}')
    return df


def read_input_files(c):
    return [read_file(file) for file in c.infiles]


def dataminer_ctrlm_extract(c):
    try:
        host = c.dataminer_host
        port = c.dataminer_port
        command = c.tx_command
        tempfile = c.temp_file
        outfile = c.tx_outfile

        tn_conn = telnet_connection(host, port)
        if tn_conn:
            file_status = save_data_to_file(tn_conn, command, tempfile)
            if file_status:
                line_count = process_telnet_data(tempfile, outfile)
                print(f'{line_count} recs successfully written to "{outfile}" file\n')
        else:
            print('Telnet connection Failed')
            return False

        return True
    except Exception as error:
        print(f'Error while connecting to DataMiner and Loading data to files - {error}')
        return False


def telnet_connection(host, port):
    try:
        tn = telnetlib.Telnet(host, port)
        print(f'Telnet connection established - {tn}')
        return tn
    except Exception as error:
        print(f'Error while connecting to Telnet - {error}')
        return False


def save_data_to_file(tn, command, outfile):
    try:
        # Run command in telnet server and get data
        tn.write(command)
        tn.write(b"exit\n")
        result = tn.read_all().decode('ascii')
        tn.close()
        print('Telnet connection is closed')

        # Load data into a outfile file
        with open(outfile, "w") as f:
            f.write(result)
        print(f'Extract saved to {outfile} file')
        return True
    except Exception as error:
        print(f'Error while processing Temp file and save to {outfile} - {error}')
        return False


def process_telnet_data(infile, outfile):
    # From temp file - Remove '> ' characters and blank lines
    # And write formatted data to outfile
    line_count = 0
    with open(infile, 'r') as f1:
        with open(outfile, "w") as f2:
            for line in f1:
                line = line.replace('> ', '')
                if not line.strip():
                    continue
                f2.write(line)
                line_count += 1

    return line_count


def ctrlm_db_load(c):
    username = c.db_user
    password = c.db_password
    hostname = c.db_host
    portnum = c.db_port
    dbname = c.database

    inputfile = c.tx_inputfile
    table_name = c.tx_tablename

    conn = database_connection(username, password, hostname, portnum, dbname)
    return database_upload(conn, inputfile, table_name)


def database_connection(username, password, hostname, portnum, dbname):
    try:
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=hostname,
                                      port=portnum,
                                      database=dbname)
        print(f'Postgres DB connection established - {connection}')
        return connection
    except (Exception, psycopg2.Error) as error:
        return f"Error while connecting to PostgreSQL - {error}"


def database_upload(conn, inputfile, table_name):
    try:
        cursor = conn.cursor()
        with open(inputfile[0], 'r') as f:
            query = 'truncate table ' + table_name + ';'
            cursor.execute(query)
            cursor.copy_from(f, table_name, sep=inputfile[1])
            cursor.execute("commit;")
            print(f'{table_name} - Loaded successfully')

        sql = 'select count(*) from ' + table_name
        cursor.execute(sql)
        recs = cursor.fetchone()
    except Exception as error:
        print(f"Error while loading input file to PostgreSQL DB - {error}")
        return False
    else:
        # Closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
        print(f"Total records of {recs[0]} loaded into {table_name.upper()} table")
        return True


def create_objects(df, class_name):
    # Converts all rows in a dataframe into indivdual objects
    try:
        objs = []
        for index, row in df.iterrows():
            obj = class_name(*list(row))
            objs.append(obj)

        return objs
    except Exception as error:
        print(f'Error while creating {class_name} objects - {error}')
        return False


def create_job_objects(df, class_name, df2, c):
    # Populate jobs objects
    try:
        objs = []

        for index, row in df.iterrows():
            args = list(row)
            args.append(df2)
            args.append(c)
            obj = class_name(*args)
            objs.append(obj)

        return objs
    except Exception as error:
        print(f'Error while creating {class_name} objects - {error}')
        return False


def map_jobs_to_tables(tables, jobs, c):
    # Add jobs to respective control-m tables
    try:
        for t in tables:
            for j in jobs:
                if t.table_name == j.order_table:
                    t.add_job(j, c)
        return tables
    except Exception as error:
        print(f'Error while mapping jobs to tables - {error}')
        return False
