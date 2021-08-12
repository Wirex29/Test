import pygame
import player

# Settings
''' window '''
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Name of Game"
FPS = 60

''' colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' fonts '''
TITLE_FONT = None
DEFAULT_FONT = None

# Make window
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load assets
font_sm = pygame.font.Font(DEFAULT_FONT, 24)
font_md = pygame.font.Font(DEFAULT_FONT, 32)
font_xl = pygame.font.Font(TITLE_FONT, 96)


# Scenes
class Scene:
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        self.bg_menu = pygame.image.load("PNG/BG_01/BG_01.png").convert()
        self.start_button = pygame.Rect(480, 288, 320, 72)
        self.option_button = pygame.Rect(480, 432, 320, 72)
        self.rect = self.bg_menu.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def process_input(self, events, keys):
        for event in events:
            """if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = GameScene()"""
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button.collidepoint(mouse_pos):
                    print("Starting Game...")
                    self.next_scene = GameScene()
                elif self.option_button.collidepoint(mouse_pos):
                    print("Opening Option....")
                    self.next_scene = OptionScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        self.bg_menu = pygame.transform.scale(self.bg_menu, [SCREEN_WIDTH, SCREEN_HEIGHT])
        screen.blit(self.bg_menu, self.rect)
        pygame.draw.rect(screen, (0, 255, 255), self.start_button)
        pygame.draw.rect(screen, (0, 255, 255), self.option_button)


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.map = pygame.image.load("PNG/map.png").convert()
        self.rect = self.map.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def process_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = EndScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        screen.blit(self.map, self.rect)


class EndScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Game Over", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


class OptionScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, keys):
        """for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()"""
        pass

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Option scene", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


# Main game class
class Game:
    def __init__(self):
        self.active_scene = TitleScene()

    @staticmethod
    def is_quit_event(event, pressed_keys):
        x_out = event.type == pygame.QUIT
        ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        q = pressed_keys[pygame.K_q]

        return x_out or (ctrl and q)

    def run(self):
        while self.active_scene is not None:
            # Get user input
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    self.active_scene.terminate()
                else:
                    filtered_events.append(event)

            # Manage scene
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()
            self.active_scene = self.active_scene.next_scene

            # Update and tick
            pygame.display.flip()
            clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
    main = Game()
    main.run()
    pygame.quit()
