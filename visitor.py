import drone
import math

def parameter_factory(x, y, chunk_size=None, xq=0, yq=0):
	n = get_world_size()
	rank = (y * n) + x + 1
	obj = { 
		'rank': rank, 
		'coord': (x,y),
		'X': x, #OBSOLETE
		'Y': y, #OBSOLETE 
		'chunk': { 
			'width': n, 
			'height': n,
			'coord': (xq, yq),
			'tiles': n * n, 
			'X': xq, 'Y': yq# Obsolete 
		} 
	}
	if chunk_size:
		cw, ch = chunk_size
		obj['chunk']['width'] = cw
		obj['chunk']['height'] = ch
		obj['chunk']['tiles'] = ch * cw
	return obj

def zig_zag_rows(activity):
	size = get_world_size()
	for j in range(size):
		for i in range(size):
			i2 = (1 - (j%2)) * i + (j%2) * (size-1-i)
			drone.move_to(i2,j)
			activity(parameter_factory(i2, j))

def zig_zag_columns(activity):
	size = get_world_size()
	for i in range(size):
		for j in range(size):
			j2 = (1 - (i%2)) * j + (i%2)* (size-1-j)
			drone.move_to(i,j2)
			activity(parameter_factory(i, j2))

def chunks(activity):
	size = get_world_size()
	cz = size // 4
	for jj in range(0, size, cz):
		yq = jj // cz
		
		for ii in range(0, size, cz):
			xq = ii // cz
			for i in range(ii, ii + cz, 1):
				for j in range(jj, jj + cz, 1):
					j2 = (1 - (i%2)) * j + (i%2)* (2* jj + cz - j - 1)
					drone.move_to(i,j2)
					activity(parameter_factory(i, j, (cz,cz), xq, yq))
					
def parallel_chunks(activity, num_workers=4):
	size = get_world_size()
	if num_workers > max_drones():
		quick_print('Sorry, we canot create', num_workers, 'drones')
		return
	tiles_per_worker = (size ** 2) // num_workers
	cz_h = math.sqrt(tiles_per_worker)
	if cz_h % 1 == 0: # perfect square
		cz_w = cz_h
	else:
		cz_h, cz_w = size // num_workers, size
		
	chunk_size = size // num_workers

	drones = []
	for jj in range(0, size, cz_h):
		yq = jj // chunk_size
		for ii in range(0, size, cz_w):
			xq = ii // chunk_size
			def work(xs=ii, ys=jj, w=cz_w, h=cz_h):
				for i in range(xs, xs + w, 1):
					for j in range(ys, ys + h, 1):
						j2 = (1 - (i%2)) * j + (i%2)* (2* ys + h - j - 1)
						drone.move_to(i,j2)
						activity(parameter_factory(i, j, (w,h), xq, yq))
			if xq == 0 and yq == 0:
				continue
			
			while True:
				quick_print('to', xq, yq)
				d = spawn_drone(work)
				if d:
					drones.append(d)
					break
	work(0,0, cz_w,cz_h)
	for d in drones:
		wait_for(d)
			
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
			activity(parameter_factory(top, c))
		top += 1

		# downwards
		for r in range(top, bottom + 1):
			drone.move_to(r, right)
			activity(parameter_factory(r, right))
		right -= 1

		if top <= bottom:
			# walk to the left
			for c in range(right, left - 1, -1):
				drone.move_to(bottom, c)
				activity(parameter_factory(bottom, c))
			bottom -= 1

		if left <= right:
			# upwards
			for r in range(bottom, top - 1, -1):
				drone.move_to(r, left)
				activity(parameter_factory(r, left))
			left += 1

if __name__ == '__main__':
	clear()
	drone.move_to(0,0)
	def action(pos):
		till()
	for i in [8,6]:
		parallel_chunks(action, i)
	pass