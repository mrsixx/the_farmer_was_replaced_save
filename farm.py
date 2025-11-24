import drone
import inventory
import visitor
import structures
import algorithms
import polyculture
import maze

def hay(enable_polyculture=True):
	def sow_field(position):
		x,y = position['coord']
		drone.try_harvest()
		drone.plant(Entities.Grass)

		if enable_polyculture:
			return get_companion()
		return None
		
	change_hat(Hats.Straw_Hat)
	votes = visitor.parallel_cols(sow_field, max_drones())
	computed = polyculture.compute_votes(votes)
	if enable_polyculture:
		visitor.parallel_cols(polyculture.apply_votes(computed), max_drones())
		drone.clear_only({ Entities.Grass })
	drone.clear()
	
def wood(enable_polyculture=True):

	def plant_a_lot_of_wood(position):
		drone.try_harvest()
		x,y = position['coord']
		wich = x % 2 == y % 2
		choice = [Entities.Bush, Entities.Tree][wich]
		drone.plant(choice)

		if enable_polyculture:
			return get_companion()
		return None
	
	change_hat(Hats.Tree_Hat)
	votes = visitor.parallel_cols(plant_a_lot_of_wood, max_drones())
	computed = polyculture.compute_votes(votes)
	if enable_polyculture:
		visitor.parallel_cols(polyculture.apply_votes(computed), max_drones())
		drone.clear_only({Entities.Bush, Entities.Tree})
	drone.clear()
	
def carrots(enable_polyculture=True):
	votes = polyculture.get_polyculture_map(enable_polyculture)
	n = get_world_size()
	if	not inventory.has_enought_to_produce(Entities.Carrot, (n**2)):
		quick_print('Canot produce carrots')
		return None
		
	def whats_up_doc(position):
		x,y = position['coord']
		drone.try_harvest()
		drone.plant(Entities.Carrot)

		if enable_polyculture:
			return get_companion()
		
	change_hat(Hats.Wizard_Hat)

	votes = visitor.parallel_rows(whats_up_doc, max_drones())
	computed = polyculture.compute_votes(votes)
	if enable_polyculture:
		visitor.parallel_cols(polyculture.apply_votes(computed), max_drones())
		drone.clear_only({ Entities.Carrot })
	drone.clear()
	
def pumpkins():
	n = get_world_size()
	if	not inventory.has_enought_to_produce(Entities.Pumpkin, 1.5 * (n**2)):
		quick_print('Canot produce pumpkins')
		return None
	def pumpkin_factory():
		fila = structures.queue()
		def check_queue():
			while not fila['empty']():
				cur = fila['dequeue']()
				x,y = cur['coord']
				drone.move_to(x, y)
				if not can_harvest():
					fila['enqueue'](cur)
					
					is_dead = get_entity_type() == Entities.Dead_Pumpkin
					if is_dead:
						drone.plant(Entities.Pumpkin)
						
		def smashing_pumpkins(position):
			if drone.plant(Entities.Pumpkin):
				fila['enqueue'](position)
			
			last_tile = fila['size']() == position['chunk']['tiles']
			if last_tile:
				check_queue()
		return smashing_pumpkins
		
	change_hat(Hats.Traffic_Cone)
	visitor.parallel_chunks(pumpkin_factory(), max_drones())
	drone.clear()

def power():
	size = get_world_size()
	change_hat(Hats.Wizard_Hat)
	petals_map = dict()
	for i in range(7,16):
		petals_map[i] = set()

	def planting_sunflowers(position):
		x,y = position['coord']
		drone.plant(Entities.Sunflower)
		return measure()
			
	sunflowers_infos = visitor.parallel_rows(planting_sunflowers, max_drones())
	for sunflowers_info in sunflowers_infos:
		for tile in sunflowers_info:
			petals_map[sunflowers_info[tile]].add(tile)
		
	for qtd in range(15,6, -1):
		for x,y in petals_map[qtd]:
			drone.move_to(x,y)
			drone.try_harvest()

def cactus():
	n = get_world_size()
	def make_a_desert(position):
		x,y = position['coord']
		drone.plant(Entities.Cactus)
		
	def sort_row(position):
		x,y = position['coord']
		algorithms.bubble_sort_row(y)
		
	def sort_col(position):
		x,y = position['coord']
		algorithms.bubble_sort_col(x)
		
	change_hat(Hats.Cactus_Hat)
	visitor.parallel_rows(make_a_desert, max_drones())
	visitor.parallel_rows(sort_row, max_drones())
	visitor.parallel_cols(sort_col, max_drones())
	drone.clear()

def gold():
	n = get_world_size()
	n_2 = n // 2
	drone.move_to(n_2,n_2)
	drone.plant(Entities.Bush)
	maze.create(n)
	gold_position = measure()

	def distance(dir):
		global gold_position
		dx,dy = drone.vector[dir]
		x,y = get_pos_x() + dx, get_pos_y() + dy
		ax, ay = gold_position
		
		dist = ((ax-x) ** 2 + (ay - y) ** 2) ** 0.5 + random()
		return dist
	def treasure_found(x,y):
		return get_entity_type() == Entities.Treasure
		
	for _ in range(301):
		algorithms.depht_first_search(treasure_found, distance)
		maze.create(n, False)		
		gold_position = measure()
		
	drone.try_harvest()

def bones():
	n = get_world_size()
	tiles = n ** 2
	_apples = 0
	change_hat(Hats.Carrot_Hat)
	change_hat(Hats.Dinosaur_Hat)
	
	apple_position = measure()
	
	def distance(dir):
		global apple_position
		dx,dy = drone.vector[dir]
		x,y = get_pos_x() + dx, get_pos_y() + dy
		ax, ay = apple_position
		#dist = abs(ax-x) + abs(ay - y)
		dist = ((ax-x) ** 2 + (ay - y) ** 2) ** 0.5 + random()
		return dist

	def eat_apple(position):
		global _apples
		global apple_position
		
		if get_entity_type() == Entities.Apple:
			apple_position = measure()
			_apples += 1
			
		if _apples >= tiles:
			change_hat(Hats.Brown_Hat)
			_apples = 0
			change_hat(Hats.Dinosaur_Hat)

	visitor.snake(eat_apple,distance)

if __name__ == '__main__':
	#change_hat(Hats.Brown_Hat)
	#quick_print(random())
	#clear()
	hay()
	#wood()