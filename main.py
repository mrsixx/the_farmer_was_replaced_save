import farm
import drone
def twice(i):
	return i < 3

def grass_above_10k(i):
	return num_items(Items.Hay) < 10000

def wood_above_10k(i):
	return num_items(Items.Wood) < 10000

def carrots_above_10k(i):
	return num_items(Items.Carrot) < 10000

def can_unlock_expansion(i):
	cost = get_cost(Unlocks.Expand)
	for item in cost:
		if  num_items(item) < cost[item]:
			return True
	
	unlock(Unlocks.Expand)			
	return False
	
if __name__ == '__main__':
	drone.clear()
	#farm.hay(twice)
	#farm.wood(twice)
	farm.pumpkins(twice)
	#farm.power(twice)
	#farm.carrots(carrots_above_10k)

	
	
	
			
