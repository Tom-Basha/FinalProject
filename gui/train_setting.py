import os

from gui.attribute_selection import attribute_selection
import key_selection as ks
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from assets.components.button import back_btn, manu_btn
from assets.components.scrollbar import Scrollbar
from assets.paths import *
from assets.utils import *
from assets.components.slider import Slider

BACKGROUND = pygame.image.load(BACKGROUND_IMAGE)
BACKGROUND_COVER = pygame.image.load(SCROLLBAR_BG)

DEFAULT_THRESHOLD = 300
DEFAULT_POPULATION = 100
DEFAULT_GENERATIONS = 10000
DEFAULT_START_GEN = -1
DEFAULT_HIDDEN_LAYERS = 3


class Settings:
    def __init__(self, game_name, selected_keys, selected_attributes, fitness, generations, population, start_cp, hidden_layers):
        pygame.init()
        self.cps_path = f"..\\agents\\NEAT\\games\\{game_name}\\checkpoints"
        # Screen creation.
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Training Settings")

        self.selected_keys = selected_keys
        self.selected_attributes = selected_attributes
        # List settings.
        self.top_margin = 200
        self.bottom_margin = 150
        self.list_window = SCREEN_H - self.top_margin - self.bottom_margin
        self.item_height = 150
        self.item_width = 600
        self.items_spacing = 20
        self.slider_x = SCREEN_W // 2 - 250

        # Settings and sliders creation.
        self.items = [
            ("Start Checkpoint", "Set to -1 for a new training",
             Slider(self.slider_x, self.top_margin + 0 * (self.item_height + self.items_spacing), 500, -1,
                    self.cps_count(), 1,
                    start_cp)),
            ("Fitness Threshold", "Recommended: 250 - 350",
             Slider(self.slider_x, self.top_margin + 1 * (self.item_height + self.items_spacing), 500, 50, 5000, 50,
                    fitness)),
            ("Generations", "Recommended: 10000",
             Slider(self.slider_x, self.top_margin + 2 * (self.item_height + self.items_spacing), 500, 50, 10000, 50,
                    generations)),
            ("Population", "Recommended: 50",
             Slider(self.slider_x, self.top_margin + 3 * (self.item_height + self.items_spacing), 500, 10, 200, 5,
                    population)),
            ("Neural Network Hidden Layers", "Recommended: 2 - 3",
             Slider(self.slider_x, self.top_margin + 4 * (self.item_height + self.items_spacing), 500, 1, 5, 1,
                    hidden_layers)),
        ]
        self.values = [start_cp, fitness, generations, population, hidden_layers]

        self.num_items = len(self.items)

        # Sliders list.
        self.sliders = [
            self.items[0][2],
            self.items[1][2],
            self.items[2][2],
            self.items[3][2],
            self.items[4][2]
        ]

        # Scrollbar creation.
        self.scrollbar = Scrollbar(self.screen,
                                   170 + self.num_items * (self.item_height + self.items_spacing) - self.items_spacing,
                                   self.list_window, self.top_margin, self.bottom_margin)

        # Font.
        self.font = pygame.font.Font(None, 36)

    # Description: Counts how many checkpoints are there.
    def cps_count(self):
        count = -1
        if os.path.exists(self.cps_path):
            for filename in os.listdir(self.cps_path):
                if filename.startswith("train_checkpoint_") and os.path.isfile(os.path.join(self.cps_path, filename)):
                    count += 1
        return count

    def draw_item(self, item, sub_item, y, slider):
        # Set the dimensions and position of the rectangle.
        rect_width = 750
        rect_height = 150
        x = SCREEN_W // 2 - rect_width // 2  # center the rectangle horizontally.

        item_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)

        item_surface.fill((0, 0, 0, 0))

        # Create a mask and a temporary surface for the rectangle with rounded corners.
        mask = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 128))  # semi-transparent color
        pygame.draw.rect(mask, (0, 0, 0, 128), mask.get_rect(), border_radius=15)  # punch a hole in the mask.

        # Create another temporary surface and draw the rectangle with rounded corners onto it.
        temp = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        pygame.draw.rect(temp, (0, 0, 0, 128), temp.get_rect(), border_radius=15)

        # Apply the mask onto the temporary surface.
        temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        # Draw the rectangle border with a border radius.
        pygame.draw.rect(temp, MAIN_CLR, temp.get_rect(), width=3, border_radius=15)

        # Draw the temporary surface onto the item surface.
        item_surface.blit(temp, (0, 0))

        # Render the text.
        font = pygame.font.Font(None, 36)
        text = font.render(item, True, MAIN_CLR)
        surface_midtop = item_surface.get_rect().midtop

        text_rect = text.get_rect(midtop=(surface_midtop[0], surface_midtop[1] + 20))  # center the text.

        # Draw the text onto the Surface.
        item_surface.blit(text, text_rect)

        # Render the subtext.
        sub_font = pygame.font.Font(None, 20)
        subtext = sub_font.render(sub_item, True, SECONDARY_CLR)
        subtext_rect = subtext.get_rect(midtop=(surface_midtop[0], surface_midtop[1] + 45))  # center the text.

        # Draw the subtext onto the Surface.
        item_surface.blit(subtext, subtext_rect)

        # Draw the Surface onto the screen.
        self.screen.blit(item_surface, (x, y))

        # Draw the slider.
        slider.y = 15 + y + self.item_height // 2  # update the slider's y-position.
        slider.draw(self.screen)


def train_setting(game_name, game_attributes, selected_keys, selected_attributes, threshold, population, generations, start_gen, hidden_layers):
    settings = Settings(game_name, selected_keys, selected_attributes, threshold, population, generations, start_gen, hidden_layers)
    HEADER, HEADER_RECT = header("SETTINGS")
    SUBHEAD, SUBHEAD_RECT = subhead("SELECT YOUR TRAINING PREFERENCES", 16)
    CONTROLS_BTN = manu_btn("Controls", (SCREEN_W // 2 - 200, 250))
    ATTRIBUTES_BTN = manu_btn("Attributes", (SCREEN_W // 2 + 200, 250))
    BACK_BTN = back_btn()

    while True:
        settings.values = [
            item[2].value for i, item in enumerate(settings.items)
        ]
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the button.
                if BACK_BTN.check_input(mouse_pos):
                    return selected_keys, selected_attributes, settings.values[0], settings.values[1], settings.values[2], settings.values[3], \
                        settings.values[4]

                # Keys selection.
                if CONTROLS_BTN.check_input(mouse_pos):
                    settings.selected_keys = ks.key_selection(selected_keys)

                # Attributes selection.
                if ATTRIBUTES_BTN.check_input(mouse_pos):
                    settings.selected_attributes = attribute_selection(game_attributes, selected_attributes)

            settings.scrollbar.handle_event(event)

            # Handle events for the sliders.
            for slider in settings.sliders:
                slider.handle_event(event)

        settings.screen.blit(BACKGROUND, (0, 0))

        y = settings.top_margin + settings.scrollbar.scroll_offset + 80

        CONTROLS_BTN = manu_btn("Controls", (SCREEN_W // 2 - 185, y))
        ATTRIBUTES_BTN = manu_btn("Attributes", (SCREEN_W // 2 + 185, y))
        y += 90
        for i, item in enumerate(settings.items):
            settings.draw_item(settings.items[i][0], settings.items[i][1], y, settings.items[i][2])
            y += settings.item_height + settings.items_spacing

        settings.scrollbar.draw()

        buttons = [CONTROLS_BTN, ATTRIBUTES_BTN]
        for button in buttons:
            button.change_color(mouse_pos)
            button.update(settings.screen)

        settings.screen.blit(BACKGROUND_COVER, (0, 0))

        BACK_BTN.change_color(mouse_pos)
        BACK_BTN.update(settings.screen)

        settings.screen.blit(HEADER, HEADER_RECT)
        settings.screen.blit(SUBHEAD, SUBHEAD_RECT)

        pygame.display.flip()
