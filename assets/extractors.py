import ast
import re
import os
import json

from assets.paths import ATTRIBUTES_JSON
from testings.key_map import key_mapping


def games_extractor():
    games_list = []
    folder_path = "..\\games"
    for game in os.listdir(folder_path):
        if game.endswith(".py"):
            file_path = os.path.join(folder_path, game)
            file_name_without_ext = os.path.splitext(game)[0]
            file_name = file_name_without_ext.replace("_", " ").title()
            games_list.append((file_name, file_path))
    return games_list


def keys_extractor(file_path):
    key_pattern = r"(pygame\.K_[A-Za-z0-9_]+)"

    with open(file_path, 'r') as file:
        content = file.read()

    keys = re.findall(key_pattern, content)

    if "pygame.K_ESCAPE" in keys:
        keys.remove("pygame.K_ESCAPE")

    return set(keys)


def attribute_extractor(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
        class_features = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_features[class_name] = []
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        for subsubnode in subnode.body:
                            if isinstance(subsubnode, ast.Assign):
                                for target in subsubnode.targets:
                                    if isinstance(target, ast.Attribute):
                                        value = target.value
                                        while isinstance(value, ast.Attribute):
                                            value = value.value
                                        if isinstance(value, ast.Name) and value.id == "self":
                                            attr = target.attr
                                            while isinstance(target.value, ast.Attribute):
                                                target = target.value
                                                attr = target.attr + "." + attr
                                            if attr == 'rect':
                                                attr = 'rect.center'
                                            if attr not in ['rect.x', 'rect.y', 'rect.w', 'rect.h', 'score'] and attr not in class_features[class_name]:
                                                class_features[class_name].append(attr)
    return [(class_name, attrs) for class_name, attrs in class_features.items()]


def match_attributes(game_attributes):
    with open(ATTRIBUTES_JSON, 'r') as f:
        json_data = json.load(f)

    match_dict = {}

    for obj_type, obj_attrs in game_attributes:
        if obj_type != "BaseObject":
            attributes = []
            for attr in obj_attrs:
                if attr in json_data:
                    attributes.append(attr)
            if len(attributes) != 0:
                match_dict[obj_type] = attributes

    return match_dict
