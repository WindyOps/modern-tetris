import pygame
import random

pygame.init()
pygame.key.set_repeat(200, 50)   # 按住时连续触发

# ---------- 常量 ----------
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
}

SHAPES = [
    [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],  # I
    [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]],  # O
    [[0,0,0,0], [0,1,0,0], [1,1,1,0], [0,0,0,0]],  # T
    [[0,0,0,0], [0,1,1,0], [1,1,0,0], [0,0,0,0]],  # S
    [[0,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,0]],  # Z
    [[0,0,0,0], [1,0,0,0], [1,1,1,0], [0,0,0,0]],  # L
    [[0,0,0,0], [0,0,1,0], [1,1,1,0], [0,0,0,0]],  # J
]

SHAPE_COLORS = [
    COLORS['cyan'], COLORS['yellow'], COLORS['magenta'],
    COLORS['green'], COLORS['red'], COLORS['orange'], COLORS['blue']
]

# ---------- 游戏类 ----------
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)

        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 300
        self.game_over = False

        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2
        self.piece_y = 0

    def new_piece(self):
        idx = random.randint(0, len(SHAPES)-1)
        return {'shape': [row[:] for row in SHAPES[idx]], 'color': SHAPE_COLORS[idx]}

    def rotate_piece(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def check_collision(self, shape, dx, dy):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.piece_x + x + dx
                    ny = self.piece_y + y + dy
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT or (ny >= 0 and self.grid[ny][nx] != 0):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    gy = self.piece_y + y
                    gx = self.piece_x + x
                    if gy >= 0:
                        self.grid[gy][gx] = self.current_piece['color']

        lines_removed = 0
        for y in range(GRID_HEIGHT-1, -1, -1):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                del self.grid[y]
                self.grid.insert(0, [0]*GRID_WIDTH)
                lines_removed += 1

        if lines_removed:
            self.lines_cleared += lines_removed
            scores = {1:100, 2:300, 3:500, 4:800}
            self.score += scores.get(lines_removed, 0) * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(100, 300 - (self.level-1) * 20)

        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2
        self.piece_y = 0
        if self.check_collision(self.current_piece['shape'], 0, 0):
            self.game_over = True

    def hard_drop(self):
        while not self.check_collision(self.current_piece['shape'], 0, 1):
            self.piece_y += 1
        self.merge_piece()

    def move(self, dx, dy):
        if not self.check_collision(self.current_piece['shape'], dx, dy):
            self.piece_x += dx
            self.piece_y += dy
            return True
        if dy == 1:
            self.merge_piece()
        return False

    def rotate(self):
        rotated = self.rotate_piece(self.current_piece['shape'])
        if not self.check_collision(rotated, 0, 0):
            self.current_piece['shape'] = rotated
        else:
            for dx in (-1, 1):
                if not self.check_collision(rotated, dx, 0):
                    self.current_piece['shape'] = rotated
                    self.piece_x += dx
                    break

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if color != 0:
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, COLORS['gray'], rect, 1)
                else:
                    pygame.draw.rect(self.screen, COLORS['black'], rect)
                    pygame.draw.rect(self.screen, COLORS['gray'], rect, 1)

    def draw_piece(self, piece, ox=0, oy=0, ghost=False):
        shape = piece['shape']
        color = piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((ox+x)*BLOCK_SIZE, (oy+y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if ghost:
                        pygame.draw.rect(self.screen, COLORS['gray'], rect, 2)
                    else:
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, COLORS['gray'], rect, 1)

    def draw_ghost(self):
        gy = self.piece_y
        while not self.check_collision(self.current_piece['shape'], 0, gy - self.piece_y + 1):
            gy += 1
        self.draw_piece(self.current_piece, self.piece_x, gy, ghost=True)

    def draw_info(self):
        info_x = GRID_WIDTH * BLOCK_SIZE + 20
        y = 20

        label = self.font.render("Next:", True, COLORS['white'])
        self.screen.blit(label, (info_x, y))
        y += 40
        next_shape = self.next_piece['shape']
        next_color = self.next_piece['color']
        for row in range(len(next_shape)):
            for col in range(len(next_shape[0])):
                if next_shape[row][col]:
                    rect = pygame.Rect(info_x + col*25, y + row*25, 25, 25)
                    pygame.draw.rect(self.screen, next_color, rect)
                    pygame.draw.rect(self.screen, COLORS['gray'], rect, 1)

        y += 120
        for text in (f"Score: {self.score}", f"Level: {self.level}", f"Lines: {self.lines_cleared}"):
            surf = self.font.render(text, True, COLORS['white'])
            self.screen.blit(surf, (info_x, y))
            y += 40

        y += 80
        tips = [
            "W / Up    Rotate",
            "A / Left  Move Left",
            "D / Right Move Right",
            "S / Down  Soft Drop",
            "Space     Hard Drop",
            "R         Restart"
        ]
        for tip in tips:
            surf = self.font.render(tip, True, COLORS['gray'])
            self.screen.blit(surf, (info_x, y))
            y += 30

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['black'])
        self.screen.blit(overlay, (0, 0))

        text = self.big_font.render("GAME OVER", True, COLORS['red'])
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, rect)

        restart = self.font.render("Press R to Restart", True, COLORS['white'])
        rect2 = restart.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(restart, rect2)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            # 打印每一帧所有事件（谨慎，可能会刷屏，但能抓住问题）
            for event in pygame.event.get():
                print(f"[EVENT] {event}")  # 打印所有事件对象

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    print(
                        f"[KEYDOWN] key={event.key} ({pygame.key.name(event.key)}), mod={event.mod}, game_over={self.game_over}")

                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            print("[DEBUG] 重置游戏")
                        else:
                            print("[DEBUG] 游戏结束，忽略按键")
                        continue

                    # 映射所有键，包括未映射的（都会打印）
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        print("  -> 左移")
                        self.move(-1, 0)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        print("  -> 右移")
                        self.move(1, 0)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        print("  -> 加速下落")
                        self.move(0, 1)
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        print("  -> 旋转")
                        self.rotate()
                    elif event.key == pygame.K_SPACE:
                        print("  -> 硬降")
                        self.hard_drop()
                    elif event.key == pygame.K_r:
                        print("  -> 重启")
                        self.reset_game()
                    else:
                        print(f"  -> 未映射键，忽略（但继续处理）")
                        # 注意：这里不 continue，让后续方向键也能正常处理
                elif event.type == pygame.KEYUP:
                    print(f"[KEYUP] key={event.key} ({pygame.key.name(event.key)})")
                elif event.type == pygame.ACTIVEEVENT:
                    print(f"[ACTIVEEVENT] {event}")
                elif event.type == pygame.VIDEOEXPOSE:
                    print("[VIDEOEXPOSE]")
                else:
                    # 其他事件（如鼠标等）
                    print(f"[OTHER] {event}")

            if not self.game_over:
                self.fall_time += dt
                if self.fall_time >= self.fall_speed:
                    self.move(0, 1)
                    self.fall_time = 0

            # 绘制...
            self.screen.fill(COLORS['black'])
            self.draw_grid()
            if not self.game_over:
                self.draw_ghost()
                self.draw_piece(self.current_piece, self.piece_x, self.piece_y)
            self.draw_info()
            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
        pygame.quit()

# ---------- 启动 ----------
if __name__ == "__main__":
    game = Tetris()
    game.run()