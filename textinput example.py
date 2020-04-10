#!/usr/bin/python3
import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInput()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

running = True

while running:
    screen.fill((225, 225, 225))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    if running:
    # Feed it with events every frame
        textinput.update(events)
    # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (10, 10))

        pygame.display.update()
        clock.tick(30)
print(textinput.get_text())
