import subprocess
import pickle
from typing import List


def print_game_attributes(game_process: subprocess.Popen, attributes: List[str], game_snake_class: str):
    game_snake = pickle.loads(game_process.stdout.readline())

    def get_attribute_value(obj, attr_name):
        try:
            return getattr(obj, attr_name)
        except AttributeError:
            return None

    for attribute in attributes:
        class_name, attr_name = attribute.split('.')
        if class_name == game_snake_class:
            value = get_attribute_value(game_snake, attr_name)
            print(f"{attribute}: {value}")
