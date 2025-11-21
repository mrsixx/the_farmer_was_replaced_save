import drone
import inventory
import visitor
import structures
import algorithms
import polyculture

def hay():
	clear()
	def sow_field(position):
		drone.try_harvest()
		#drone.plant(Entities.Grass)
		
	change_hat(Hats.Straw_Hat)
	visitor.zig_zag_columns(sow_field)
	drone.clear()

def wood(enable_polyculture=True):
	votes = polyculture.get_polyculture_map(enable_polyculture)

	def plant_a_lot_of_wood(position):
		drone.try_harvest()
		x,y = position['X'],position['Y']
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
	visitor.zig_zag_columns(plant_a_lot_of_wood)
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
		x,y = position['X'],position['Y']
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
	visitor.zig_zag_rows(whats_up_doc)
	if enable_polyculture:
		drone.clear_only({ Entities.Carrot })
	drone.clear()
	
def pumpkins():
	n = get_world_size()
	if	not inventory.has_enought_to_produce(Entities.Pumpkin, 1.5 * (n**2)):
		quick_print('Canot produce pumpkins')
		return None
		
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
			
		
	change_hat(Hats.Traffic_Cone)
	visitor.chunks(smashing_pumpkins)
	drone.clear()


def power():
	size = get_world_size()
	change_hat(Hats.Wizard_Hat)
	sunflowers = dict()
	for i in range(7,16):
		sunflowers[i] = set()

	def planting_sunflowers(position):
		x,y = position['X'], position['Y']
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
	def making_a_desert(position):
		x,y = position['X'], position['Y']
		drone.plant(Entities.Cactus)
	
	change_hat(Hats.Cactus_Hat)
	visitor.zig_zag_rows(making_a_desert)
	for i in range(n):
		algorithms.bubble_sort_row(i)
	
	for i in range(n):
		algorithms.bubble_sort_col(i)
	drone.clear()
