import pygame
import os
import random

def run():
    '''
    first section was to initialize required variables of the game
    '''
    pygame.init()

    screen = pygame.display.set_mode((1600,900))
    # creating screen barrier avoiding player go out of screen
    # using screen.get_width() to make the barrier ajusted automatically based on screen setting
    screen_barrier = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    # load player image
    player_img = pygame.image.load(os.path.join("assets", "ship_small.png")).convert()

    # player variables
    player_pos = player_img.get_rect()
    player_pos.x = screen.get_width() / 2 - player_pos.w / 2
    player_pos.y = screen.get_height() / 2 - player_pos.h / 2
    player_speed = 300

    player_projectiles = []
    projectiles_speed = 400
    # delay the projectile creation speed
    projectiles_delay = 500
    prev_projectile_time = 0

    # creating enemy variables
    enemies = []
    for e in range(0, 5):
        enemies_pos_x = random.randint(0, 1600)
        enemies_pos_y = random.randint(0, (player_pos.y - 200))
        enemies.append(pygame.Rect(enemies_pos_x, enemies_pos_y, 50, 50))

    '''
    main game logic starting from here
    '''
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

        # limited player movement to screen space
        player_pos.clamp_ip(screen_barrier)

        # projectiles logic
        if keys[pygame.K_SPACE]:
            # check if enough time has passed before creating new projectile
            if pygame.time.get_ticks() - prev_projectile_time > projectiles_delay:
                # new prjectile starts from above player
                # new_projectile = pygame.Vector2(player_pos.center)
                # for testing projectile collision with enemy, creating rect instead of vector
                new_projectile = pygame.Rect(player_pos.x + player_pos.w / 2, player_pos.y, 3, 10)
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

        # check enemies and projectile collision
        for e in range(len(enemies) - 1, -1, -1):
             collision_projectile_index = enemies[e].collidelist(player_projectiles)
             if collision_projectile_index != -1:
                del enemies[e]
                # remove collision projectile index from projectile list
                del player_projectiles[collision_projectile_index]


        # Fill the display with a solid color
        screen.fill("black")

        # Render the graphics here.
        # draw player
        # pygame.draw.circle(screen, "white", player_pos, 15)
        # draw player image on screen
        screen.blit(player_img, (player_pos.x, player_pos.y))

        # draw projectiles
        for p in player_projectiles:
            # draw projectiles
            pygame.draw.rect(screen, "red", p)

        # draw enemies
        for e in enemies:
            pygame.draw.rect(screen, "green", e)

        # Refresh on-screen display
        pygame.display.flip()
        # wait until next frame (at 60 FPS)
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        delta_time = clock.tick(60) / 1000

    pygame.quit()