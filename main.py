import drone
import solver

if __name__ == '__main__':
	drone.clear()
	while True:
		for u in [Unlocks.Grass, Unlocks.Carrots]:
			if num_unlocked(u) < 11:
				solver.unlock_objective(u)