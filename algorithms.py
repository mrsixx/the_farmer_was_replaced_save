import drone
def bubble_sort_row(row):
	n = get_world_size()
	for i in range(n):
		swapped = False
		for j in range(n-1):
			drone.move_to(j, row)
			x = measure()
			y = measure(East)
			if x > y:
				swap(East)
				swapped = True
		if not swapped:
			break
				
def bubble_sort_col(col):
	n = get_world_size()
	for i in range(n):
		swapped = False
		for j in range(n-1):
			drone.move_to(col, j)
			x = measure()
			y = measure(North)
			if x > y:
				swap(North)
				swapped = True
		if not swapped:
			break
	