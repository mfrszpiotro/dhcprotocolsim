from flask import current_app
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
            if str(entity.name) == str(target):
                return entity
        return None

    def sendMessage(self, packet):
        sender = self.getEntity(packet.source)

        if not sender.halted:
            log = f"ENTITY {packet.source}: SEND '{packet.message}' TO {packet.destination};\n"
            confirm = f"Message '{packet.message}' could not be sent to {packet.destination}!"
            utils.writer(self.logfile, "a", log)

            for entity in self.entities:
                if str(entity.name) == packet.destination:
                    entity.queue.append(packet)
                    confirm = f"'{packet.message}' has been saved in ENTITY '{packet.destination}' queue;\n"
                    utils.writer(self.logfile, "a", confirm)

            return log + '\n' + confirm

    def listenMessage(self, packet, entity):
        if not entity.halted:
            entity.halted = True
            log = f"ENTITY {packet.destination}: LISTEN '{packet.message}' FROM {packet.source};\n"
            confirm = f"Message could not be received!"
            utils.writer(self.logfile, "a", log)

            if entity.queue:
               if entity.queue(0).message == packet.message:
                   packet = entity.queue.pop(0)
                   confirm = f"'{packet.message}' has been obtained by ENTITY {packet.destination} queue;\n"
                   entity.halted = False

            return log + "\n" + confirm

    def checkFinish(self):
        self.entites = [entity for entity in self.entities if not entity.halted]

    def terminateEntity(self, entity_name):
        entity = self.getEntity(entity_name)
        if entity:
            entity.halted = True
            utils.writer(self.logfile, "a", f"Entity {entity_name} END;\n")
        else:
            print(f"Entity {entity_name} not found!\n")

    def translateAndExecute(self, actor_name, command):
        parts = command.split()
        action = parts[0].upper()
        message = ' '.join(parts[1:-2])
        target = parts[-1][:-1]

        if not self.getEntity(actor_name):
            print(f"Entity {actor_name} not found!\n")
            return ""

        if action == 'SEND':
            packet = Packet(actor_name, target, message)
            return self.sendMessage(packet)
        elif action == 'LISTEN':
            packet = Packet(target, actor_name, message)
            return self.listenMessage(packet, self.getEntity(actor_name))


    # First we execute SEND actions, since it is required 
    # for the proper functionality of our program
    def simulateStep(self, entity_steps):
        executedLog = ""

        for index in range(len(entity_steps)):
            print(index)
            current = entity_steps[index]
            if current.startswith("SEND"):
                executedLog = executedLog + str(self.translateAndExecute(self.getEntity(index+1), current))
                entity_steps.pop(index)

        for index in range(len(entity_steps)):
            current = entity_steps[index]
            if current.startswith("LISTEN"):
                executedLog = executedLog + str(self.translateAndExecute(self.getEntity(index+1), current))
                entity_steps.pop(index)
        
        haltedList = []
        for entity in self.entities:
            if entity.halted:
                haltedList.append(entity.name)

        return executedLog, haltedList

