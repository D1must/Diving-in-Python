class FileReader:
    def __init__(self, reading):
        self.reading = reading

    def read(self):
        try:
            with open(self.reading, "r") as f:
                return f.read()
        except OSError:
            return ""


reader = FileReader('some_file.txt')
print(reader.read())
