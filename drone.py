import algorithms
import math
import ground
import inventory
import visitor

native_plant = plant
dry_ground_entities = {Entities.Grass}

vector = {
	North: (0,1),
	East: (1,0),
	South: (0,-1),
	West: (-1,0),
}

def move_to(x,y):
	start = math.point(get_pos_x(), get_pos_y())
	goal = math.point(x,y)
	for dir in algorithms.find_path(start, goal):
		move(dir)
		
def try_harvest():
	if get_entity_type() == None:
		return False
	
	fertilized = False
	while not can_harvest() and get_entity_type() != Entities.Dead_Pumpkin:
		use_item(Items.Fertilizer)
		fertilized = True
	if fertilized:
		use_item(Items.Weird_Substance)
	return harvest()


def wet_soil():
	while ground.dry_soil()	and inventory.has_water():
		use_item(Items.Water)

def plant(entity):
	if not inventory.has_enought_to_produce(entity, 1):
		quick_print('Not able to plant', entity)
		return False
		
	if ground.need_till():
		till()
		
	if entity not in dry_ground_entities:
		wet_soil()
		
	return native_plant(entity)

def clear():
	def clear_tile(position):
		if get_entity_type() not in {None}:
			try_harvest()
		
	visitor.parallel_cols(clear_tile)

def clear_only(types):
	def clear_tile(position):
		if get_entity_type() in types:
			try_harvest()
		
	visitor.parallel_rows(clear_tile)