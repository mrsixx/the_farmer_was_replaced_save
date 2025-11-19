import calculator
import farm
import drone
import inventory

#TODO: calculate topological sort
topological_sort = [Items.Power, Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin]

farm_strategies = {
	Items.Power: farm.power,
	Items.Hay: farm.hay,
	Items.Wood: farm.wood,
	Items.Carrot: farm.carrots,
	Items.Pumpkin: farm.pumpkins,
}


def unlock_objective(objective):
	quick_print('Starting unlocker...')
	quick_print('Unlocking ', objective)
	cycles = calculator.how_many_cicles(objective)
	cycles[Items.Power] = 2 #TODO: estimate energy
	quick_print('Scheduling: ', cycles)
	for dependency in topological_sort:
		if dependency not in cycles:
			continue
		if inventory.has_enought_to_unlock(objective):
			break
				
		farm_strategy = farm_strategies[dependency]
		for i in range(cycles[dependency]):
			if inventory.has_enought_to_unlock(objective):
				break
				
			quick_print('Farming ', dependency, ' (',i+1,'/',cycles[dependency],')')
			drone.move_to(0,0)
			farm_strategy()
	quick_print('Stopping unlocker...')
	unlock(objective)
	quick_print(objective, ' unlocked!')
	do_a_flip()
	