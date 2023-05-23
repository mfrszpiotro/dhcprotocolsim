class Entity:
    def __init__(self, name, max_queue_length=1):
        self.name = name
        self.queue = []
        self.max_queue_length = max_queue_length

class Packet:
    def __init__(self, source, destination, message):
        self.source = source
        self.destination = destination
        self.message = message

class Simulation:
    def __init__(self):
        self.entities = []

    def addEntity(self, entity):
        self.entities.insert(0, entity)

    def sendMessage(self, packet):
        for entity in self.entities:
            if entity.name == packet.destination:
                try:
                    entity.queue.append(packet.message)
                    print(f"Mesage from {packet.source} was sent to {packet.destination}!")
                except Exception as e:
                    print(f"Message could not be sent! {str(e)}")

    # create listenMessage function that will pop the message from the queue
    def listenMessage(self, entity):
        if entity.queue:
            message = entity.queue.pop(0)
            print(f"Recovered message: {message}")
            

    def print(self):
        list = []
        for entity in self.entities:
            list.append(f"Entity: {entity.name}, Queue: {entity.queue}")

        return list

    # while loop for send/listen execution, finised when no code is left to run
    def exec(self):
        pass

