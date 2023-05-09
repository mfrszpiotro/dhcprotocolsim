class Entity:
    queue = {}
    max_queue_length = 1

    def init(self, max_queue_length):
        self.max_queue_length = max_queue_length
        return

    def send(self, message, destination):
        return

    def listen(self, message, source, wait_time=None):
        return
