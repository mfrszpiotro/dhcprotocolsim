from entity import Entity, Packet, Simulation, createTimestamp, writer

def test_handshake():
    e1 = Entity(1)
    e2 = Entity(2)
    e3 = Entity(3)

    simulation = Simulation()
    logfile = createTimestamp()

    simulation.addEntity(e1)
    simulation.addEntity(e2)
    simulation.addEntity(e3)

    # STEP 1
    writer(logfile, "a", "STEP 1\n")
    p11 = Packet(1, 2, "HANDSHAKE")
    p12 = Packet(2, 3, "HANDSHAKE")
    simulation.sendMessage(p11, logfile)
    simulation.listenMessage(p11, e2, logfile)
    simulation.listenMessage(p12, e3, logfile)
    simulation.checkFinish()
    
    # STEP 2
    writer(logfile, "a", "STEP 2\n")
    p21 = Packet(2, 1, "HANDSHAKE")
    p22 = Packet(3, 2, "HANDSHAKE")
    simulation.sendMessage(p21, logfile)
    simulation.sendMessage(p22, logfile)
    simulation.listenMessage(p21, e1, logfile)
    simulation.checkFinish()
    
    # STEP 3
    writer(logfile, "a", "STEP 3\n")
    p31 = Packet(1, 2, "SECRET VERIFIED MESSAGE")
    simulation.sendMessage(p31, logfile)
    simulation.listenMessage(Packet(1,1,""), e2, logfile)
    simulation.listenMessage(Packet(1,1,""), e3, logfile)
    simulation.checkFinish()

    # STEP 4
    writer(logfile, "a", "STEP 4\n")
    p41 = Packet(2, 1, "OK")
    simulation.sendMessage(p41, logfile)
    simulation.checkFinish()


def test_2entity_communication():
    # Example of message sending
    e1 = Entity(1)
    e2 = Entity(2)
    
    simulation = Simulation()
    
    simulation.addEntity(e1)
    simulation.addEntity(e2)
    
    p1 = Packet(1, 2, "there is no try")
    simulation.sendMessage(p1)
    
    p2 = Packet(2, 1, "do or do not")
    simulation.sendMessage(p2)
    
    p3 = Packet(2, 1, "or have a donut")
    simulation.sendMessage(p3)
    
    p4 = Packet(2, 1, "or be gone")
    simulation.sendMessage(p4)
    
    # Exemplary listen message
    simulation.listenMessage(e1)
    
    return simulation

def test_3entity_communication():
    # Example of message sending
    e1 = Entity(1)
    e2 = Entity(2)
    e3 = Entity(3)
    
    simulation = Simulation()

    logfile = createTimestamp()
    print(logfile)
    
    simulation.addEntity(e1)
    simulation.addEntity(e2)
    simulation.addEntity(e3)
    
    p1 = Packet(1, 2, "one to two")
    simulation.sendMessage(p1, logfile)
    
    p1 = Packet(2, 3, "two to three")
    simulation.sendMessage(p1, logfile)

    p1 = Packet(3, 1, "three to one")
    simulation.sendMessage(p1, logfile)

    p1 = Packet(2, 1, "two to one")
    simulation.sendMessage(p1, logfile)

    p1 = Packet(3, 2, "three to two")
    simulation.sendMessage(p1, logfile)

    p1 = Packet(1, 3, "one to three")
    simulation.sendMessage(p1, logfile)
    
    # Exemplary listen message
    simulation.listenMessage(e1, logfile)
    simulation.listenMessage(e2, logfile)
    simulation.listenMessage(e3, logfile)
    
    return simulation
