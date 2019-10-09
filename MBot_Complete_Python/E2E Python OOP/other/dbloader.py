import psycopg2


def db_load(c):
    try:
        username = c.db_user
        password = c.db_password
        hostname = c.db_host
        portnum = c.db_port
        dbname = c.database
        inputfile = c.tx_inputfile
        table_name = c.tx_tablename

        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=hostname,
                                      port=portnum,
                                      database=dbname)
        print(f'Postgres DB connection established - {connection}')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        return f"Error while connecting to PostgreSQL - {error}"
    try:
        with open(inputfile[0], 'r') as f:
            query = 'truncate table ' + table_name + ';'
            cursor.execute(query)
            cursor.copy_from(f, table_name, sep=inputfile[1])
            cursor.execute("commit;")
            f'{table_name} - Loaded successfully'

        sql = 'select count(*) from ' + table_name
        cursor.execute(sql)
        recs = cursor.fetchone()
    except Exception as error:
        return f"Error while loading input file to PostgreSQL DB - {error}"
    else:
        return f"Total records {recs[0]} loaded into {table_name.upper()} table"
    finally:
        # Closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
