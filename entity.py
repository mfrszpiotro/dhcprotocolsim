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
                    log = f"ENTITY {packet.source}: SEND '{packet.message}' TO {packet.destination};\n"
                    writer("log.txt", "a", log)
                except Exception as e:
                    print(f"Message could not be sent! {str(e)}")

    def listenMessage(self, entity):
        if entity.queue:
            try:
                packet = entity.queue.pop(0)
                log = f"ENTITY {entity.name}: LISTEN '{packet.message}' FROM {packet.destination};\n"
                writer("log.txt", "a", log)
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

def writer(filename, mode, log):
    with open(filename, mode) as file:
        file.write(log)

