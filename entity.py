import datetime

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
        log = f"ENTITY {packet.source}: SEND '{packet.message}' TO {packet.destination};\n"
        writer("log.txt", "a", log)
        for entity in self.entities:
            if entity.name == packet.destination:
                try:
                    entity.queue.append(packet)
                    writer("log.txt", "a", f"{packet.message}' has been saved in ENTITY '{packet.destination}' queue;")
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


def writer(filename, mode, log):
    with open(filename, mode) as file:
        file.write(log)

def logMaker():
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"log_{timestamp}.txt"
    
    with open(file_name, "w") as file:
        file.write("")
    
    print(f"File '{file_name}' created with timestamp: {timestamp}")

    return file_name

