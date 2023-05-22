import pygame
import os
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre de jeu
WIDTH = 1200
HEIGHT = 800

# Couleurs
WHITE = (255, 255, 255)

# Création de la fenêtre de jeu
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balkany Runner")

# Chargement des sprites
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'sprites')

background = pygame.image.load(os.path.join(image_path, 'paris.png'))

player_sprite1 = pygame.image.load(os.path.join(image_path, 'balkany1.png'))
player_sprite1 = pygame.transform.scale(player_sprite1, (80, 160))
player_sprite2 = pygame.image.load(os.path.join(image_path, 'balkany2.png'))
player_sprite2 = pygame.transform.scale(player_sprite2, (80, 160))
player_rect = player_sprite1.get_rect()
player_rect.x = 50
player_rect.y = HEIGHT - player_rect.height - 50

obstacle_sprite = pygame.image.load(os.path.join(image_path, 'policier.png'))
obstacle_sprite = pygame.transform.scale(obstacle_sprite, (50, 50))
obstacle_rect = obstacle_sprite.get_rect()
obstacle_rect.x = WIDTH
obstacle_rect.y = HEIGHT - obstacle_rect.height - 50

argent_sprite = pygame.image.load(os.path.join(image_path, 'argent.png'))
argent_sprite = pygame.transform.scale(argent_sprite, (50, 50))
argent_rect = argent_sprite.get_rect()
argent_rect.x = WIDTH + random.randint(200, 400)
argent_rect.y = HEIGHT - argent_rect.height - 50

game_over_sprite = pygame.image.load(os.path.join(image_path, 'game_over.png'))
game_over_sprite= pygame.transform.scale(game_over_sprite, (1200, 800))
game_over_rect = game_over_sprite.get_rect()
game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

play_button_sprite = pygame.image.load(os.path.join(image_path, 'bouton_jouer.png'))
play_button_sprite= pygame.transform.scale(play_button_sprite, (200, 100))
play_button_rect = play_button_sprite.get_rect()
play_button_rect.center = (WIDTH // 2, HEIGHT - 100)

score = 0
velocity_multiplier = 1.0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

gravity = 0.56
player_velocity = 0

running = True
game_over = False
sprite_index = 0  # Indice du sprite actuel du joueur
player_sprites = [player_sprite1, player_sprite2]  # Liste des sprites du joueur

sprite_change_frames = 10  # Nombre de frames entre chaque changement de sprite
frame_count = 0  # Compteur de frames

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if play_button_rect.collidepoint(event.pos):
                game_over = False
                player_rect.y = HEIGHT - player_rect.height - 50
                obstacle_rect.x = WIDTH
                obstacle_rect.y = HEIGHT - obstacle_rect.height - 50
                argent_rect.x = WIDTH + random.randint(200, 400)
                argent_rect.y = HEIGHT - argent_rect.height - 50
                score = 0
                velocity_multiplier = 1.0

    if not game_over:
        # Déplacement du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player_rect.y == HEIGHT - player_rect.height - 50:
            player_velocity = -12

        # Mise à jour de la position du joueur avec la physique du saut
        player_velocity += gravity
        player_rect.y += player_velocity
        if player_rect.y > HEIGHT - player_rect.height - 50:
            player_rect.y = HEIGHT - player_rect.height - 50
            player_velocity = 0

        # Déplacement de l'obstacle
        obstacle_rect.x -= 5 * velocity_multiplier
        if obstacle_rect.x + obstacle_rect.width < 0:
            obstacle_rect.x = WIDTH + random.randint(200, 400)
            obstacle_rect.y = HEIGHT - obstacle_rect.height - 50
            velocity_multiplier *= 1.06

        # Déplacement de l'objet argent
        argent_rect.x -= 5 * velocity_multiplier
        if argent_rect.x + argent_rect.width < 0:
            argent_rect.x = WIDTH + random.randint(200, 400)
            argent_rect.y = HEIGHT - argent_rect.height - 50

        # Collision entre le joueur et l'obstacle
        if player_rect.colliderect(obstacle_rect):
            game_over = True

        # Collision entre le joueur et l'objet argent
        if player_rect.colliderect(argent_rect):
            score += 1
            argent_rect.x = WIDTH + random.randint(200, 400)
            argent_rect.y = HEIGHT - argent_rect.height - 50
            velocity_multiplier *= 1.06

    # Affichage des éléments
    window.blit(background, (0, 0))

    if not game_over:
        if frame_count % sprite_change_frames == 0:  # Changement de sprite toutes les sprite_change_frames frames
            sprite_index = (sprite_index + 1) % len(player_sprites)  # Alterne entre les deux sprites

        window.blit(player_sprites[sprite_index], (player_rect.x, player_rect.y))
        window.blit(obstacle_sprite, (obstacle_rect.x, obstacle_rect.y))
        window.blit(argent_sprite, (argent_rect.x, argent_rect.y))
    else:
        window.blit(game_over_sprite, game_over_rect)
        window.blit(play_button_sprite, play_button_rect)

    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)
    frame_count += 1  # Incrémente le compteur de frames

# Fermeture de Pygame
pygame.quit()
