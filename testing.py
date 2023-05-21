from entity import Entity, Packet, Simulation

def test_communication():
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
