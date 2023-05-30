from entity import Entity, Packet, Simulation
import utils

def test_dhcp():
    e1 = Entity(1)
    e2 = Entity(2)
    e3 = Entity(3)

    simulation = Simulation()

    simulation.addEntity(e1)
    simulation.addEntity(e2)
    simulation.addEntity(e3)

    # STEP 1
    utils.writer(simulation.logfile, "a", "\nSTEP 1\n")
    p11 = Packet(1, 3, "DHCP DISCOVER")
    p12 = Packet(2, 3, "DHCP DISCOVER")
    simulation.sendMessage(p12)
    simulation.listenMessage(p11, e3)
    # DECIDE ON THE IMPLEMENTATION IN THE LATER STAGE!
    # simulation.listenMessage(p12, e3)
    simulation.checkFinish()

    # STEP 2
    utils.writer(simulation.logfile, "a", "\nSTEP 2\n")
    p21 = Packet(3, 1, "DHCP OFFER")
    # REMEMBER THE ONE THAT HAS BEEN LISTENED IN THE STEP BEFORE
    p22 = Packet(3, 2, "DHCP OFFER")
    simulation.sendMessage(p21)
    simulation.listenMessage(p21, e1)
    simulation.listenMessage(p22, e2)
    # LOOK COMMENT ABOVE
    # simulation.listenMessage(p22, e2)
    simulation.checkFinish()

    # STEP 3
    utils.writer(simulation.logfile, "a", "\nSTEP 3\n")
    p31 = Packet(1, 3, "DHCP REQUEST")
    # LOOK COMMENTS ABOVE
    # p32 = Packet(2, 3, "DHCP REQUEST")
    simulation.sendMessage(p31)
    # simulation.sendMessage(p32)
    simulation.listenMessage(p31, e3)
    # simulation.listenMessage(p32, e3)
    simulation.checkFinish()

    # STEP 4
    utils.writer(simulation.logfile, "a", "\nSTEP 4\n")
    p41 = Packet(3, 1, "DHCP ACKNOWLEDGE")
    # LOOK COMMENTS ABOVE
    p42 = Packet(3, 2, "DHCP ACKNOWLEDGE")
    simulation.sendMessage(p41)
    simulation.sendMessage(p42)
    simulation.listenMessage(p41, e1)
    simulation.listenMessage(p42, e2)
    simulation.checkFinish()

    # STEP 5
    utils.writer(simulation.logfile, "a", "\nSTEP 5\n")
    utils.writer(simulation.logfile, "a", "ENTITY 1: END")
    # ENTITY 2 END

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

