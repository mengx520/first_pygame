import pygame

def run():
    # pygame setup
    pygame.init()
    
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_speed = 300

    while running:
        # Process player inputs.
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Do logical updates here.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= player_speed * delta_time
        if keys[pygame.K_s]:
            player_pos.y += player_speed * delta_time
        if keys[pygame.K_a]:
            player_pos.x -= player_speed * delta_time
        if keys[pygame.K_d]:
            player_pos.x += player_speed * delta_time
            
        # Fill the display with a solid color
        screen.fill("black")  

        # Render the graphics here.
        pygame.draw.circle(screen, "white", player_pos, 15)

        # Refresh on-screen display
        pygame.display.flip()  
        # wait until next frame (at 60 FPS)
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        delta_time = clock.tick(60) / 1000        
    
    pygame.quit()