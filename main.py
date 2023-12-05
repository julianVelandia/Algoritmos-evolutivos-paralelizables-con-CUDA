import sys
import pygame
from car import Car, load_neural_network
import neat

SCREEN_HEIGHT = 1500
SCREEN_WIDTH = 800
CAR_HEIGHT = 100
CAR_WIDTH = 100
GENERATION = 0

pygame.display.set_caption('cars')
icon = pygame.image.load('car.png')
pygame.display.set_icon(icon)

game_map = pygame.image.load('track1.png')

def main():

    car = Car(game_map)
    car_speed = 4

    running = True
    while running:

        screen.blit(game_map, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dif_angle = -car_speed
                if event.key == pygame.K_RIGHT:
                    dif_angle = car_speed

                if event.key == pygame.K_DOWN:
                    dif_y = car_speed
                if event.key == pygame.K_UP:
                    dif_y = -car_speed

                if event.key == pygame.K_SPACE:
                    dif_angle = car_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dif_x = 0
                    dif_angle = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    dif_y = 0

                if event.key == pygame.K_SPACE:
                    dif_angle = 0

        car.update()

        if not car.get_collided():
            car.draw(screen)

        pygame.display.update()


def run_car(genomes, config):
    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car(game_map))

    pygame.init()
    screen = pygame.display.set_mode((
        SCREEN_HEIGHT, SCREEN_WIDTH
    ))

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 40)
    font = pygame.font.SysFont("Arial", 20)

    global GENERATION
    GENERATION += 1
    while True:
        screen.blit(game_map, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_data())
            i = output.index(max(output))
            if i == 0:
                car.angle += 10
            else:
                car.angle -= 10

        remain_cars = 0
        for i, car in enumerate(cars):
            if not(car.get_collided()):
                remain_cars += 1
                car.update()
                genomes[i][1].fitness += car.get_reward()

        if remain_cars == 0:
            break

        screen.blit(game_map, (0, 0))
        for car in cars:
            if not(car.get_collided()):
                car.draw(screen)

        text = generation_font.render(
            "Generation : " + str(GENERATION), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 300, 150)
        screen.blit(text, text_rect)

        text = font.render("Remain cars : " +
                           str(remain_cars), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 200, 200)
        screen.blit(text, text_rect)

        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 200, 230)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(0)


if __name__ == "__main__":
    load_neural_network('winner.pkl')
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(run_car, 1000)

