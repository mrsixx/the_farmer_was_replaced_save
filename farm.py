import drone
import inventory
import visitor
import structures
import algorithms
import polyculture
import maze

def hay(enable_polyculture=True):
	votes = polyculture.get_polyculture_map(enable_polyculture)
	n = get_world_size()
		
	def whats_up_doc(position):
		x,y = position['coord']
		drone.try_harvest()
		plant = None
		if enable_polyculture:
			plant = polyculture.get_most_voted(votes, (x,y))
		if not plant:
			plant = Entities.Grass

		drone.plant(plant)

		if enable_polyculture and plant == Entities.Grass:
			type, tile = get_companion()
			polyculture.vote(votes, tile, type)
		
	change_hat(Hats.Straw_Hat)
	visitor.parallel_cols(whats_up_doc)
	if enable_polyculture:
		drone.clear_only({ Entities.Grass })
	drone.clear()
	
def hay_sequencial():
	clear()
	def sow_field(position):
		drone.try_harvest()
		#drone.plant(Entities.Grass)
		
	change_hat(Hats.Straw_Hat)
	visitor.parallel_rows(sow_field)
	drone.clear()

def wood(enable_polyculture=True):
	votes = polyculture.get_polyculture_map(enable_polyculture)

	def plant_a_lot_of_wood(position):
		drone.try_harvest()
		x,y = position['coord']
		wich = x % 2 == y % 2
		choice = [Entities.Bush, Entities.Tree][wich]
		final_choice = None

		if enable_polyculture:
			final_choice = polyculture.get_most_voted(votes, (x,y))
		
		if not final_choice:
			final_choice = choice
		
		drone.plant(final_choice)
		
		if enable_polyculture and final_choice == choice:
			type, tile = get_companion()
			polyculture.vote(votes, tile, type)
	
	change_hat(Hats.Tree_Hat)
	visitor.parallel_cols(plant_a_lot_of_wood)
	if enable_polyculture:
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
		plant = None
		if enable_polyculture:
			plant = polyculture.get_most_voted(votes, (x,y))
		if not plant:
			plant = Entities.Carrot

		drone.plant(plant)

		if enable_polyculture and plant == Entities.Carrot:
			type, tile = get_companion()
			polyculture.vote(votes, tile, type)
		
	change_hat(Hats.Wizard_Hat)
	visitor.parallel_rows(whats_up_doc)
	if enable_polyculture:
		drone.clear_only({ Entities.Carrot })
	drone.clear()
	
def pumpkins():
	n = get_world_size()
	if	not inventory.has_enought_to_produce(Entities.Pumpkin, 1.5 * (n**2)):
		quick_print('Canot produce pumpkins')
		return None
	def scope():
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
	visitor.parallel_chunks(scope(), 4)
	drone.clear()

def power():
	size = get_world_size()
	change_hat(Hats.Wizard_Hat)
	sunflowers = dict()
	for i in range(7,16):
		sunflowers[i] = set()

	def planting_sunflowers(position):
		x,y = position['coord']
		drone.plant(Entities.Sunflower)
		petals = measure()
		if petals != None:
			sunflowers[petals].add((x,y))
			
	visitor.zig_zag_rows(planting_sunflowers)
	for petals in range(15,6, -1):
		for x,y in sunflowers[petals]:
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
	visitor.parallel_rows(make_a_desert)
	visitor.parallel_rows(sort_row)
	visitor.parallel_cols(sort_col)
	drone.clear()

def gold():
	n = get_world_size()
	drone.move_to(0,0)
	maze.create(n)
	def treasure_found(x,y):
		return get_entity_type() == Entities.Treasure
	algorithms.depht_first_search(treasure_found)
	drone.try_harvest()

if __name__ == '__main__':
	#hay()
	wood()