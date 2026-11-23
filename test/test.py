import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

line_x = None

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                line_x = event.pos[0]

    screen.fill((30, 30, 30))

    if line_x is not None:
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (line_x, 0),
            (line_x, 600),
            2
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()