import drone
import farm
import math
import inventory 

# dou um unlock para o solver
# ele calcula quantos ciclos de cada coisa precisa ser feito
# e coloca numa fila de execucoes


map_entity = {
	Items.Hay: Entities.Grass,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Wood: Entities.Tree, #tree + bush
	Items.Carrot: Entities.Carrot
}

#lower bounds for an cycle
def get_harvest_estimate(item):
	n = get_world_size()
	harvest_estimate = {
		Items.Hay: n * 8,
		Items.Pumpkin: min(6, n) * (n ** 2),
		Items.Wood: (n**2) * (5 + 2) * 0.5, #tree + bush
		Items.Carrot: (n**2) * 4
	}
	return harvest_estimate[item]
	
def calculate_cost(objective):
	obj = {}
	for item in objective:
		amount = inventory.get_shortage(item, objective[item])
		__key_accumulate(obj, item, amount)
		costs = calculate_cost_recursive(item, amount)
		for key in costs:
			__key_accumulate(obj, key, costs[key])
	return __clear_keys(obj)
	
def calculate_cost_recursive(desired_item, amount):
	obj = { }
	if desired_item not in map_entity:
		return {}
	entity = map_entity[desired_item]
	cost = get_cost(entity)
	for item in cost:
		__key_accumulate(obj, item, inventory.get_shortage(item, amount * cost[item]))
		dependencies_cost = calculate_cost_recursive(item, obj[item])
		for dependency in dependencies_cost:
			__key_accumulate(obj, dependency, dependencies_cost[dependency])
	return obj
	

def how_many_cicles(objective):
	cycles = {}
	unlock_cost = get_cost(objective)
	shortage_items = calculate_cost(unlock_cost)
	for item in shortage_items:
		amount_needed = shortage_items[item]
		if amount_needed == 0:
			continue
			
		estimate = get_harvest_estimate(item)
		cycles[item] = math.round_positive(amount_needed / estimate)

	return __clear_keys(cycles)
	
def __key_accumulate(dict, key, amount):
		if key not in dict:
			dict[key] = 0
		dict[key] += amount
		
def __clear_keys(dic):
	remove_keys = []	
	for key in dic:
		if dic[key] == 0:
			remove_keys.append(key)
	for key in remove_keys:		
		dic.pop(key)
	return dic
	
def calc_error():
	drone.clear()

	def one_time(i):
		return i < 2
		
	def run(item, farmer):
		num = num_items(item)
		expected = get_harvest_estimate(item)
	
		farmer(one_time)
		yield = num_items(item) - num
		error = expected - yield
		quick_print(item, 'error=', error)
	
	run(Items.Hay, farm.hay)
	run(Items.wood, farm.wood)
	run(Items.Carrot, farm.carrots)
	run(Items.Pumpkin, farm.pumpkins)

if __name__ == '__main__':
	quick_print(how_many_cicles(Unlocks.Pumpkins))