import drone
import farm
import math

# heuristic values (average)
power_consume_cycle = {
	Items.Hay: 40,
	Items.Pumpkin: 90,
	Items.Wood: 90, #tree + bush
	Items.Carrot: 70,
	Items.Cactus: 330
}

#heuristic factor of production factors
def get_harvest_factor(item):
	factor = {
		Items.Hay: 79.5, #harvesting 2x in farm.hay
		Items.Wood: 89.5, #polyculture
		Items.Carrot: 78.5, #polyculture
		Items.Power: 0.95 #sunflower cycle consumes 5% of expected
	}
	if item not in factor:
		return 1
	return factor[item]

def mult(unlock):
	return 2**(num_unlocked(unlock)-1)

#lower bounds for an cycle
def get_harvest_estimate(item):
	n = get_world_size()
	harvest_estimate = {
		Items.Hay: (n**2) * mult(Unlocks.Grass),
		Items.Pumpkin: (n**2) * mult(Unlocks.Pumpkins) * min(6, n),
		Items.Wood: (n**2) * 3 * mult(Unlocks.Trees), #n^2 * mult * (5+1)/2
		Items.Carrot: (n**2) * mult(Unlocks.Carrots),
		Items.Power: (n**2 - 9) * (5 * mult(Unlocks.Sunflowers)) + 9,
		Items.Cactus: (n**4) * mult(Unlocks.Cactus),
		Items.Gold: (n**2) * mult(Unlocks.Mazes),
		Items.Bone: (n**2) * mult(Unlocks.Dinosaurs)
	}
	return harvest_estimate[item]


def production_cycles(item, amount):
	factor = get_harvest_factor(item)
	estimate = factor * get_harvest_estimate(item)
	return math.round_positive(amount / estimate)

def calculate_inventory_variation_after(item, action):
	qtd = num_items(item)
	action()
	return num_items(item) - qtd


def calculate_yield(entity, farmer_action):
	expected = get_harvest_estimate(entity)
	start_time = get_time()
	obtained = calculate_inventory_variation_after(entity, farmer_action)
	finish_time = get_time()
	return {
		'entity': entity,
		'expected': expected,
		'obtained': obtained,
		'percentual_variation': ((obtained-expected) / expected) * 100,
		'percent_of_target': (obtained / expected) * 100,
		'duration': finish_time - start_time
	}


if __name__ == '__main__':

	quick_print(calculate_yield(Items.Hay, farm.hay))
	quick_print(calculate_yield(Items.Wood, farm.wood))
	quick_print(calculate_yield(Items.Carrot, farm.carrots))
	#quick_print(calculate_yield(Items.Pumpkin, farm.pumpkins))
	#quick_print(calculate_yield(Items.Power, farm.power))
	#quick_print(calculate_yield(Items.Cactus, farm.cactus))
	#quick_print(calculate_yield(Items.Gold, farm.gold))
	#quick_print(calculate_yield(Items.Bone, farm.bone))