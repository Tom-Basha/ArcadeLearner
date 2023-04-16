import ast
import re
import os

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
    print(games_list)
    return games_list


def keys_extractor(file_path):
    key_pattern = r"(pygame\.K_[A-Za-z0-9_]+)"

    with open(file_path, 'r') as file:
        content = file.read()

    keys = re.findall(key_pattern, content)

    if "pygame.K_ESCAPE" in keys:
        keys.remove("pygame.K_ESCAPE")

    return keys

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
                                        class_features[class_name].append(target.attr)
    # print([(class_name, attrs) for class_name, attrs in class_features.items()])
    return [(class_name, attrs) for class_name, attrs in class_features.items()]


