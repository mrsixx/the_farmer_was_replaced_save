import drone
import solver

if __name__ == '__main__':
	drone.clear()
	while True:
		for u in [Unlocks.Megafarm]:
			if num_unlocked(u) < 5:
				solver.unlock_objective(u)