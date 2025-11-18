def need_till():
	return get_ground_type() != Grounds.Soil

def dry_soil():
	threshold = 0.75
	return get_water() < threshold