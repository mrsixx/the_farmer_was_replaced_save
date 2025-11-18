def has_enought_to_produce(item, amount):
	cost = get_cost(item)
	for key in cost:
		if num_items(key) < amount * cost[key]:
			return False
	return True
	
def has_water():
	return num_items(Items.Water) > 0