import datetime

class Entity:
    def __init__(self, name, max_queue_length=1):
        self.name = name
        self.queue = []
        self.max_queue_length = max_queue_length
        #self.halted = false


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

    # check if halted, proceed only if false
    def sendMessage(self, packet, logfile):
        log = f"ENTITY {packet.source}: SEND '{packet.message}' TO {packet.destination};\n"
        writer(logfile, "a", log)
        for entity in self.entities:
            if entity.name == packet.destination:
                try:
                    entity.queue.append(packet)
                    writer(logfile, "a", f"'{packet.message}' has been saved in ENTITY '{packet.destination}' queue;\n")
                except Exception as e:
                    #TOBECHANGED
                    print(f"Message could not be sent! {str(e)}")

   # def listenMessage(self, entity, logfile):
   #     #entity.halted = true
   #     log = f"ENTITY {entity.name}: LISTEN '{packet.message}' FROM {packet.destination};\n"
   #     if entity.queue:
   #         try:
   #             packet = entity.queue.pop(0)
   #             writer(logfile, "a", log)
   #             #entity.halted = false
   #         except Exception as e:
   #             #TOBECHANGED
   #             #when halted 
   #             print(f"Message could not be received! {str(e)}\n")

    def listenMessage(self, packet, entity, logfile):
        #entity.halted = true
        log = f"ENTITY {packet.destination}: LISTEN '{packet.message}' FROM {packet.source};\n"
        writer(logfile, "a", log)
        if entity.queue:
            try:
                packet = entity.queue.pop(0)
                #entity.halted = false
            except Exception as e:
                #TOBECHANGED
                #when halted 
                print(f"Message could not be received! {str(e)}\n")

    # if required action is issued later, but still in the same state, accept it
    def checkFinish(self):
        pass

    def print(self):
        list = []

        for entity in self.entities:
            list.append(f"Entity: {entity.name}, Queue: {entity.queue}")

        return list


def writer(filename, mode, log):
    with open(filename, mode) as file:
        file.write(log)

def createTimestamp():
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"./logs/log_{timestamp}.txt"
    
    print(f"File '{file_name}' created with timestamp: {timestamp}")

    return file_name

