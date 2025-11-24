import drone
import solver
unlocks = {
	Unlocks.Cactus: 4,
	Unlocks.Dinosaurs: 2,
	Unlocks.Mazes: 2,
}
if __name__ == '__main__':
	drone.clear()
	while True:
		for u in unlocks:
			for _ in range(unlocks[u]):
				if num_unlocked(u) < 5:
					solver.unlock_objective(u)
				continue
		break