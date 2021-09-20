import os.path
import tempfile
import uuid


class File:
    def __init__(self, _path):
        # Initialisation of path
        self.path = _path
        # self._current = 0
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def read(self):
        with open(self.path, "r") as f:
            return f.read()

    def write(self, data):
        print(len(str(data)))
        with open(self.path, "w") as f:
            return f.write(data)

    def __add__(self, second):
        # string summation
        newpath = os.path.join(tempfile.gettempdir(), str(uuid.uuid4().hex))
        newfile = type(self)(newpath)
        newfile.write(self.read() + second.read())
        return newfile

    def __iter__(self):
        self.current = 0
        with open(self.path, "r") as f:
            self.strings = f.readlines()
        return self

    def __next__(self):
        try:
            string = self.strings[self.current]
            self.current = self.curent + 1
            return string
        except Exception:
            raise StopIteration

    def __str__(self):
        return self.path
