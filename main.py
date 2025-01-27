import sys
import time
from random import randint
import pygame
from pygame import Vector2
from database import Player, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.is_moving = False
        self.snake_graphics = {
            "snake_head_up": pygame.image.load("graphics/head_up.png").convert_alpha(),
            "snake_head_down": pygame.image.load(
                "graphics/head_down.png"
            ).convert_alpha(),
            "snake_head_right": pygame.image.load(
                "graphics/head_right.png"
            ).convert_alpha(),
            "snake_head_left": pygame.image.load(
                "graphics/head_left.png"
            ).convert_alpha(),
            "snake_tail_up": pygame.image.load("graphics/tail_up.png").convert_alpha(),
            "snake_tail_down": pygame.image.load(
                "graphics/tail_down.png"
            ).convert_alpha(),
            "snake_tail_right": pygame.image.load(
                "graphics/tail_right.png"
            ).convert_alpha(),
            "snake_tail_left": pygame.image.load(
                "graphics/tail_left.png"
            ).convert_alpha(),
            "snake_body_horizontal": pygame.image.load(
                "graphics/body_horizontal.png"
            ).convert_alpha(),
            "snake_body_vertical": pygame.image.load(
                "graphics/body_vertical.png"
            ).convert_alpha(),
            "snake_body_tr": pygame.image.load("graphics/body_tr.png").convert_alpha(),
            "snake_body_tl": pygame.image.load("graphics/body_tl.png").convert_alpha(),
            "snake_body_br": pygame.image.load("graphics/body_br.png").convert_alpha(),
            "snake_body_bl": pygame.image.load("graphics/body_bl.png").convert_alpha(),
        }

    def update_head_graphics(self, snake_rect: pygame.Rect) -> None:
        if self.body[0] - self.body[1] == Vector2(-1, 0):
            screen.blit(self.snake_graphics["snake_head_left"], snake_rect)
        elif self.body[0] - self.body[1] == Vector2(1, 0):
            screen.blit(self.snake_graphics["snake_head_right"], snake_rect)
        elif self.body[0] - self.body[1] == Vector2(0, -1):
            screen.blit(self.snake_graphics["snake_head_up"], snake_rect)
        else:
            screen.blit(self.snake_graphics["snake_head_down"], snake_rect)

    def update_tail_graphics(
        self, snake_rect: pygame.Rect, body: Vector2, tail: Vector2
    ) -> None:
        if body - tail == Vector2(1, 0):
            screen.blit(self.snake_graphics["snake_tail_left"], snake_rect)
        elif body - tail == Vector2(-1, 0):
            screen.blit(self.snake_graphics["snake_tail_right"], snake_rect)
        elif body - tail == Vector2(0, 1):
            screen.blit(self.snake_graphics["snake_tail_up"], snake_rect)
        else:
            screen.blit(self.snake_graphics["snake_tail_down"], snake_rect)

    def update_body_graphics(
        self, snake_rect, body: Vector2, left: Vector2, right: Vector2
    ) -> None:
        if (body - left) + (body - right) == Vector2(1, 1):
            screen.blit(self.snake_graphics["snake_body_tl"], snake_rect)
        elif (body - left) + (body - right) == Vector2(1, -1):
            screen.blit(self.snake_graphics["snake_body_bl"], snake_rect)
        elif (body - left) + (body - right) == Vector2(-1, 1):
            screen.blit(self.snake_graphics["snake_body_tr"], snake_rect)
        elif (body - left) + (body - right) == Vector2(-1, -1):
            screen.blit(self.snake_graphics["snake_body_br"], snake_rect)
        elif body.x - left.x == 1 or body.x - right.x == 1:
            screen.blit(self.snake_graphics["snake_body_horizontal"], snake_rect)
        else:
            screen.blit(self.snake_graphics["snake_body_vertical"], snake_rect)

    def draw_snake(self) -> None:
        for index, block in enumerate(self.body):
            snake_rect = pygame.Rect(
                int(block.x * HEIGHT), int(block.y * HEIGHT), HEIGHT, HEIGHT
            )
            if index == 0:
                self.update_head_graphics(snake_rect)
            elif index == len(self.body) - 1:
                self.update_tail_graphics(snake_rect, self.body[index - 1], block)
            else:
                self.update_body_graphics(
                    snake_rect, block, self.body[index - 1], self.body[index + 1]
                )

    def move_snake(self) -> None:
        if self.is_moving:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else:
            self.is_moving = False

    def add_block(self) -> None:
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def reset(self) -> None:
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)


class Food:
    def __init__(self) -> None:
        self.x = randint(0, WIDTH - 1)
        self.y = randint(0, WIDTH - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load("graphics/apple.png").convert_alpha()

    def draw_food(self) -> None:
        food_rect = pygame.Rect(
            int(self.pos.x * HEIGHT), int(self.pos.y * HEIGHT), HEIGHT, HEIGHT
        )
        screen.blit(self.apple, food_rect)

    def reset(self) -> None:
        self.x = randint(0, WIDTH - 1)
        self.y = randint(0, WIDTH - 1)
        self.pos = Vector2(self.x, self.y)


HEIGHT = 40
WIDTH = 20
screen = pygame.display.set_mode((HEIGHT * WIDTH, HEIGHT * WIDTH))
pygame.display.set_caption("Snake Game")
scree_color = (136, 255, 71)
snake_color = (78, 68, 255)
food_color = (255, 10, 110)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 30)
        self.level = 1
        self.game_speed = 150
        self.db_engine = create_engine("sqlite:///snake_game.db")
        Base.metadata.create_all(self.db_engine)
        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()

    def update(self) -> None:
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self) -> None:
        self.snake.draw_snake()
        self.food.draw_food()
        self.draw_score()

    def check_collision(self) -> None:
        if self.food.pos == self.snake.body[0]:
            self.food.reset()
            self.score += 1
            for block in self.snake.body:
                if block == self.food.pos:
                    self.food = Food()
            self.snake.add_block()

    def game_over(self) -> None:
        self.snake.reset()
        self.food.reset()

    def check_fail(self) -> None:
        if (not 0 <= self.snake.body[0].x < WIDTH) or (
            not 0 <= self.snake.body[0].y < WIDTH
        ):
            self.draw_game_over()
            pygame.display.flip()
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.game_over()
                            self.score = 0
                            waiting_for_input = False
                        elif event.key == pygame.K_q:
                            self.get_player_name()
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.draw_game_over()
                pygame.display.flip()
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.game_over()
                                self.score = 0
                                waiting_for_input = False
                            elif event.key == pygame.K_q:
                                self.get_player_name()
                                pygame.quit()
                                sys.exit()
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

    def pause_game(self) -> None:
        self.snake.is_moving = False
        paused = True
        clock = pygame.time.Clock()

        while paused:
            screen.fill(scree_color)
            msg = self.font.render("Pause", False, (255, 24, 9))
            msg_rect = msg.get_rect(center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2))
            screen.blit(msg, msg_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                        self.resume_game()

            clock.tick(60)

    def resume_game(self) -> None:
        self.snake.is_moving = True

    def draw_score(self) -> None:
        msg = self.font.render(f"Score: {self.score}", False, (255, 24, 9))
        msg_rect = msg.get_rect()
        msg_rect.topright = (WIDTH * HEIGHT, 0)
        screen.blit(msg, msg_rect)

    def draw_game_over(self) -> None:
        # Game Over text
        msg = self.font.render("Game Over", False, (255, 24, 9))
        msg_rect = msg.get_rect(center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 - 40))
        screen.blit(msg, msg_rect)

        # Score display
        score_text = self.font.render(f"Score: {self.score}", False, (255, 24, 9))
        score_rect = score_text.get_rect(
            center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2)
        )
        screen.blit(score_text, score_rect)

        # Options
        replay_text = self.font.render("Press R to Replay", False, (255, 24, 9))
        replay_rect = replay_text.get_rect(
            center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 + 40)
        )
        screen.blit(replay_text, replay_rect)

        quit_text = self.font.render("Press Q to Quit", False, (255, 24, 9))
        quit_rect = quit_text.get_rect(
            center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 + 80)
        )
        screen.blit(quit_text, quit_rect)

    def show_level_menu(self) -> None:
        selecting = True
        clock = pygame.time.Clock()
        levels = [(1, "Easy"), (2, "Medium"), (3, "Hard")]
        level_rects = []

        while selecting:
            screen.fill(scree_color)
            title = self.font.render("Select Level", False, (255, 24, 9))
            title_rect = title.get_rect(
                center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 - 60)
            )
            screen.blit(title, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            level_rects.clear()

            for i, (level, text) in enumerate(levels):
                level_text = self.font.render(f"{text}", False, (255, 24, 9))
                level_rect = level_text.get_rect(
                    center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 + i * 40)
                )
                level_rects.append((level_rect, level))

                # Highlight option when mouse hovers over it
                if level_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (200, 200, 200), level_rect, 2)

                screen.blit(level_text, level_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for rect, level in level_rects:
                            if rect.collidepoint(event.pos):
                                self.level = level
                                self.game_speed = (
                                    150 if level == 1 else 100 if level == 2 else 70
                                )
                                selecting = False
                                self.snake.is_moving = True
                                break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.level = 1
                        self.game_speed = 150
                        selecting = False
                    elif event.key == pygame.K_2:
                        self.level = 2
                        self.game_speed = 100
                        selecting = False
                    elif event.key == pygame.K_3:
                        self.level = 3
                        self.game_speed = 70
                        selecting = False

            clock.tick(60)

    def get_player_name(self) -> None:
        name = ""
        input_active = True
        clock = pygame.time.Clock()

        while input_active:
            screen.fill(scree_color)
            prompt = self.font.render("Enter Your Name:", False, (255, 24, 9))
            prompt_rect = prompt.get_rect(
                center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2 - 40)
            )
            screen.blit(prompt, prompt_rect)

            name_text = self.font.render(name, False, (255, 24, 9))
            name_rect = name_text.get_rect(
                center=(WIDTH * HEIGHT // 2, WIDTH * HEIGHT // 2)
            )
            screen.blit(name_text, name_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        player = Player(name=name, score=self.score)
                        self.db_session.add(player)
                        self.db_session.commit()
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 20 and event.unicode.isalnum():
                        name += event.unicode

            clock.tick(60)

    def run(self) -> None:
        self.show_level_menu()
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)
        running = True
        game_over = False
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == SCREEN_UPDATE:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.snake.direction.y != 1:
                            self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction.y != -1:
                            self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction.x != 1:
                            self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction.x != -1:
                            self.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_SPACE:
                        if self.snake.is_moving:
                            self.pause_game()
                        else:
                            self.resume_game()

            screen.fill(scree_color)
            self.draw_elements()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
