from flask import current_app
import utils, copy, json


class Entity:
    def __init__(self, name, max_queue_length=1):
        self.name = name
        self.queue = []
        self.max_queue_length = max_queue_length
        self.halted = False

    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Entity):
                return {
                    "__class__": "Entity",
                    "name": obj.name,
                    "queue": obj.queue,
                    "max_queue_length": obj.max_queue_length,
                    "halted": obj.halted,
                }
            elif isinstance(obj, Packet):
                return {
                    "__class__": "Packet",
                    "source": obj.source,
                    "destination": obj.destination,
                    "message": obj.message,
                }
            return super().default(obj)

    def decoder(obj):
        if "__class__" in obj:
            if obj["__class__"] == "Entity":
                entity = Entity(obj["name"], obj["max_queue_length"])
                entity.queue = obj["queue"]
                entity.halted = obj["halted"]
                return entity
            elif obj["__class__"] == "Packet":
                return Packet(obj["source"], obj["destination"], obj["message"])
        return obj


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
            confirm = f"Message '{packet.message}' could not be sent to {packet.destination}!\n"
            utils.writer(self.logfile, "a", log)

            for entity in self.entities:
                if str(entity.name) == packet.destination:
                    entity.queue.append(packet)
                    confirm = f"'{packet.message}' has been saved in ENTITY '{packet.destination}' queue;\n"
                    utils.writer(self.logfile, "a", confirm)
                    halted_content = entity.halted
                    if isinstance(halted_content, Packet):
                        if (
                            str(halted_content.source) == str(packet.source)
                            and halted_content.message == packet.message
                        ):
                            entity.halted = False
                            self.listenMessage(halted_content, entity)
                    break

            return log + confirm

    def listenMessage(self, packet, entity):
        if not entity.halted:
            entity.halted = packet
            log = f"ENTITY {packet.destination}: LISTEN '{packet.message}' FROM {packet.source};\n"
            confirm = f"Message could not be found in queue!\n"
            utils.writer(self.logfile, "a", log)

            if entity.queue:
                if str(entity.queue[0].message) == str(packet.message) and str(entity.queue[0].destination) == str(packet.destination):
                    packet = entity.queue.pop(0)
                    confirm = f"'{packet.message}' has been read from queue by ENTITY {packet.destination};\n"
                    entity.halted = False

            return log + confirm

    # obsolete
    def checkFinish(self):
        self.entites = [entity for entity in self.entities if not entity.halted]

    def terminateEntity(self, entity):
        confirm = f"ENTITY {entity.name}: END;\n"
        entity.halted = True
        utils.writer(self.logfile, "a", confirm)
        return confirm

    def translateAndExecute(self, actor_name, command):
        entity = self.getEntity(actor_name)
        if not entity:
            print(f"Entity {actor_name} not found!\n")
            return ""

        if not str(command).startswith(("SEND", "LISTEN", "SKIP", "FINISH")):
            return f"ENTITY {actor_name}: invalid command!\n"

        parts = command.split()
        action = parts[0].upper()
        message = " ".join(parts[1:-2])
        target = parts[-1][:-1]

        if action == "SEND":
            return self.sendMessage(Packet(actor_name, target, message))
        elif action == "LISTEN":
            return self.listenMessage(Packet(target, actor_name, message), entity)
        elif action == "FINISH":
            return self.terminateEntity(entity)
        elif action == "SKIP":
            pass

    # First we execute SEND actions, since it is required
    # for the proper functionality of our program
    def simulateStep(self, entity_steps):
        executedLog = ""
        for index in range(len(entity_steps)):
            entity_steps[index] = (index, entity_steps[index])

        listen_steps = copy.copy(entity_steps)
        for index in range(len(entity_steps)):
            current = entity_steps[index]
            if current[1].startswith("SEND"):
                executedLog = executedLog + str(
                    self.translateAndExecute(current[0] + 1, current[1])
                )
                listen_steps.remove(current)

        for step in listen_steps:
            executedLog = executedLog + str(
                self.translateAndExecute(step[0] + 1, step[1])
            )

        haltedList = []
        for entity in self.entities:
            if entity.halted:
                haltedList.append(entity.name)

        return executedLog, haltedList, self.entities
