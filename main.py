import drone
import solver
unlocks = {
	Unlocks.The_Farmers_Remains: 1,
	#Unlocks.Dinosaurs: 2,
	#Unlocks.Mazes: 2,
}
if __name__ == '__main__':
	drone.clear()
	
	for u in unlocks:
		for _ in range(unlocks[u]):
			solver.unlock_objective(u)
		