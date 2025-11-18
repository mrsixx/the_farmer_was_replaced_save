import drone
import structures

def just_collect_hay(position):
	drone.try_harvest()
	if get_ground_type() != Grounds.Grassland:
		till()

def plant_a_lot_of_wood(position):
	drone.try_harvest()
	choice = [Entities.Bush, Entities.Tree][position['Rank'] % 2]
	drone.plant(choice)

def wood_and_hay_just_like_astekas(position):
	chunk = position['Chunk']
	x,y = chunk['X'], chunk['Y']
	if x == y:
		just_collect_hay(position)
	else:
		plant_a_lot_of_wood(position)
		
			
def whats_up_doc(position):
	drone.try_harvest()
	
	if not drone.plant(Entities.Carrot):#if cannot plant carrots
		choice = [Entities.Tree, Entities.Grass][position['Rank'] % 2]#plant tree or grass 
		drone.plant(choice)

fila = structures.queue()
def smashing_pumpkins(position):

	def check_queue(dont_stop=False):
		if fila['size']() > num_items(Items.Carrot):
			return None
		while fila['is_not_empty']():
			cur = fila['dequeue']()
			drone.move_to(cur['X'], cur['Y'])
			is_dead = get_entity_type() == Entities.Dead_Pumpkin
			if not can_harvest():
				fila['enqueue'](cur)
				if not is_dead and not dont_stop:
					break
			if is_dead:
				drone.plant(Entities.Pumpkin)
						
	last_tile = position['Rank'] == get_world_size() ** 2
	if drone.plant(Entities.Pumpkin):
		fila['enqueue'](position)
	
	if fila['size']() > (position['Chunk']['Size'] ** 2) - 1 or last_tile:
		check_queue(last_tile)