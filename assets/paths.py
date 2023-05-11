import os

# Define the base paths for images, fonts, and other assets folders
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(BASE_PATH, "images")
FONTS = os.path.join(BASE_PATH, "fonts")

# Define the file paths for images
BACKGROUND_IMAGE = os.path.join(IMAGES, "Background.jpg")
SCROLLBAR_BG = os.path.join(IMAGES, "Scrollbar Background.png")
BUTTON_BG = os.path.join(IMAGES, "Button.png")
TRAINING_BTN = os.path.join(IMAGES, "Training Button.png")

# Define the file paths for fonts
MAIN_FONT = os.path.join(FONTS, "font.ttf")
TRAIN_FONT = os.path.join(FONTS, "verdana.ttf")

# Define the file paths for attributes list
ATTRIBUTES_JSON = os.path.join(BASE_PATH, "attributes.json")
