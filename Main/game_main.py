import pygame
import random
import json
import os
from ufo import Enemy

# SCREEN SET --> WIDTH --> HEIGHT --> FPS
WIDTH = 600
HEIGHT = 1024
FPS = 60

# SET GAME SETTINGS
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездный корабль")
clock = pygame.time.Clock()

# RGB COLOR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Load sounds
try:
    shoot_sound = pygame.mixer.Sound('content_game/Bonus/sfx_laser1.ogg')
    hit_sound = pygame.mixer.Sound('content_game/Bonus/sfx_zap.ogg')
    death_sound = pygame.mixer.Sound('content_game/Bonus/sfx_lose.ogg')
    shoot_sound.set_volume(0.3)
    hit_sound.set_volume(0.4)
    death_sound.set_volume(0.5)
except:
    print("Warning: Could not load sounds")
    shoot_sound = hit_sound = death_sound = None

# Load background music
try:
    # Используем один из звуковых эффектов как фоновую музыку (можно заменить на музыкальный файл)
    pygame.mixer.music.load('content_game/Bonus/sfx_twoTone.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # -1 для бесконечного повтора
except:
    print("Warning: Could not load background music")

# Load font - используем системный шрифт для поддержки кириллицы
try:
    # Пробуем найти системный шрифт с поддержкой кириллицы
    font = pygame.font.SysFont('arial', 24)
    big_font = pygame.font.SysFont('arial', 48, bold=True)
    medium_font = pygame.font.SysFont('arial', 32)
except:
    # Если не получилось, используем шрифт по умолчанию
    font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 48)
    medium_font = pygame.font.Font(None, 32)

# Load images
bg_image = pygame.image.load('content_game/Backgrounds/nebula600x1024.jpg').convert()
space_ship = pygame.image.load('content_game/PNG/playerShip3_blue.png')
explosion_images = [
    pygame.image.load('content_game/PNG/Effects/fire00.png'),
    pygame.image.load('content_game/PNG/Effects/fire01.png'),
    pygame.image.load('content_game/PNG/Effects/fire02.png'),
    pygame.image.load('content_game/PNG/Effects/fire03.png'),
    pygame.image.load('content_game/PNG/Effects/fire04.png'),
]


class Star:
    """Класс звезды для параллакс эффекта"""
    def __init__(self):
        self.x = random.randrange(0, WIDTH)
        self.y = random.randrange(0, HEIGHT)
        self.speed = random.uniform(0.5, 3)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randrange(0, WIDTH)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


class Particle:
    """Класс частицы для эффектов"""
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.size = random.randint(2, 5)
        self.color = color if color else random.choice([YELLOW, RED, (255, 150, 0)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # гравитация
        self.life -= 1

    def is_alive(self):
        return self.life > 0

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)


class Laser(pygame.sprite.Sprite):
    """Класс лазерного выстрела"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('content_game/PNG/Lasers/laserBlue01.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        # Удалить лазер если он вышел за экран
        if self.rect.bottom < 0:
            self.kill()


class Explosion:
    """Класс анимации взрыва"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

    def is_done(self):
        return self.frame >= len(explosion_images)

    def draw(self, screen):
        if not self.is_done():
            img = explosion_images[self.frame]
            rect = img.get_rect(center=(self.x, self.y))
            screen.blit(img, rect)


def create_enemies(wave=1):
    """Создает список врагов в зависимости от волны"""
    num_enemies = min(4 + wave, 10)  # Максимум 10 врагов
    enemy_types = [
        'content_game/PNG/Enemies/enemyGreen2.png',
        'content_game/PNG/Enemies/enemyBlue1.png',
        'content_game/PNG/Enemies/enemyRed2.png',
        'content_game/PNG/Enemies/enemyBlack5.png',
    ]

    enemies = []
    for i in range(num_enemies):
        x = random.randrange(50, WIDTH - 50)
        speed = random.randrange(2, 4 + wave // 2)  # Скорость увеличивается с волнами
        enemy_type = random.choice(enemy_types)
        enemies.append(Enemy(x, speed, enemy_type))

    return enemies


def load_highscore():
    """Загрузить рекорд из файла"""
    try:
        if os.path.exists('highscore.json'):
            with open('highscore.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('highscore', 0)
    except:
        pass
    return 0


def save_highscore(score):
    """Сохранить рекорд в файл"""
    try:
        with open('highscore.json', 'w', encoding='utf-8') as f:
            json.dump({'highscore': score}, f)
    except:
        print("Warning: Could not save highscore")


def reset_game(wave=1):
    """Сбросить игру в начальное состояние"""
    player_x = WIDTH // 2
    player_y = HEIGHT - 100
    lives = 3
    score = 0
    lasers = pygame.sprite.Group()
    enemies = create_enemies(wave)
    explosions = []
    particles = []
    invulnerable_time = 0
    return player_x, player_y, lives, score, lasers, enemies, explosions, invulnerable_time, particles, wave


def draw_main_menu(screen, highscore):
    """Отрисовка главного меню"""
    screen.blit(bg_image, (0, 0))

    title_text = big_font.render('ЗВЕЗДНЫЙ КОРАБЛЬ', True, CYAN)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_text, title_rect)

    start_text = medium_font.render('Нажмите ENTER для начала', True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_rect)

    highscore_text = font.render(f'Рекорд: {highscore}', True, YELLOW)
    highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(highscore_text, highscore_rect)

    controls_texts = [
        'Управление:',
        'Стрелки - Движение',
        'Пробел - Стрельба',
        'ESC - Пауза',
    ]

    y_offset = HEIGHT - 250
    for text in controls_texts:
        txt = font.render(text, True, WHITE)
        txt_rect = txt.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(txt, txt_rect)
        y_offset += 30


def draw_pause_menu(screen, score, wave):
    """Отрисовка меню паузы"""
    # Полупрозрачный фон
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    pause_text = big_font.render('ПАУЗА', True, YELLOW)
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(pause_text, pause_rect)

    score_text = font.render(f'Счет: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)

    wave_text = font.render(f'Волна: {wave}', True, WHITE)
    wave_rect = wave_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(wave_text, wave_rect)

    continue_text = font.render('ESC - Продолжить', True, GREEN)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(continue_text, continue_rect)


# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3

# Initialize game
game_state = STATE_MENU
highscore = load_highscore()
player_x, player_y, lives, score, lasers, enemies, explosions, invulnerable_time, particles, wave = reset_game()
speed = 8
last_shot_time = 0
shoot_cooldown = 250

# Create stars for parallax effect
stars = [Star() for _ in range(100)]

# START
RUN_GAME_FLAG = True
while RUN_GAME_FLAG:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN_GAME_FLAG = False
            exit()

        if event.type == pygame.KEYDOWN:
            # Главное меню
            if game_state == STATE_MENU:
                if event.key == pygame.K_RETURN:
                    player_x, player_y, lives, score, lasers, enemies, explosions, invulnerable_time, particles, wave = reset_game()
                    game_state = STATE_PLAYING

            # Игра
            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_PAUSED

                # Стрельба на пробел
                if event.key == pygame.K_SPACE:
                    if current_time - last_shot_time > shoot_cooldown:
                        laser = Laser(player_x, player_y - 20)
                        lasers.add(laser)
                        last_shot_time = current_time
                        if shoot_sound:
                            shoot_sound.play()
                        # Добавляем частицы при выстреле
                        for _ in range(5):
                            particles.append(Particle(player_x, player_y - 20, CYAN))

            # Пауза
            elif game_state == STATE_PAUSED:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_PLAYING

            # Game Over
            elif game_state == STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    player_x, player_y, lives, score, lasers, enemies, explosions, invulnerable_time, particles, wave = reset_game()
                    game_state = STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU

    # Обновление и отрисовка звезд (параллакс фон)
    screen.blit(bg_image, (0, 0))
    for star in stars:
        if game_state == STATE_PLAYING:
            star.update()
        star.draw(screen)

    # Главное меню
    if game_state == STATE_MENU:
        draw_main_menu(screen, highscore)

    # Пауза
    elif game_state == STATE_PAUSED:
        # Отрисовываем игру под паузой
        space_ship_rect = space_ship.get_rect(center=(player_x, player_y))
        screen.blit(space_ship, space_ship_rect)

        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        lasers.draw(screen)

        for explosion in explosions:
            explosion.draw(screen)

        # Отображение счета и жизней
        score_text = font.render(f'СЧЕТ: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f'ЖИЗНИ: {lives}', True, WHITE)
        screen.blit(lives_text, (10, 40))

        wave_text = font.render(f'ВОЛНА: {wave}', True, WHITE)
        screen.blit(wave_text, (10, 70))

        # Меню паузы поверх
        draw_pause_menu(screen, score, wave)

    # Игра
    elif game_state == STATE_PLAYING:
        # Получаем прямоугольник корабля для коллизий
        space_ship_rect = space_ship.get_rect(center=(player_x, player_y))

        # Проверка неуязвимости
        is_invulnerable = current_time < invulnerable_time

        # Мигание при неуязвимости
        if not is_invulnerable or (current_time // 100) % 2 == 0:
            screen.blit(space_ship, space_ship_rect)

        # Управление кораблем
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= speed
        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_UP]:
            player_y -= speed
        if keys[pygame.K_DOWN]:
            player_y += speed

        # Границы экрана
        ship_half_width = space_ship.get_width() // 2
        ship_half_height = space_ship.get_height() // 2

        if player_x - ship_half_width < 0:
            player_x = ship_half_width
        if player_x + ship_half_width > WIDTH:
            player_x = WIDTH - ship_half_width
        if player_y - ship_half_height < 0:
            player_y = ship_half_height
        if player_y + ship_half_height > HEIGHT:
            player_y = HEIGHT - ship_half_height

        # Обновляем и рисуем лазеры
        lasers.update()
        lasers.draw(screen)

        # Проверка столкновений лазеров с врагами
        for laser in lasers:
            for enemy in enemies:
                if laser.rect.colliderect(enemy.rect):
                    # Создаем взрыв
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    # Создаем частицы
                    for _ in range(15):
                        particles.append(Particle(enemy.rect.centerx, enemy.rect.centery))
                    # Увеличиваем счет
                    score += 10
                    # Удаляем врага
                    enemies.remove(enemy)
                    # Удаляем лазер
                    laser.kill()
                    if hit_sound:
                        hit_sound.play()
                    break

        # Проверка на столкновение с врагами
        if not is_invulnerable:
            for enemy in enemies:
                if space_ship_rect.colliderect(enemy.rect):
                    lives -= 1
                    # Создаем взрыв
                    explosions.append(Explosion(player_x, player_y))
                    # Создаем частицы
                    for _ in range(20):
                        particles.append(Particle(player_x, player_y, RED))
                    # Неуязвимость на 2 секунды
                    invulnerable_time = current_time + 2000
                    # Удаляем врага
                    enemies.remove(enemy)
                    if death_sound:
                        death_sound.play()

                    if lives <= 0:
                        game_state = STATE_GAME_OVER
                        # Обновляем рекорд
                        if score > highscore:
                            highscore = score
                            save_highscore(highscore)
                    break

        # Проверка на завершение волны
        if len(enemies) == 0:
            wave += 1
            enemies = create_enemies(wave)

        # Обновляем и рисуем врагов
        for enemy in enemies:
            enemy.update(HEIGHT)
            screen.blit(enemy.image, enemy.rect)

        # Обновляем и рисуем взрывы
        for explosion in explosions[:]:
            explosion.update()
            if explosion.is_done():
                explosions.remove(explosion)
            else:
                explosion.draw(screen)

        # Обновляем и рисуем частицы
        for particle in particles[:]:
            particle.update()
            if not particle.is_alive():
                particles.remove(particle)
            else:
                particle.draw(screen)

        # Отображение счета
        score_text = font.render(f'СЧЕТ: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Отображение жизней
        lives_text = font.render(f'ЖИЗНИ: {lives}', True, WHITE)
        screen.blit(lives_text, (10, 40))

        # Отображение волны
        wave_text = font.render(f'ВОЛНА: {wave}', True, WHITE)
        screen.blit(wave_text, (10, 70))

    # Game Over экран
    elif game_state == STATE_GAME_OVER:
        game_over_text = big_font.render('GAME OVER', True, RED)
        score_text = font.render(f'ИТОГОВЫЙ СЧЕТ: {score}', True, WHITE)
        wave_text = font.render(f'Достигнута волна: {wave}', True, WHITE)
        highscore_text = font.render(f'РЕКОРД: {highscore}', True, YELLOW)
        restart_text = font.render('R - Перезапуск | ESC - Меню', True, GREEN)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        wave_rect = wave_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(wave_text, wave_rect)
        screen.blit(highscore_text, highscore_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()
