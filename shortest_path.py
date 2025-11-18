n = get_world_size()
def find_path(start, goal):
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
				
		
		