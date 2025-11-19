def has_enought_to_produce(item, amount):
	cost = get_cost(item)
	for key in cost:
		if num_items(key) < amount * cost[key]:
			return False
	return True
	
def has_water():
	return num_items(Items.Water) > 0
	
def get_shortage(item, amount):
	stocked = num_items(item)
	return max(amount - stocked,0)

def has_enought_to_unlock(objective):
	cost = get_cost(objective)
	for key in cost:
		if num_items(key) < cost[key]:
			return False
	return True
	