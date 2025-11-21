import farm
import drone
import solver
import calculator

def calcular_rendimento_madeira(acao):
	qtd = num_items(Items.Hay)
	acao()
	return num_items(Items.Hay) - qtd


if __name__ == '__main__':
	clear()
	#drone.move_to(0,4)
	#drone.clear()
	#change_hat(Hats.Dinosaur_Hat)
	#farm.power()
	#change_hat(Hats.Brown_Hat)
	#while True:
		#farm.power()
		#farm.cactus()
	while True:
		for u in [Unlocks.Pumpkins]:
			drone.clear()
			solver.unlock_objective(u)
	
	#quick_print(calculator.how_many_cicles(Unlocks.Expand))
	#farm.hay()
	#farm.wood(twice)
	#farm.pumpkins(twice)
	#farm.power(twice)
	#farm.carrots(carrots_above_10k)

	
	
	
			
