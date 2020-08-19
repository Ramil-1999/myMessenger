class Logger:
    def __init__(self, filename):
        self.filename = filename

    def logging(self, string):
        with open(self.filename, 'w') as f:
            f.write(string)
