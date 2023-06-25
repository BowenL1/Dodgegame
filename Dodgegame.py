import pygame
import random
import sys
import time

# 初始化 Pygame
pygame.init()

# 游戏窗口的宽度和高度
window_width = 800
window_height = 600

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dodge game")

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# 坦克的宽度和高度
tank_width = 50
tank_height = 50

# 坦克的移动速度
tank_speed = 10

# 创建游戏时钟对象
clock = pygame.time.Clock()

# 定义坦克类
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tank_width, tank_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = tank_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            self.reset_position()

    def reset_position(self):
        self.rect.y = random.randint(-window_height, -tank_height)
        self.rect.x = random.randint(0, window_width - tank_width)

# 创建玩家坦克
player_tank = Tank(window_width // 2 - tank_width // 2, window_height - tank_height, red)

# 创建敌方坦克
enemy_tanks = pygame.sprite.Group()
for _ in range(10):
    x = random.randint(0, window_width - tank_width)
    y = random.randint(-window_height, -tank_height)
    enemy_tank = Tank(x, y, green)
    enemy_tanks.add(enemy_tank)

# 创建精灵组，并将坦克添加进去
all_sprites = pygame.sprite.Group()
all_sprites.add(player_tank)
all_sprites.add(enemy_tanks)

# 游戏是否开始的标志
game_started = False

# 游戏开始文本
font = pygame.font.SysFont(None, 48)
start_text = font.render("Press ENTER to start the game", True, white)
start_text_rect = start_text.get_rect(center=(window_width // 2, window_height // 2))

# 游戏计时器
start_time = 0

# 游戏主循环
running = True
while running:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not game_started:
                    game_started = True
                    start_time = time.time()

    # 获取玩家的键盘输入
    keys = pygame.key.get_pressed()
    if game_started:
        if keys[pygame.K_LEFT] and player_tank.rect.x > 0:
            player_tank.rect.x -= tank_speed
        if keys[pygame.K_RIGHT] and player_tank.rect.x < window_width - tank_width:
            player_tank.rect.x += tank_speed
        if keys[pygame.K_UP] and player_tank.rect.y > 0:
            player_tank.rect.y -= tank_speed
        if keys[pygame.K_DOWN] and player_tank.rect.y < window_height - tank_height:
            player_tank.rect.y += tank_speed

        # 更新敌方坦克的位置
        for enemy_tank in enemy_tanks:
            enemy_tank.update()

        # 检测玩家坦克和敌方坦克的碰撞
        if pygame.sprite.spritecollide(player_tank, enemy_tanks, False):
            print("Game Over")
            sys.exit()

    # 绘制游戏窗口
    window.fill(black)
    if game_started:
        all_sprites.draw(window)
        # 绘制计时器
        elapsed_time = int(time.time() - start_time)
        timer_text = font.render("Time: {}s".format(elapsed_time), True, white)
        window.blit(timer_text, (window_width - 150, 10))
    else:
        window.blit(start_text, start_text_rect)

    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
