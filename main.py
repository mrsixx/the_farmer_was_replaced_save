import farm
import drone
import solver
import calculator

def calcular_rendimento(acao, item):
	qtd = num_items(item)
	acao()
	return num_items(item) - qtd


if __name__ == '__main__':
	clear()
	#quick_print('hay', calcular_rendimento(farm.hay, Items.Power))
	#quick_print('wood', calcular_rendimento(farm.wood, Items.Power))
	#quick_print('carrots', calcular_rendimento(farm.carrots, Items.Power))
	#quick_print('pumpkins', calcular_rendimento(farm.pumpkins, Items.Power))
	#quick_print('cactus', calcular_rendimento(farm.cactus, Items.Power))
	#drone.move_to(0,4)
	#drone.clear()
	#change_hat(Hats.Dinosaur_Hat)
	#farm.power()
	#change_hat(Hats.Brown_Hat)
	#while True:
		#farm.power()
		#farm.cactus()
	#while True:
	for u in [Unlocks.Grass, Unlocks.Pumpkins]:
		solver.unlock_objective(u)
	
	#quick_print(calculator.how_many_cicles(Unlocks.Expand))
	#farm.hay()
	#farm.wood(twice)
	#farm.pumpkins(twice)
	#farm.power(twice)
	#farm.carrots(carrots_above_10k)

	
	
	
			
