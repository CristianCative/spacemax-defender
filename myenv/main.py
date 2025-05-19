import pygame
import random
import os

# Inicializar Pygame y el mezclador de sonido
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print("Advertencia: mixer no pudo inicializarse, el sonido podría no funcionar.")

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceMax Defender")

# Rutas de assets
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
img_path = os.path.join(assets_path, 'images')
snd_path = os.path.join(assets_path, 'sounds')

# Tamaños de sprites
PLAYER_SIZE = (80, 80)
ENEMY_SIZE  = (60, 60)
BULLET_SIZE = (20, 30)

# Cargar y escalar imágenes
player_img = pygame.image.load(os.path.join(img_path, 'player.png')).convert_alpha()
player_img = pygame.transform.scale(player_img, PLAYER_SIZE)

enemy_imgs = []
for filename in ['enemy1.png', 'enemy2.png', 'enemy3.png']:
    img = pygame.image.load(os.path.join(img_path, filename)).convert_alpha()
    enemy_imgs.append(pygame.transform.scale(img, ENEMY_SIZE))

bullet_img = pygame.image.load(os.path.join(img_path, 'bullet.png')).convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, BULLET_SIZE)

background = pygame.image.load(os.path.join(img_path, 'background.jpg')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar sonidos (si mixer inicializado)
laser_sound = None
explosion_sound = None
if pygame.mixer.get_init():
    try:
        laser_sound    = pygame.mixer.Sound(os.path.join(snd_path, 'laser.mp3'))
        explosion_sound = pygame.mixer.Sound(os.path.join(snd_path, 'explosion.mp3'))
    except pygame.error:
        print("No se pudieron cargar los sonidos.")

# Definición de clases
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect  = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom  = HEIGHT - 10
        self.speed = 8
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type_index):
        super().__init__()
        self.image = enemy_imgs[type_index]
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed     = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y   += 30

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = bullet_img
        self.rect  = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom  = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Función para pantalla de fin de juego
def game_over_screen(win=False, score=0):
    font_big = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    if win:
        text = font_big.render("¡Ganaste!", True, (0, 255, 0))
    else:
        text = font_big.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))

    prompt = font_small.render("Presiona R para volver a jugar o Q para salir", True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(WIDTH/2, HEIGHT/2 + 20))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        screen.blit(prompt, prompt_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(15)

# Función para iniciar el juego
def main():
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies    = pygame.sprite.Group()
    bullets    = pygame.sprite.Group()

    # Crear jugador
    player = Player()
    all_sprites.add(player)

    # Crear enemigos
    for row in range(3):
        for col in range(8):
            enemy = Enemy(100 + col * 70, 50 + row * 60, row)
            all_sprites.add(enemy)
            enemies.add(enemy)

    clock   = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        # 1) Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, -10)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    if laser_sound:
                        laser_sound.play()

        # 2) Actualizar
        all_sprites.update()

        # 3) Colisiones balas-enemigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            if explosion_sound:
                explosion_sound.play()
            player.score += 100

        # 4) Colisiones jugador-enemigos
        if pygame.sprite.spritecollide(player, enemies, True):
            player.lives -= 1
            if player.lives <= 0:
                running = False

        # 5) Dibujar
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Mostrar puntuación y vidas
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {player.score}  Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

        # Check win condition
        if len(enemies) == 0:
            return True

    return False

if __name__ == '__main__':
    while True:
        win = main()
        if not game_over_screen(win=win):
            break

    pygame.quit()
