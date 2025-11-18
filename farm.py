from drone_visitors import *
from farm_scenarios import *
import drone
import inventory
import visitor

total = get_world_size() ** 2

def hay(until):
	clear()
	change_hat(Hats.Straw_Hat)
	i = 1
	while until(i):
		visitor.zig_zag_columns(just_collect_hay)
		i += 1
	drone.move_to(0,0)
	do_a_flip()
	drone.clear()

def wood(until):
	drone.clear()
	change_hat(Hats.Tree_Hat)
	i = 1
	while until(i):
		visitor.zig_zag_columns(plant_a_lot_of_wood)
		i+= 1
	drone.move_to(0,0)
	do_a_flip()
	drone.clear()	
	
def wood_and_hay(until):
	drone.clear()
	change_hat(Hats.Tree_Hat)
	i = 1
	while until(i):
		visitor.chunks(wood_and_hay_just_like_astekas)
		i+= 1
	drone.move_to(0,0)
	do_a_flip()
	drone.clear()	
	
def carrots(until):
	drone.clear()
	change_hat(Hats.Wizard_Hat)
	i = 1
	while until(i):
		def cant_produce(j):
			return not inventory.has_enought_to_produce(Entities.Carrot, total)
			
		if cant_produce(0):
			quick_print('Canot farm carrots, farming some wood and hay')
			farm_wood_and_hay(cant_produce)
			
			
		visitor.zig_zag_rows(whats_up_doc)
		i+=1
	drone.move_to(0,0)
	do_a_flip()
	drone.clear()
	
def pumpkins(until):
	type = get_entity_type()
	if(type != None and type != Entities.Grass):
		drone.clear()				
	change_hat(Hats.Traffic_Cone)
	i = 1
	while until(i):
		def cant_produce(j):
			return not inventory.has_enought_to_produce(Entities.Pumpkin, 1.5 * total)
			
		if cant_produce(0):
			quick_print('Canot farm pumpkins, farming some carrots')
			carrots(cant_produce)
			
		visitor.chunks(smashing_pumpkins)
		drone.move_to(0,0)
		drone.try_harvest()
		i+= 1
	do_a_flip()
	drone.clear()

def power(until):
	size = get_world_size()
	#drone.clear()
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
			

	i = 1
	while until(i):
		visitor.zig_zag_rows(planting_sunflowers)
		for petals in range(15,6, -1):
			for x,y in sunflowers[petals]:
				drone.move_to(x,y)
				drone.try_harvest()
		i+=1
	drone.move_to(0,0)
	do_a_flip()
	drone.clear()
