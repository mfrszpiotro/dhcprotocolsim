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
                    entity.queue.append(packet)
                    print(f"Mesage from {packet.source} was sent to {packet.destination}!")
                except Exception as e:
                    print(f"Message could not be sent! {str(e)}")

    def listenMessage(self, entity):
        if entity.queue:
            try:
                packet = entity.queue.pop(0)
                print(f"Entity {entity} recovered message: {packet.message} from {packet.destination}")
            except Exception as e:
                print(f"Message could not be received! {str(e)}")
            

    def print(self):
        list = []

        for entity in self.entities:
            list.append(f"Entity: {entity.name}, Queue: {entity.queue}")

        return list

    # while loop for send/listen execution, finised when no code is left to run
    def exec(self):
        pass

