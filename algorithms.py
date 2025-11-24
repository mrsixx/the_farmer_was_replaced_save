import drone
import structures

oposite = { North: South, South: North, East: West, West: East }

def identity(x):
	return x
	
def insertion_sort(list, criteria=identity):
	for i in range(1, len(list)):
		j = i - 1
		v = list[i]
		while j >= 0 and criteria(v) < criteria(list[j]):
			list[j+1], list[j] = list[j], list[j+1] 
			j -= 1
	return list


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

def find_path(start, goal):
	n = get_world_size()
	path = []
	x,y = start['X'], start['Y']
	if x != goal['X']:
		dx = (goal['X'] - x + n) % n
		if dx <= n - dx: # move to east
			for i in range(dx):
				x = (x+1) % n
				path.append(East)
		else: # move to west
			for i in range(n-dx):
				x = (x-1 + n) % n
				path.append(West)
				
	if y != goal['Y']:
		dy = (goal['Y'] - y + n) % n
		if dy <= n - dy: # move to north
			for i in range(dy):
				y = (y+1) % n
				path.append(North)
		else: # move to south
			for i in range(n - dy):
				y = (y-1+n) % n
				path.append(South)
	return path
				

def depht_first_search(target_achieved):
	visited = set()
	achieved = False
	
	def dfs(x,y):
		global achieved
		
		if achieved:
			return
		visited.add((x,y))
		if target_achieved(x,y):
			achieved = True
			return
			
		for dir in [West,North, East, South]:
			if move(dir):
				nx, ny = get_pos_x(), get_pos_y()
				if (nx,ny) in visited:
					move(oposite[dir])
					continue
				dfs(nx,ny)
				if achieved:
					return
				move(oposite[dir])
				
	dfs(get_pos_x(), get_pos_y())

