import pygame


class GameUI:
    def __init__(self, on_action=None):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 620))
        pygame.display.set_caption("游戏界面")
        self.clock = pygame.time.Clock()
        self.running = True
        self.on_action = on_action

        self.title_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 22, bold=True)
        self.button_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 24, bold=True)
        self.info_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 16)
        self.tip_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 14)
        self.status_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 15, bold=True)

        self.map_left = 40
        self.map_top = 56
        self.map_draw_width = 500
        self.map_width = 0
        self.map_height = 0

        self.tip_message = ""
        self.tip_color = (220, 60, 60)
        self.tip_start_time = 0
        self.tip_duration = 2500

        self.connection_text = "未连接"
        self.connection_color = (220, 60, 60)

        self.buttons = [
            {
                "action": "get_map",
                "label": "请求地图",
                "rect": pygame.Rect(620, 88, 180, 56),
                "color": (24, 126, 223),
            }
        ]

    def _load_font(self, candidates, size, bold=False):
        for name in candidates:
            path = pygame.font.match_font(name)
            if path:
                font = pygame.font.Font(path, size)
                font.set_bold(bold)
                return font
        return pygame.font.SysFont(None, size, bold=bold)

    def set_map_size(self, width, height):
        self.map_width = max(0, int(width))
        self.map_height = max(0, int(height))

    def set_connection_status(self, connected):
        if connected:
            self.connection_text = "已连接"
            self.connection_color = (60, 160, 90)
        else:
            self.connection_text = "未连接"
            self.connection_color = (220, 60, 60)

    def show_message(self, message, color=(220, 60, 60), duration=2500):
        self.tip_message = str(message)
        self.tip_color = color
        self.tip_duration = duration
        self.tip_start_time = pygame.time.get_ticks()

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
            pygame.draw.rect(self.screen, button["color"], rect, border_radius=8)
            text = self.button_font.render(button["label"], True, (255, 255, 255))
            tx = rect.centerx - text.get_width() // 2
            ty = rect.centery - text.get_height() // 2 - 1
            self.screen.blit(text, (tx, ty))

    def _draw_connection_status(self):
        dot_x, dot_y = 626, 40
        pygame.draw.circle(self.screen, self.connection_color, (dot_x, dot_y), 6)
        text = self.status_font.render(self.connection_text, True, (70, 70, 70))
        self.screen.blit(text, (dot_x + 14, dot_y - text.get_height() // 2))

    def _draw_tip_message(self):
        if not self.tip_message:
            return

        elapsed = pygame.time.get_ticks() - self.tip_start_time
        if elapsed >= self.tip_duration:
            self.tip_message = ""
            return

        fade_ratio = 1 - elapsed / self.tip_duration
        alpha = max(0, min(255, int(255 * fade_ratio)))

        text_surface = self.tip_font.render(self.tip_message, True, self.tip_color)
        text_surface.set_alpha(alpha)
        self.screen.blit(text_surface, (620, 154))

    def _draw_map(self):
        title = self.title_font.render("地图区域", True, (48, 48, 48))
        self.screen.blit(title, (self.map_left, 18))

        if not self.map_width or not self.map_height:
            placeholder_rect = pygame.Rect(self.map_left, self.map_top, self.map_draw_width, self.map_draw_width)
            pygame.draw.rect(self.screen, (210, 210, 210), placeholder_rect, width=1)
            text = self.info_font.render("点击右侧按钮请求地图", True, (120, 120, 120))
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

        info = self.info_font.render(
            f"地图大小: {self.map_width} x {self.map_height}    单格: {cell_size:.1f}px",
            True,
            (80, 80, 80),
        )
        self.screen.blit(info, (self.map_left, self.map_top + outer_rect.height + 16))

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
            self._draw_connection_status()
            self._draw_tip_message()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game_ui = GameUI()
    game_ui.set_map_size(25, 25)
    game_ui.show_message("服务器未连接")
    game_ui.run()
