import pygame
from easygui import ynbox, buttonbox
from random import randint
import sys
from collections import deque

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
parts = []


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

    def get_new_place(self):
        # 使用广度优先搜索寻找空闲位置
        visited = set()
        queue = deque([(randint(2, SCREEN_WIDTH // 50 - 4), randint(2, SCREEN_HEIGHT // 50 - 4))])  # 随机起始位置
        while queue:
            x, y = queue.popleft()
            new_rect = pygame.Rect(x * 50, y * 50, self.rect.width, self.rect.height)
            if not any(new_rect.colliderect(part.rect) for part in parts if part != self):
                self.rect.x = new_rect.x
                self.rect.y = new_rect.y
                return
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited and 1 <= nx < SCREEN_WIDTH // 50 - 4 and 1 <= ny < SCREEN_HEIGHT // 50 - 4:
                        queue.append((nx, ny))
        # 如果没有找到合适的位置，保持在原地
        self.rect.x = self.original_pos[0]
        self.rect.y = self.original_pos[1]


level = {
    '1': {"50": 4, "50x100": 3, "100x50": 1, "width": 3, "high": 4},
    '2': {"50": 4, "50x100": 3, "100x50": 5, "width": 5, "high": 4},
    '3': {"50": 6, "100x50": 5, "50x100": 4, "width": 6, "high": 4},
    '4': {"50": 10, "100x50": 7, "50x100": 9, "width": 7, "high": 6}
}


def get_input():
    global parts, target_rect
    parts = []  # 清空七巧板块列表，避免重复添加
    if ynbox("是否想要使用预设？", "选择", ("是", "否")):
        t = buttonbox("请选择一个预设", "预设", ("1", "2", "3", "4"))
        preset = level[str(t)]
        p1x1 = preset["50"]
        p1x2 = preset["50x100"]
        p2x1 = preset["100x50"]
        target_width = preset["width"] * 50
        target_height = preset["high"] * 50
    else:
        total_area = randint(8000, 20000)  # 随机设置总面积
        p1x1 = randint(2, 15)
        p1x2 = randint(2, 15)
        p2x1 = randint(2, 15)

        # 重新计算总面积以匹配随机数量的七巧板
        total_area = p1x1 * 50 * 50 + p1x2 * 50 * 100 + p2x1 * 100 * 50

        target_width = randint(3, 7) * 50
        target_height = (total_area // target_width) // 50 * 50

    # 确保目标区域不会超出屏幕边界
    target_width = min(target_width, SCREEN_WIDTH)
    target_height = min(target_height, SCREEN_HEIGHT)

    # 生成七巧板块并确保它们不重叠
    for i in range(p1x1):
        part = Part(randint(2, SCREEN_WIDTH // 50 - 4) * 50, randint(2, SCREEN_HEIGHT // 50 - 4) * 50, "1x1",
                    piece_images["1x1"])
        while part.check_collision(parts):
            part.rect.x = randint(2, SCREEN_WIDTH // 50 - 4) * 50
            part.rect.y = randint(2, SCREEN_HEIGHT // 50 - 4) * 50
        parts.append(part)

    for i in range(p2x1):
        part = Part(randint(2, SCREEN_WIDTH // 50 - 4) * 50, randint(2, SCREEN_HEIGHT // 50 - 4) * 50, "2x1",
                    piece_images["2x1"])
        while part.check_collision(parts):
            part.rect.x = randint(2, SCREEN_WIDTH // 50 - 4) * 50
            part.rect.y = randint(2, SCREEN_HEIGHT // 50 - 4) * 50
        parts.append(part)

    for i in range(p1x2):
        part = Part(randint(2, SCREEN_WIDTH // 50 - 4) * 50, randint(2, SCREEN_HEIGHT // 50 - 4) * 50, "1x2",
                    piece_images["1x2"])
        while part.check_collision(parts):
            part.rect.x = randint(2, SCREEN_WIDTH // 50 - 4) * 50
            part.rect.y = randint(2, SCREEN_HEIGHT // 50 - 4) * 50
        parts.append(part)

    # 对目标区域进行对齐到网格处理
    target_rect = pygame.Rect((SCREEN_WIDTH - target_width) // 2, (SCREEN_HEIGHT - target_height) // 2, target_width,
                              target_height)
    target_rect.x = (target_rect.x + 25) // 50 * 50
    target_rect.y = (target_rect.y + 25) // 50 * 50
    target_rect.width = (target_rect.width + 25) // 50 * 50
    target_rect.height = (target_rect.height + 25) // 50 * 50

    return parts


def check_success(parts, target_rect):
    # 检查所有七巧板块是否填满目标区域且没有重叠
    filled_cells = set()
    for part in parts:
        for x in range(part.rect.width // 50):
            for y in range(part.rect.height // 50):
                cell = (part.rect.x + x * 50, part.rect.y + y * 50)
                if target_rect.collidepoint(cell):
                    filled_cells.add(cell)

    # 检查是否填满目标区域
    target_cells = set((x, y) for x in range(target_rect.left, target_rect.right, 50)
                       for y in range(target_rect.top, target_rect.bottom, 50))
    return filled_cells == target_cells


def main():
    parts = get_input()
    parts_group = pygame.sprite.Group(parts)  # 创建一个精灵组包含所有七巧板块

    # 主循环
    running = True
    game_success = False
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
                                # 如果发生碰撞，将七巧板放到可放置位置
                                part.get_new_place()
                            part.dragging = False
                            # 检查是否填满目标区域
                            if check_success(parts, target_rect):
                                game_success = True

            elif event.type == pygame.MOUSEMOTION:
                for part in parts:
                    if part.dragging:
                        part.update_position(event.pos[0], event.pos[1])

        screen.fill((255, 255, 255))  # 清屏为白色
        parts_group.draw(screen)  # 绘制所有七巧板块

        # 绘制目标区域
        pygame.draw.rect(screen, (0, 255, 0), target_rect, 2)

        if game_success:
            parts_group.draw(screen)  # 绘制所有七巧板块
            pygame.display.flip()  # 更新屏幕显示
            pygame.time.wait(750)
            screen.fill((255, 255, 255))  # 清屏为白色
            font = pygame.font.Font("XHei_Intel.ttc", 74)
            text = font.render("游戏成功!", True, (0, 255, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()  # 更新屏幕显示
            pygame.time.wait(2000)  # 等待2秒
            running = False  # 退出游戏循环

        pygame.display.flip()  # 更新屏幕显示

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
