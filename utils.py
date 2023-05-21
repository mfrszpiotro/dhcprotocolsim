def create_triplet(value, number_of_steps):
    entity = []
    for index in range(number_of_steps):
        entity.append(value)
    return [entity, entity, entity]

