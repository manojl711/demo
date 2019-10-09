# Connect to control-m telnet server and extract Control M table details to file
import telnetlib


def ctrlm_extract(c):
    try:
        host = c.telnet_host
        port = c.telnet_port
        command = c.tx_command
        outfile = c.tx_outfile

        tn = telnetlib.Telnet(host, port)
        print(f'Telnet connection established - {tn}')
        # Run command in telnet server and get data
        tn.write(command)
        tn.write(b"exit\n")
        result = tn.read_all().decode('ascii')

        # Load data into a temp file
        f = open('temp.txt', 'w')
        f.write(result)
        f.close()

        # From temp file - Remove '> ' characters and blank lines
        # And write formatted data to outfile
        line_count = 0
        with open('temp.txt', 'r') as f1:
            with open(outfile, "w") as f2:
                for line in f1:
                    line = line.replace('> ', '')
                    if not line.strip():
                        continue
                    f2.write(line)
                    line_count += 1
    except Exception as error:
        tn.close()
        print('Telnet connection is closed')
        return f'Error while connecting to Dataminer and Loading data to files - {error}'
    else:
        tn.close()
        print('Telnet connection is closed')
        return f'{line_count} recs successfully written to "{outfile}" file'
