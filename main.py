import drone
import solver

if __name__ == '__main__':
	drone.clear()
	while True:
		for u in [Unlocks.Expand]:
			if num_unlocked(u) < 9:
				solver.unlock_objective(u)