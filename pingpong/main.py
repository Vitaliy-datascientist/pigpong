import sys
import random
import time
import os
import pygame

pygame.init()

BASE_DIR = os.path.dirname(__file__)

FONT1 = pygame.font.SysFont("stxingkai", 100)
FONT2 = pygame.font.SysFont("stxingkai", 50)
FONT3 = pygame.font.SysFont("stxingkai", 25)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREY = (190, 190, 190)


class Screen:
    icon = pygame.image.load(f"{BASE_DIR}/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Ping-Pong")

    def __init__(self):
        self.width = 900
        self.height = 500
        self.size = (self.width, self.height)
        self.display = pygame.display.set_mode(self.size)
        self.end_text1 = True
        self.end_text2 = True
        self.player_blue_win = False
        self.player_red_win = False
        self.text_menu1_rect = (20, 70)
        self.text_menu2_rect = (20, 174)
        self.text_menu3_rect = (20, 278)
        self.text_menu4_rect = (20, 382)
        self.text_menu1_size = FONT2.size("STANDARD")
        self.text_menu2_size = FONT2.size("CUSTOM")
        self.text_menu3_size = FONT2.size("STANDARD WITH BOT")
        self.text_menu4_size = FONT2.size("CUSTOM WITH BOT")
        self.text_menu5_size = FONT1.size("PING")
        self.text_menu6_size = FONT1.size("PONG")
        self.sound_menu = pygame.mixer.Sound(f"{BASE_DIR}/sound_menu.wav")
        self.sound_game_over = pygame.mixer.Sound(f"{BASE_DIR}/game_over_sound.wav")

    def menu(self):
        self.display.blit(FONT2.render("STANDARD", True, GREY), self.text_menu1_rect)
        self.display.blit(FONT2.render("CUSTOM", True, GREY), self.text_menu2_rect)
        self.display.blit(
            FONT2.render("STANDARD WITH BOT", True, GREY), self.text_menu3_rect
        )
        self.display.blit(
            FONT2.render("CUSTOM WITH BOT", True, GREY), self.text_menu4_rect
        )
        self.display.blit(
            FONT1.render("PING", True, RED),
            (self.width - 300, (self.height - self.text_menu5_size[1] - 52) // 2),
        )
        self.display.blit(
            FONT1.render("PONG", True, BLUE),
            (self.width - 320, (self.height - self.text_menu6_size[1] + 52) // 2),
        )

    def blit_item(self, ball, player1, player2):
        self.display.fill(BLACK)
        self.display.blit(
            FONT3.render(str(player1.score), True, RED), (self.width // 2 - 30, 10)
        )
        self.display.blit(
            FONT3.render(str(player2.score), True, BLUE), (self.width // 2 + 30, 10)
        )
        pygame.draw.ellipse(self.display, WHITE, ball.rect)
        pygame.draw.rect(self.display, RED, player1.rect)
        pygame.draw.rect(self.display, BLUE, player2.rect)

    def end_game(self):
        self.display.fill(BLACK)
        if self.player_blue_win:
            self.display.blit(
                FONT1.render("BLUE", True, BLUE),
                (0, self.height - FONT1.get_height() + 7),
            )
        elif self.player_red_win:
            self.display.blit(FONT1.render("RED", True, RED), (0, 0))

        if self.end_text1:
            self.sound_game_over.play()
            pygame.display.flip()
            time.sleep(1)
            self.end_text1 = False
        if self.player_blue_win:
            self.display.blit(
                FONT1.render("WIN", True, WHITE), (self.width - FONT1.size("WIN")[0], 0)
            )
        elif self.player_red_win:
            self.display.blit(
                FONT1.render("WIN", True, WHITE),
                (
                    self.width - FONT1.size("WIN")[0],
                    self.height - FONT1.get_height() + 7,
                ),
            )

        if self.end_text2:
            pygame.display.flip()
            time.sleep(0.5)
            self.end_text2 = False
        self.display.blit(
            FONT2.render("ENTER TO RESTART", True, GREY),
            (
                (self.width - FONT2.size("ENTER TO RESTART")[0]) // 2,
                (self.height - FONT2.get_height() - 50) // 2,
            ),
        )
        self.display.blit(
            FONT2.render("ESC TO MENU", True, GREY),
            (
                (self.width - FONT2.size("ESC TO MENU")[0]) // 2,
                (self.height - FONT2.get_height() + 50) // 2,
            ),
        )


class Ball:
    def __init__(self):
        self.not_collide = True
        self.y = 5
        self.rect = pygame.Rect(445, 245, 10, 10)
        self.speed = [random.choice([-5, 5]), 0]
        self.sound = pygame.mixer.Sound(f"{BASE_DIR}/ball_sound.wav")

    def move(self):
        self.rect = self.rect.move(self.speed)

    def collide_with_players(self, player1, player2):
        if self.not_collide:
            if self.rect.colliderect(player1.rect) or self.rect.colliderect(
                player2.rect
            ):
                self.speed[1] = random.choice([-5, -2, -3, -4, -5, 1, 2, 3, 4, 5])
                self.not_collide = False
                self.sound.play()

        if self.rect.colliderect(player1.rect):
            self.speed[0] = -self.speed[0]
            player1.score += 1
            self.sound.play()
            if self.speed[1] > 0:
                self.speed[1] = random.randint(1, self.y)
            else:
                self.speed[1] = random.randint(-self.y, -1)

        if self.rect.colliderect(player2.rect):
            self.speed[0] = -self.speed[0]
            player2.score += 1
            self.sound.play()
            if self.speed[1] > 0:
                self.speed[1] = random.randint(1, self.y)
            else:
                self.speed[1] = random.randint(-self.y, -1)

    def collide_with_window(self, screen):
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
            self.sound.play()

        if self.rect.bottom >= screen.height:
            self.speed[1] = -self.speed[1]
            self.sound.play()

        if self.rect.right <= 0:
            screen.player_blue_win = True
        if self.rect.left >= screen.width:
            screen.player_red_win = True


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 80)
        self.speed_up = (0, -5)
        self.speed_down = (0, 5)
        self.score = 0

    def move(self, player_num, screen):
        if player_num == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect = self.rect.move(self.speed_up)
            if keys[pygame.K_s] and self.rect.bottom < screen.height:
                self.rect = self.rect.move(self.speed_down)
        if player_num == 2:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect = self.rect.move(self.speed_up)
            if keys[pygame.K_DOWN] and self.rect.bottom < screen.height:
                self.rect = self.rect.move(self.speed_down)


class Bot(Player):
    def __init__(self, x, y, mode):
        Player.__init__(self, x, y)
        if mode == "STANDARD":
            self.speed_up = (0, -4)
            self.speed_down = (0, 4)
        elif mode == "CUSTOM":
            self.speed_up = (0, -5)
            self.speed_down = (0, 5)

    def move(self, ball, screen):
        if self.rect.centery > ball.rect.centery and self.rect.top > 0:
            self.rect = self.rect.move(self.speed_up)
        if self.rect.centery < ball.rect.centery and self.rect.bottom < screen.height:
            self.rect = self.rect.move(self.speed_down)


"""---------------------------game-menu---------------------------------------"""


def menu():
    menu_on = True
    menu_screen = Screen()
    while menu_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    menu_screen.text_menu1_rect[0]
                    <= event.pos[0]
                    <= menu_screen.text_menu1_rect[0] + menu_screen.text_menu1_size[0]
                    and menu_screen.text_menu1_rect[1]
                    <= event.pos[1]
                    <= menu_screen.text_menu1_rect[1] + menu_screen.text_menu1_size[1]
                ):
                    menu_screen.sound_menu.play()
                    menu_on = False
                    main("STANDARD")
                elif (
                    menu_screen.text_menu2_rect[0]
                    <= event.pos[0]
                    <= menu_screen.text_menu2_rect[0] + menu_screen.text_menu2_size[0]
                    and menu_screen.text_menu2_rect[1]
                    <= event.pos[1]
                    <= menu_screen.text_menu2_rect[1] + menu_screen.text_menu2_size[1]
                ):
                    menu_screen.sound_menu.play()
                    menu_on = False
                    main("CUSTOM")
                elif (
                    menu_screen.text_menu3_rect[0]
                    <= event.pos[0]
                    <= menu_screen.text_menu3_rect[0] + menu_screen.text_menu3_size[0]
                    and menu_screen.text_menu3_rect[1]
                    <= event.pos[1]
                    <= menu_screen.text_menu3_rect[1] + menu_screen.text_menu3_size[1]
                ):
                    menu_screen.sound_menu.play()
                    menu_on = False
                    main("STANDARD", True)
                elif (
                    menu_screen.text_menu4_rect[0]
                    <= event.pos[0]
                    <= menu_screen.text_menu4_rect[0] + menu_screen.text_menu4_size[0]
                    and menu_screen.text_menu4_rect[1]
                    <= event.pos[1]
                    <= menu_screen.text_menu4_rect[1] + menu_screen.text_menu4_size[1]
                ):
                    menu_screen.sound_menu.play()
                    menu_on = False
                    main("CUSTOM", True)

        menu_screen.menu()
        pygame.display.update()


"""---------------------------main---------------------------------------"""


def main(mode, bot=False):
    game_on = True
    screen = Screen()
    ball = Ball()
    player1 = Player(10, 210)
    player2 = Bot(885, 210, mode) if bot else Player(885, 210)
    ball_speed_upx = pygame.USEREVENT
    pygame.time.set_timer(ball_speed_upx, 10000)
    ball_speed_upy = pygame.USEREVENT + 1
    pygame.time.set_timer(ball_speed_upy, 50000)
    clock = pygame.time.Clock()
    fps = None
    if mode == "STANDARD":
        fps = 120
    elif mode == "CUSTOM":
        fps = 80

    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if mode == "CUSTOM":
                if event.type == ball_speed_upx:
                    ball.speed[0] += 1 if ball.speed[0] > 0 else -1
                if event.type == ball_speed_upy:
                    ball.y += 1

        if not screen.player_blue_win or screen.player_red_win:
            player1.move(1, screen)
            player2.move(ball, screen) if bot else player2.move(2, screen)
            ball.move()
        ball.collide_with_players(player1, player2)
        ball.collide_with_window(screen)
        screen.blit_item(ball, player1, player2)

        if screen.player_blue_win or screen.player_red_win:
            ball.sound.stop()
            screen.end_game()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                screen = Screen()
                ball = Ball()
                player1 = Player(10, 210)
                player2 = Bot(885, 210, mode) if bot else Player(885, 210)
            if keys[pygame.K_ESCAPE]:
                game_on = False
                menu()

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    menu()
