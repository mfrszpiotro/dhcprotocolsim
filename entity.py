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
        self.entities.append(entity)

    def sendMessage(self, packet):
        for entity in self.entities:
            if entity.name == packet.destination:
                entity.queue.append(packet.message)

    #def listenMessage(self, entity): #wait_time=None):
    #    while True:
    #        print("works")
    #        if entity.queue:
    #            message = entity.queue.pop(0)
    #            print(f"Recovered message: {message}")
    #            break

    def print(self):
        list = []
        for entity in self.entities:
            list.append(f"Entity: {entity.name}, Queue: {entity.queue}")

        return list

    # while loop for send/listen execution, finised when no code is left to run
    def exec(self):
        pass

