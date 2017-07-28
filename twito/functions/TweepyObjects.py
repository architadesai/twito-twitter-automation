

class Status(object):

    def __init__(self, message, writer, writerUsername, writerProfile):

        self.message = message
        self.writer = writer
        self.writerUsername = writerUsername
        self.writerProfile = writerProfile

    def __str__(self):

        return "{} writer tweet {}".format(self.writerUsername, self.message)