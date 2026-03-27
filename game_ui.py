import pygame


class GameUI:
    DIRECTION_KEY_MAP = {
        pygame.K_UP: 0,
        pygame.K_DOWN: 1,
        pygame.K_LEFT: 2,
        pygame.K_RIGHT: 3,
        pygame.K_w: 0,
        pygame.K_s: 1,
        pygame.K_a: 2,
        pygame.K_d: 3,
    }

    def __init__(self, on_action=None):
        pygame.init()
        self.screen = pygame.display.set_mode((980, 680))
        pygame.display.set_caption("贪吃蛇客户端")
        self.clock = pygame.time.Clock()
        self.running = True
        self.on_action = on_action

        self.title_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 34, bold=True)
        self.subtitle_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 22, bold=True)
        self.button_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 24, bold=True)
        self.info_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 18)
        self.tip_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 15)
        self.status_font = self._load_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei"], 16, bold=True)

        self.current_scene = "home"

        self.map_width = 0
        self.map_height = 0
        self.snake = []
        self.food = None
        self.room_id = ""
        self.score = 0

        self.connection_text = "未连接"
        self.connection_color = (220, 60, 60)

        self.tip_message = ""
        self.tip_color = (220, 60, 60)
        self.tip_start_time = 0
        self.tip_duration = 2500

        self.map_area = pygame.Rect(60, 120, 560, 480)
        self.scene_buttons = {
            "home": [
                {
                    "action": "join_room",
                    "label": "加入房间",
                    "rect": pygame.Rect(380, 380, 220, 64),
                    "color": (31, 123, 255),
                }
            ],
            "room": [
                {
                    "action": "start_game",
                    "label": "开始游戏",
                    "rect": pygame.Rect(720, 520, 180, 58),
                    "color": (46, 170, 95),
                }
            ],
            "game": [],
        }

    def _load_font(self, candidates, size, bold=False):
        for name in candidates:
            path = pygame.font.match_font(name)
            if path:
                font = pygame.font.Font(path, size)
                font.set_bold(bold)
                return font
        return pygame.font.SysFont(None, size, bold=bold)

    def set_scene(self, scene_name):
        self.current_scene = scene_name

    def update_room(self, room_id, score=0, snake=None):
        self.room_id = str(room_id)
        self.score = int(score or 0)
        if snake is not None:
            self.set_snake(snake)
        self.set_scene("room")

    def enter_game_scene(self):
        self.set_scene("game")

    def set_map_size(self, width, height):
        self.map_width = max(0, int(width))
        self.map_height = max(0, int(height))

    def set_snake(self, snake):
        segments = []
        if snake:
            for point in snake:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    segments.append((int(point[0]), int(point[1])))
        self.snake = segments

    def set_food(self, food):
        if not isinstance(food, dict) or "x" not in food or "y" not in food:
            self.food = None
            return
        self.food = (int(food["x"]), int(food["y"]))

    def set_score(self, score):
        self.score = int(score or 0)

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

    def _emit_action(self, action, payload=None):
        print(f"触发动作: {action}, payload={payload}")
        if self.on_action:
            self.on_action(action, payload)

    def _get_current_buttons(self):
        return self.scene_buttons.get(self.current_scene, [])

    def _handle_button_click(self, mouse_pos):
        for button in self._get_current_buttons():
            if button["rect"].collidepoint(mouse_pos):
                self._emit_action(button["action"])
                break

    def _handle_keydown(self, key):
        if self.current_scene != "game":
            return

        direction = self.DIRECTION_KEY_MAP.get(key)
        if direction is None:
            return

        self._emit_action("move", {"direction": direction})

    def _draw_card(self, rect, bg_color=(255, 255, 255), border_color=(220, 226, 232)):
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=18)
        pygame.draw.rect(self.screen, border_color, rect, width=1, border_radius=18)

    def _draw_buttons(self):
        for button in self._get_current_buttons():
            rect = button["rect"]
            pygame.draw.rect(self.screen, button["color"], rect, border_radius=14)
            text = self.button_font.render(button["label"], True, (255, 255, 255))
            self.screen.blit(
                text,
                (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2 - 1),
            )

    def _draw_connection_status(self):
        dot_x, dot_y = 860, 40
        pygame.draw.circle(self.screen, self.connection_color, (dot_x, dot_y), 7)
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
        self.screen.blit(text_surface, (60, 34))

    def _draw_home_scene(self):
        title = self.title_font.render("贪吃蛇对战大厅", True, (32, 36, 48))
        subtitle = self.info_font.render("点击下方按钮进入四人房间", True, (110, 120, 138))

        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 190))
        self.screen.blit(subtitle, (self.screen.get_width() // 2 - subtitle.get_width() // 2, 252))

        hero_rect = pygame.Rect(250, 120, 480, 380)
        self._draw_card(hero_rect, bg_color=(252, 254, 255), border_color=(221, 229, 238))

        deco_rect = pygame.Rect(300, 300, 380, 70)
        pygame.draw.rect(self.screen, (235, 244, 255), deco_rect, border_radius=16)
        deco_text = self.subtitle_font.render("当前版本：主题页 / 房间页 / 游戏页", True, (52, 92, 164))
        self.screen.blit(
            deco_text,
            (deco_rect.centerx - deco_text.get_width() // 2, deco_rect.centery - deco_text.get_height() // 2),
        )

    def _draw_room_scene(self):
        title = self.title_font.render("四人房间", True, (32, 36, 48))
        room_text = self.info_font.render(f"房间号：{self.room_id or '--'}", True, (85, 96, 114))
        note_text = self.tip_font.render("当前先按单人演示，其他位置预留。", True, (120, 128, 142))

        self.screen.blit(title, (60, 68))
        self.screen.blit(room_text, (60, 112))
        self.screen.blit(note_text, (60, 142))

        slot_width = 190
        slot_height = 180
        gap = 24
        start_x = 60
        start_y = 210

        for index in range(4):
            row = index // 2
            col = index % 2
            rect = pygame.Rect(start_x + col * (slot_width + gap), start_y + row * (slot_height + gap), slot_width, slot_height)

            if index == 0:
                self._draw_card(rect, bg_color=(239, 248, 242), border_color=(154, 216, 171))
                title_text = self.subtitle_font.render("玩家1（我）", True, (33, 88, 46))
                score_text = self.info_font.render(f"分数：{self.score}", True, (72, 92, 76))
                body_text = self.tip_font.render("已加入房间，等待开始游戏", True, (98, 110, 100))
            else:
                self._draw_card(rect, bg_color=(249, 250, 252), border_color=(224, 228, 233))
                title_text = self.subtitle_font.render(f"空位 {index + 1}", True, (130, 138, 150))
                score_text = self.info_font.render("分数：--", True, (150, 156, 166))
                body_text = self.tip_font.render("等待其他玩家加入", True, (160, 166, 176))

            self.screen.blit(title_text, (rect.x + 18, rect.y + 18))
            self.screen.blit(score_text, (rect.x + 18, rect.y + 76))
            self.screen.blit(body_text, (rect.x + 18, rect.y + 118))

        side_rect = pygame.Rect(690, 210, 220, 300)
        self._draw_card(side_rect, bg_color=(252, 254, 255), border_color=(221, 229, 238))
        info_title = self.subtitle_font.render("房间信息", True, (42, 48, 60))
        info_1 = self.info_font.render(f"房间号：{self.room_id or '--'}", True, (92, 102, 118))
        info_2 = self.info_font.render("房间类型：4人房", True, (92, 102, 118))
        info_3 = self.info_font.render("当前人数：1 / 4", True, (92, 102, 118))

        self.screen.blit(info_title, (side_rect.x + 20, side_rect.y + 24))
        self.screen.blit(info_1, (side_rect.x + 20, side_rect.y + 86))
        self.screen.blit(info_2, (side_rect.x + 20, side_rect.y + 128))
        self.screen.blit(info_3, (side_rect.x + 20, side_rect.y + 170))

    def _draw_map(self):
        title = self.title_font.render("游戏地图", True, (32, 36, 48))
        self.screen.blit(title, (self.map_area.x, 68))

        self._draw_card(
            pygame.Rect(self.map_area.x - 16, self.map_area.y - 16, self.map_area.width + 32, self.map_area.height + 32),
            bg_color=(252, 254, 255),
            border_color=(221, 229, 238),
        )

        if not self.map_width or not self.map_height:
            placeholder_rect = self.map_area
            pygame.draw.rect(self.screen, (235, 240, 245), placeholder_rect, border_radius=10)
            text = self.info_font.render("开始游戏后，正在等待地图数据...", True, (120, 120, 120))
            self.screen.blit(
                text,
                (placeholder_rect.centerx - text.get_width() // 2, placeholder_rect.centery - text.get_height() // 2),
            )
            return

        cell_size = min(self.map_area.width / self.map_width, self.map_area.height / self.map_height)
        draw_width = cell_size * self.map_width
        draw_height = cell_size * self.map_height
        offset_x = self.map_area.x + (self.map_area.width - draw_width) / 2
        offset_y = self.map_area.y + (self.map_area.height - draw_height) / 2

        outer_rect = pygame.Rect(round(offset_x), round(offset_y), round(draw_width), round(draw_height))
        pygame.draw.rect(self.screen, (86, 92, 104), outer_rect, width=1, border_radius=4)

        for row in range(self.map_height):
            for col in range(self.map_width):
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                rect = pygame.Rect(round(x), round(y), round(cell_size), round(cell_size))
                pygame.draw.rect(self.screen, (232, 242, 249), rect)
                pygame.draw.rect(self.screen, (205, 214, 224), rect, width=1)

        if self.food is not None:
            food_x, food_y = self.food
            if 0 <= food_x < self.map_width and 0 <= food_y < self.map_height:
                x = offset_x + food_x * cell_size
                y = offset_y + food_y * cell_size
                center = (round(x + cell_size / 2), round(y + cell_size / 2))
                radius = max(4, round(cell_size * 0.32))
                pygame.draw.circle(self.screen, (235, 76, 76), center, radius)
                pygame.draw.circle(self.screen, (188, 38, 38), center, radius, width=1)

        for index, (snake_x, snake_y) in enumerate(self.snake):
            if snake_x < 0 or snake_x >= self.map_width or snake_y < 0 or snake_y >= self.map_height:
                continue

            x = offset_x + snake_x * cell_size
            y = offset_y + snake_y * cell_size
            rect = pygame.Rect(round(x), round(y), round(cell_size), round(cell_size))
            color = (41, 163, 90) if index == len(self.snake) - 1 else (81, 196, 112)
            pygame.draw.rect(self.screen, color, rect, border_radius=max(2, round(cell_size * 0.18)))
            pygame.draw.rect(self.screen, (33, 117, 66), rect, width=1, border_radius=max(2, round(cell_size * 0.18)))

        info = self.info_font.render(
            f"地图：{self.map_width} x {self.map_height}    分数：{self.score}    蛇长：{len(self.snake)}",
            True,
            (80, 88, 98),
        )
        self.screen.blit(info, (self.map_area.x, self.map_area.bottom + 26))

    def _draw_game_scene(self):
        self._draw_map()

        side_rect = pygame.Rect(680, 120, 240, 330)
        self._draw_card(side_rect, bg_color=(252, 254, 255), border_color=(221, 229, 238))

        title = self.subtitle_font.render("当前信息", True, (42, 48, 60))
        room_text = self.info_font.render(f"房间号：{self.room_id or '--'}", True, (92, 102, 118))
        score_text = self.info_font.render(f"分数：{self.score}", True, (92, 102, 118))
        snake_text = self.info_font.render(f"蛇身长度：{len(self.snake)}", True, (92, 102, 118))
        food_text = self.info_font.render(
            f"食物：{self.food if self.food is not None else '--'}",
            True,
            (92, 102, 118),
        )
        note_1 = self.tip_font.render("方向键 / WASD：发送移动指令", True, (120, 128, 142))
        note_2 = self.tip_font.render("移动结果以后端推送状态为准。", True, (120, 128, 142))

        self.screen.blit(title, (side_rect.x + 20, side_rect.y + 22))
        self.screen.blit(room_text, (side_rect.x + 20, side_rect.y + 84))
        self.screen.blit(score_text, (side_rect.x + 20, side_rect.y + 126))
        self.screen.blit(snake_text, (side_rect.x + 20, side_rect.y + 168))
        self.screen.blit(food_text, (side_rect.x + 20, side_rect.y + 210))
        self.screen.blit(note_1, (side_rect.x + 20, side_rect.y + 266))
        self.screen.blit(note_2, (side_rect.x + 20, side_rect.y + 290))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_button_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event.key)

            self.screen.fill((244, 247, 251))

            if self.current_scene == "home":
                self._draw_home_scene()
            elif self.current_scene == "room":
                self._draw_room_scene()
            elif self.current_scene == "game":
                self._draw_game_scene()

            self._draw_buttons()
            self._draw_connection_status()
            self._draw_tip_message()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.update_room("Room0", score=0, snake=[[18, 8], [18, 7], [18, 6]])
    game_ui.set_map_size(25, 25)
    game_ui.set_food({"x": 1, "y": 4})
    game_ui.enter_game_scene()
    game_ui.show_message("演示界面")
    game_ui.run()
