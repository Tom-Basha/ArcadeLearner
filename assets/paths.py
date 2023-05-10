import os

# Define the base paths for images, fonts, and other assets
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(BASE_PATH, "images")
FONTS = os.path.join(BASE_PATH, "fonts")

# Define the file paths for specific assets
BACKGROUND_IMAGE = os.path.join(IMAGES, "background.jpg")
BUTTON_BG = os.path.join(IMAGES, "buttonBG1.png")
TRAINING_BTN = os.path.join(IMAGES, "Training Button1.png")
QUIT_BG = os.path.join(IMAGES, "Quit Rect.jpg")
OPTIONS_BG = os.path.join(IMAGES, "Options Rect.jpg")
MAIN_FONT = os.path.join(FONTS, "font.ttf")
TRAIN_FONT = os.path.join(FONTS, "verdana.ttf")
ERROR_NEON = os.path.join(IMAGES, "error neon1.png")
