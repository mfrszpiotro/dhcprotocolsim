from entity import Entity, Packet, Simulation
import utils

def test_handshake():
    e1 = Entity(1)
    e2 = Entity(2)
    e3 = Entity(3)

    simulation = Simulation()

    simulation.addEntity(e1)
    simulation.addEntity(e2)
    simulation.addEntity(e3)

    # STEP 1
    utils.writer(simulation.logfile, "a", "STEP 1\n")
    p11 = Packet(1, 2, "HANDSHAKE")
    p12 = Packet(2, 3, "HANDSHAKE")
    simulation.sendMessage(p11)
    simulation.listenMessage(p11, e2)
    simulation.listenMessage(p12, e3)
    simulation.checkFinish()
    
    # STEP 2
    utils.writer(simulation.logfile, "a", "STEP 2\n")
    p21 = Packet(2, 1, "HANDSHAKE")
    p22 = Packet(3, 2, "HANDSHAKE")
    simulation.sendMessage(p21)
    simulation.sendMessage(p22)
    simulation.listenMessage(p21, e1)
    simulation.checkFinish()
    
    # STEP 3
    utils.writer(simulation.logfile, "a", "STEP 3\n")
    p31 = Packet(1, 2, "SECRET VERIFIED MESSAGE")
    simulation.sendMessage(p31)
    simulation.listenMessage(Packet(1,1,""), e2)
    simulation.listenMessage(Packet(1,1,""), e3)
    simulation.checkFinish()

    # STEP 4
    utils.writer(simulation.logfile, "a", "STEP 4\n")
    p41 = Packet(2, 1, "OK")
    simulation.sendMessage(p41)
    simulation.checkFinish()

