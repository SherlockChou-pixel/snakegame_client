import pygame


class GameUI:
    def __init__(self, on_action=None):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 620))
        pygame.display.set_caption("游戏界面")
        self.clock = pygame.time.Clock()
        self.running = True
        self.on_action = on_action
        self.font = pygame.font.SysFont(None, 32)
        self.small_font = pygame.font.SysFont(None, 24)

        self.map_left = 40
        self.map_top = 50
        self.map_draw_width = 500
        self.map_width = 0
        self.map_height = 0

        self.buttons = [
            {
                "action": "get_map",
                "label": "请求地图",
                "rect": pygame.Rect(620, 80, 160, 50),
                "color": (0, 120, 220),
            }
        ]

    def set_map_size(self, width, height):
        self.map_width = max(0, int(width))
        self.map_height = max(0, int(height))

    def _emit_action(self, action):
        print(f"点击按钮：{action}")
        if self.on_action:
            self.on_action(action)

    def _handle_button_click(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self._emit_action(button["action"])
                break

    def _draw_buttons(self):
        for button in self.buttons:
            rect = button["rect"]
            pygame.draw.rect(self.screen, button["color"], rect, border_radius=6)
            text = self.font.render(button["label"], True, (255, 255, 255))
            tx = rect.centerx - text.get_width() // 2
            ty = rect.centery - text.get_height() // 2
            self.screen.blit(text, (tx, ty))

    def _draw_map(self):
        title = self.font.render("地图区域", True, (40, 40, 40))
        self.screen.blit(title, (self.map_left, 15))

        if not self.map_width or not self.map_height:
            placeholder_rect = pygame.Rect(self.map_left, self.map_top, self.map_draw_width, self.map_draw_width)
            pygame.draw.rect(self.screen, (210, 210, 210), placeholder_rect, width=1)
            text = self.small_font.render("点击右侧按钮请求地图", True, (120, 120, 120))
            tx = placeholder_rect.centerx - text.get_width() // 2
            ty = placeholder_rect.centery - text.get_height() // 2
            self.screen.blit(text, (tx, ty))
            return

        cell_size = self.map_draw_width / self.map_width
        map_draw_height = cell_size * self.map_height

        outer_rect = pygame.Rect(
            round(self.map_left),
            round(self.map_top),
            round(self.map_draw_width),
            round(map_draw_height),
        )
        pygame.draw.rect(self.screen, (90, 90, 90), outer_rect, width=1)

        for row in range(self.map_height):
            for col in range(self.map_width):
                x = self.map_left + col * cell_size
                y = self.map_top + row * cell_size
                rect = pygame.Rect(round(x), round(y), round(cell_size), round(cell_size))
                pygame.draw.rect(self.screen, (220, 235, 250), rect)
                pygame.draw.rect(self.screen, (180, 180, 180), rect, width=1)

        info = self.small_font.render(
            f"地图大小: {self.map_width} x {self.map_height}    单格: {cell_size:.1f}px",
            True,
            (70, 70, 70),
        )
        self.screen.blit(info, (self.map_left, self.map_top + outer_rect.height + 12))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_button_click(event.pos)

            self.screen.fill((245, 245, 245))
            self._draw_map()
            self._draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game_ui = GameUI()
    game_ui.set_map_size(25, 25)
    game_ui.run()
