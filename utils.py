import datetime

def create_triplet(value, number_of_steps):
    entity = []
    for index in range(number_of_steps):
        entity.append(value)
    return [entity, entity, entity]

def writer(filename, mode, log):
    with open(filename, mode) as file:
        file.write(log)

def createTimestamp():
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    logFile = f"./logs/log_{timestamp}.txt"
    
    print(f"File '{logFile}' created with timestamp: {timestamp}")

    return logFile

