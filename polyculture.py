import drone
def compute_votes(drones_votes):
	map = get_polyculture_map(True)
	for drone_votes in drones_votes:
		for tile in drone_votes:
			entity, position  = drone_votes[tile]
			vote(map, position, entity)
	return map
	
def get_polyculture_map(enabled):
	if not enabled:
		return dict()
		
	n = get_world_size()
	map = dict()
	for i in range(n):
		for j in range(n):
			map[(i,j)] = None
	return map

def vote(map, position, entity):
	if not map[position]:
		map[position] = dict()
	
	if entity not in map[position]:
		map[position][entity] = 0
		
	map[position][entity] += 1

def get_most_voted(map, position):
	coord = position['coord']
	if not map[coord]:
		return None
		
	qtd,entity = 0, None
	for entity in map[coord]:
		if map[coord][entity] > qtd:
			qtd, entity = map[coord][entity], entity
	return entity

def apply_votes(votes):
	def the_edge_of_democracy(position):
		most_voted = get_most_voted(votes, position)

		if most_voted and get_entity_type() != most_voted:
			drone.try_harvest()
			drone.plant(most_voted)

	return the_edge_of_democracy