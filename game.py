import pygame
from easygui import integerbox
from random import randint
import sys

# 初始化 Pygame
pygame.init()

# 游戏屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("七巧板游戏")

# 加载七巧板图像
piece_images = {
    "1x1": pygame.image.load("1x1.png").convert_alpha(),
    "1x2": pygame.image.load("1x2.png").convert_alpha(),
    "2x1": pygame.image.load("2x1.png").convert_alpha()
}

class Part(pygame.sprite.Sprite):
    def __init__(self, x, y, size, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_pos = (x, y)  # 初始位置
        self.dragging = False  # 是否正在被拖动
        self.offset_x = 0  # 鼠标点击位置与七巧板左上角的偏移量
        self.offset_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_position(self, x, y):
        self.rect.x = x - self.offset_x
        self.rect.y = y - self.offset_y

    def snap_to_grid(self):
        # 对齐到网格的步长
        grid_size = 50

        # 计算当前位置在网格上的位置
        snap_x = (self.rect.x + grid_size // 2) // grid_size * grid_size
        snap_y = (self.rect.y + grid_size // 2) // grid_size * grid_size

        # 更新七巧板位置
        self.rect.x = snap_x
        self.rect.y = snap_y

    def check_collision(self, other_parts):
        for part in other_parts:
            if part != self and self.rect.colliderect(part.rect):
                return True
        return False

def get_input():
    parts = []
    p1x1 = integerbox("请输入1x1的七巧板的个数", "输入", 4, 2, 15)
    p1x2 = integerbox("请输入1x2的七巧板的个数", "输入", 4, 2, 15)
    p2x1 = integerbox("请输入2x1的七巧板的个数", "输入", 4, 2, 15)
    for i in range(p1x1):
        parts.append(Part(randint(2, 14) * 50, randint(2, 14) * 50, "1x1", piece_images["1x1"]))
    for i in range(p2x1):
        parts.append(Part(randint(2, 14) * 50, randint(2, 14) * 50, "2x1", piece_images["2x1"]))
    for i in range(p1x2):
        parts.append(Part(randint(2, 14) * 50, randint(2, 14) * 50, "1x2", piece_images["1x2"]))
    return parts

def main():
    parts = get_input()
    parts_group = pygame.sprite.Group(parts)  # 创建一个精灵组包含所有七巧板块

    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键按下
                    for part in parts:
                        if part.rect.collidepoint(event.pos):
                            part.dragging = True
                            part.offset_x = event.pos[0] - part.rect.x
                            part.offset_y = event.pos[1] - part.rect.y
                            break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键释放
                    for part in parts:
                        if part.dragging:
                            part.snap_to_grid()  # 拖动结束时自动对齐到网格
                            if part.check_collision(parts_group.sprites()):
                                # 如果发生碰撞，将七巧板放回初始位置
                                part.rect.x, part.rect.y = part.original_pos
                            part.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                for part in parts:
                    if part.dragging:
                        part.update_position(event.pos[0], event.pos[1])

        screen.fill((255, 255, 255))  # 清屏为白色
        parts_group.draw(screen)  # 绘制所有七巧板块
        
        pygame.display.flip()  # 更新屏幕显示

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
