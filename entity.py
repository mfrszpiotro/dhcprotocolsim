import utils

class Entity:
    def __init__(self, name, max_queue_length=1):
        self.name = name
        self.queue = []
        self.max_queue_length = max_queue_length
        self.halted = False


class Packet:
    def __init__(self, source, destination, message):
        self.source = source
        self.destination = destination
        self.message = message


class Simulation:
    def __init__(self):
        self.entities = []
        self.logfile = utils.createTimestamp()

    def addEntity(self, entity):
        self.entities.insert(0, entity)

    def getEntity(self, target):
        for entity in self.entities:
            if entity.name == target:
                return entity
        return None

    def sendMessage(self, packet):
        sender = self.getEntity(packet.source)

        if not sender.halted:
            log = f"ENTITY {packet.source}: SEND '{packet.message}' TO {packet.destination};\n"
            utils.writer(self.logfile, "a", log)

            for entity in self.entities:
                if entity.name == packet.destination:
                    try:
                        entity.queue.append(packet)
                        utils.writer(self.logfile, "a", f"'{packet.message}' has been saved in ENTITY '{packet.destination}' queue;\n")
                    except Exception as e:
                        print(f"Message could not be sent! {str(e)}")

    def listenMessage(self, packet, entity):
        if not entity.halted:
            entity.halted = True
            log = f"ENTITY {packet.destination}: LISTEN '{packet.message}' FROM {packet.source};\n"
            utils.writer(self.logfile, "a", log)

            if entity.queue:
                try:
                    packet = entity.queue.pop(0)
                    log = f"'{packet.message}' has been saved in ENTITY {packet.destination} queue;\n"
                    entity.halted = False
                except Exception as e:
                    print(f"Message could not be received! {str(e)}\n")

    def checkFinish(self):
        self.entites = [entity for entity in self.entities if not entity.halted]

