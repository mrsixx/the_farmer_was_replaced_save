import drone
def parameter_factory(x, y, chunk_size, xq, yq):
	w = get_world_size()
	rank = (y * w) + x + 1
	return { 'Rank': rank, 'X': x, 'Y': y, 'Chunk': { 'Size': chunk_size, 'X': xq, 'Y': yq } }

def zig_zag_rows(activity):
	size = get_world_size()
	for j in range(size):
		for i in range(size):
			i2 = (1 - (j%2)) * i + (j%2) * (size-1-i)
			drone.move_to(i2,j)
			activity(parameter_factory(i2, j, size, 0, 0))

def zig_zag_columns(activity):
	size = get_world_size()
	for i in range(size):
		for j in range(size):
			j2 = (1 - (i%2)) * j + (i%2)* (size-1-j)
			drone.move_to(i,j2)
			activity(parameter_factory(i, j2, size, 0, 0))

def chunks(activity):
	size = get_world_size()
	chunk_size = size // 4
	for jj in range(0, size, chunk_size):
		yq = jj // chunk_size
		
		for ii in range(0, size, chunk_size):
			xq = ii // chunk_size
			for i in range(ii, ii + chunk_size, 1):
				for j in range(jj, jj + chunk_size, 1):
					j2 = (1 - (i%2)) * j + (i%2)* (2* jj + chunk_size - j - 1)
					drone.move_to(i,j2)
					activity(parameter_factory(i, j, chunk_size, xq, yq))

def spiral(activity):
	size = get_world_size()
	top = 0
	bottom = size - 1
	left = 0
	right = size - 1

	while top <= bottom and left <= right:
		# walk to the right
		for c in range(left, right + 1):
			drone.move_to(top, c)
			activity(parameter_factory(top, c, size, 0, 0))
		top += 1

		# downwards
		for r in range(top, bottom + 1):
			drone.move_to(r, right)
			activity(parameter_factory(r, right, size, 0, 0))
		right -= 1

		if top <= bottom:
			# walk to the left
			for c in range(right, left - 1, -1):
				drone.move_to(bottom, c)
				activity(parameter_factory(bottom, c, size, 0, 0))
			bottom -= 1

		if left <= right:
			# upwards
			for r in range(bottom, top - 1, -1):
				drone.move_to(r, left)
				activity(parameter_factory(r, left, size, 0, 0))
			left += 1

if __name__ == '__main__':
	pass