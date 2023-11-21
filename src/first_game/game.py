import pygame
import os

def run():
    # pygame setup
    pygame.init()
    
    screen = pygame.display.set_mode((1728,1117))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    # player variables
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_speed = 300

    # load player image
    player_img = pygame.image.load(os.path.join("assets", "ship_small.png"))
    player_img.convert()
    player_img_rect = player_img.get_rect()


    player_projectiles = []
    projectiles_speed = 400
    # delay the projectile creation speed
    projectiles_delay = 500
    prev_projectile_time = 0

    while running:
        # Process player inputs.
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Do logical updates here
        # player logic
        # player movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= player_speed * delta_time
        if keys[pygame.K_s]:
            player_pos.y += player_speed * delta_time
        if keys[pygame.K_a]:
            player_pos.x -= player_speed * delta_time
        if keys[pygame.K_d]:
            player_pos.x += player_speed * delta_time

        # projectiles logic
        if keys[pygame.K_SPACE]:
            # check if enough time has passed before creating new projectile
            if pygame.time.get_ticks() - prev_projectile_time > projectiles_delay:
                # new prjectile starts from above player
                new_projectile = pygame.Vector2(player_pos.x,  player_pos.y - 8)
                player_projectiles.append(new_projectile)
                # saving the previous projectile creation time
                prev_projectile_time = pygame.time.get_ticks()

        # projectile movement
        # loop throught front the end of the list to avoid bad indexes
        for i in range(len(player_projectiles) - 1, -1, -1):
            p = player_projectiles[i]
            p.y -= projectiles_speed * delta_time
            # destroy projectile when it goes beyond screen
            if p.y < -15:
                del player_projectiles[i]

        # Fill the display with a solid color
        screen.fill("black")  


        # Render the graphics here.
        # draw player 
        # pygame.draw.circle(screen, "white", player_pos, 15)
        # draw player image on screen
        screen.blit(player_img, (player_pos.x - player_img_rect.w / 2, player_pos.y - player_img_rect.h / 2))

        # draw projectiles
        for p in player_projectiles:
            # initialized position to draw projectiles
            projectile_rect = pygame.Rect(p.x, p.y, 3, 10)
            # draw projectiles
            pygame.draw.rect(screen, "red", projectile_rect)


        # Refresh on-screen display
        pygame.display.flip()  
        # wait until next frame (at 60 FPS)
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        delta_time = clock.tick(60) / 1000        
    
    pygame.quit()