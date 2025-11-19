import drone
import farm

# dou um unlock para o solver
# ele calcula quantos ciclos de cada coisa precisa ser feito
# e coloca numa fila de execucoes
n = get_world_size()

map_entity = {
	Items.Hay: Entities.Grass,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Wood: Entities.Tree, #tree + bush
	Items.Carrot: Entities.Carrot
}

#lower bounds for an cycle
harvest_estimate = {
	Items.Hay: n * 8,
	Items.Pumpkin: min(6, n) * (n ** 2),
	Items.Wood: n * (5 + 2) * 0.5, #tree + bush
	Items.Carrot: n * 4
}

def how_many_cicles(objective):
	cycles = {}
	unlock_cost = get_cost(objective)
	for item in unlock_cost:
		stocked = num_items(item)
		cost = unlock_cost[item]
		amount_needed = max(cost - stocked,0)
		if amount_needed == 0:
			pass
			
		estimate = harvest_estimate[item]
		cycles[item] = (amount_needed // estimate) + 1
		
		if item not in map_entity:
			pass
		
		dependencies = how_many_cicles(map_entity[item])
		for dependency in dependencies:
			if dependency not in cycles:
				cycles[dependency] = 0
			cycles[dependency] += dependencies[dependency]
	return cycles


def calc_error():
	drone.clear()

	def one_time(i):
		return i < 2
		
	def run(item, farmer):
		num = num_items(item)
		expected = harvest_estimate[item]
	
		farmer(one_time)
		yield = num_items(item) - num
		error = expected - yield
		quick_print(item, 'error=', error)
	
	run(Items.Hay, farm.hay)
	run(Items.wood, farm.wood)
	run(Items.Carrot, farm.carrots)
	run(Items.Pumpkin, farm.pumpkins)

if __name__ == '__main__':
	clear()
	drone.move_to(0,0)
	drone.plant(Entities.Pumpkin)
	quick_print(get_companion())