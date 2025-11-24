import drone
import algorithms

def create(size, plant=True):
	if plant:
		drone.plant(Entities.Bush)
	weird_substance_amount = size * (2**(num_unlocked(Unlocks.Mazes)-1))
	if num_items(Items.Weird_Substance) < weird_substance_amount:
		quick_print('Canot create maze')
		return None
	use_item(Items.Weird_Substance, weird_substance_amount)


if __name__ == '__main__':
	clear()
	drone.move_to(0,0)
	create(get_world_size())
	def target(x,y):
		return get_entity_type() == Entities.Treasure
	algorithms.depht_first_search(target)
	drone.try_harvest()
	#harvest()
