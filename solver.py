import calculator
import farm
import drone
import inventory

#TODO: calculate topological sort
topological_sort = [Items.Power, Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin, Items.Cactus]

farm_strategies = {
	Items.Power: farm.power,
	Items.Hay: farm.hay,
	Items.Wood: farm.wood,
	Items.Carrot: farm.carrots,
	Items.Pumpkin: farm.pumpkins,
	Items.Cactus: farm.cactus
}

map_entity = {
	Items.Hay: Entities.Grass,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Wood: Entities.Tree, #tree + bush
	Items.Carrot: Entities.Carrot,
	Items.Power: Entities.Sunflower,
	Items.Cactus: Entities.Cactus
}

def __farm_power_to(item, cycles):
	power_needed = calculator.power_consume_cycle[item] * cycles
	__farm_item_recursive(Items.Power, power_needed)


def __farm_item_recursive(item, amount):
	amount_needed = inventory.get_shortage(item, amount)
	if amount_needed == 0:
		return
	entity = map_entity[item]
	production_cost = get_cost(entity)
	for dependency in production_cost:
		__farm_item_recursive(dependency, amount_needed * production_cost[dependency])

	farm_strategy = farm_strategies[item]
	cycles = calculator.production_cycles(item, amount_needed)
	if item != Items.Power:
		quick_print('Farming power for ', item, ' x', cycles, ' if needed...')
		__farm_power_to(item, cycles)

	quick_print('farming ', item, ' x', cycles, '(', amount_needed, ' un. )')
	for i in range(cycles):
		if inventory.get_shortage(item, amount) == 0:
			quick_print('breaking too early', item)
			break
		quick_print(item, '(', i+1, '/', cycles, ')')
		farm_strategy()
	quick_print('finished farming ', item)

#unlock any objective
def unlock_objective(objective):
	quick_print('starting unlocker...')
	quick_print('unlocking ', objective)

	unlock_cost = get_cost(objective)
	for item in topological_sort:
		if item not in unlock_cost:
			continue
		__farm_item_recursive(item, unlock_cost[item])
	
	quick_print('stopping unlocker...')
	if unlock(objective):
		quick_print(objective, ' unlocked!')
		do_a_flip()
	else:
		quick_print('failed to unlock ', objective)
