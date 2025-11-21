def get_polyculture_map(enabled):
	if not enabled:
		return dict()
		
	n = get_world_size()
	map = dict()
	for i in range(n):
		for j in range(n):
			map[(i,j)] = None
	return map

def vote(map, position, vote):
	if not map[position]:
		map[position] = dict()
	
	if vote not in map[position]:
		map[position][vote] = 0
		
	map[position][vote] += 1

def get_most_voted(map, position):
	if not map[position]:
		return None
		
	qtd,entity = 0, None
	for entity in map[position]:
		if map[position][entity] > qtd:
			qtd, entity = map[position][entity], entity
	return entity
	