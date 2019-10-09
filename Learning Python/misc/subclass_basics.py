def file_processor(reader, converter, writer):
    print('Open File using ', reader.read())
    print('Convert file using ', converter)
    print('Write File using ', writer.write())


class Reader:
    def read(self):
        return 'Default Reader'


class FileReader(Reader):
    def read(self):
        return 'FileReader'


class SocketReader(Reader):
    def read(self):
        return 'SocketReader'


class FtpReader(Reader):
    def read(self):
        return 'FtpReader'


class Writer:
    def write(self):
        return 'Default Write'


class TapeWriter(Writer):
    def write(self):
        return 'TapeWriter'


class FileWriter(Writer):
    def write(self):
        return 'FileWriter'


class NetworkWriter(Writer):
    def write(self):
        return 'NetworkWriter'


converter = 0

a = FileReader()
b = Writer()

# you call directly the Class or its Instance
# both are one and the same
file_processor(FileReader(), converter, Writer())
file_processor(a, converter, b)
print('----------')
file_processor(Reader(), converter, TapeWriter())
file_processor(SocketReader(), converter, NetworkWriter())
file_processor(FtpReader(), converter, TapeWriter())
