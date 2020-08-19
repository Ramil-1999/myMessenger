import os


class Logger:
    def __init__(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass
        self.filename = filename

    def logging(self, string):
        with open(self.filename, 'w') as f:
            f.write(string)
