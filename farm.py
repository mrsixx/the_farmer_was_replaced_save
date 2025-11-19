import drone
import inventory
import visitor
import structures

def hay():
	def sow_field(position):
		drone.try_harvest()
		drone.plant(Entities.Grass)
		
	change_hat(Hats.Straw_Hat)
	visitor.zig_zag_columns(sow_field)
	drone.clear()

def wood():
	def plant_a_lot_of_wood(position):
		drone.try_harvest()
		choice = [Entities.Bush, Entities.Tree][position['Rank'] % 2]
		drone.plant(choice)
	
	change_hat(Hats.Tree_Hat)
	visitor.zig_zag_columns(plant_a_lot_of_wood)
	drone.clear()
	
def carrots():
	n = get_world_size()
	if	not inventory.has_enought_to_produce(Entities.Carrot, (n**2)):
		quick_print('Canot produce carrots')
		return None
		
	def whats_up_doc(position):
		drone.try_harvest()
		drone.plant(Entities.Carrot)
		
	change_hat(Hats.Wizard_Hat)
	visitor.zig_zag_rows(whats_up_doc)
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
