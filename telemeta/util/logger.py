
class Logger:
    "Provide simple message logging"

    filename="/tmp/telemeta.log"

    def __init__(self):
        self.file = open(self.filename, "a")

    def debug(self, msg):
        self.file.write(msg + "\n")
        self.file.flush()
        
