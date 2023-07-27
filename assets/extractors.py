import ast
import re
import os
import json

from assets.paths import ATTRIBUTES_JSON


# Output: List of tuples, each tuple consists of a game title and its file path.
# Description: Finds all Python game files from the "games" folder.
def games_extractor():
    games_list = []
    folder_path = "..\\games"               # games folder path.

    # saves the game title and its file path for each .py file.
    for game in os.listdir(folder_path):
        if game.endswith(".py"):
            file_path = os.path.join(folder_path, game)
            file_name_without_ext = os.path.splitext(game)[0]
            file_name = file_name_without_ext.replace("_", " ").title()
            games_list.append((file_name, file_path))
    return games_list


# Inputs: Game file path.
# Outputs: Set of Pygame keys.
# Description: Finds all Pygame keys mentioned in the game file.
def keys_extractor(file_path):
    key_pattern = r"(pygame\.K_[A-Za-z0-9_]+)"      # Pygame keys prefix and pattern.

    # Reads the game file and stores it in content.
    with open(file_path, 'r') as file:
        content = file.read()

    # Searching for pygame keys by the pattern.
    keys = re.findall(key_pattern, content)

    # Removes the escape button to avoid AI players to quit.
    if "pygame.K_ESCAPE" in keys:
        keys.remove("pygame.K_ESCAPE")

    return set(keys)


# Inputs: Game file path.
# Outputs: List of tuples, each containing a class name and its associated attributes.
# Description: Reads the Python game file, parses the Abstract Syntax Tree (AST) and extracts class names and their associated attributes
def attribute_extractor(file_path):
    # Parses the content of game the file into an abstract syntax tree (AST) and initializes a dictionary.
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
        class_features = {}

        # Iterates through the AST nodes and extracts class attributes.
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):          # Class.
                class_name = node.name
                class_features[class_name] = []
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):        # Function.
                        for subsubnode in subnode.body:
                            if isinstance(subsubnode, ast.Assign):      # Assignment statement.
                                for target in subsubnode.targets:
                                    if isinstance(target, ast.Attribute):   # Attribute.
                                        value = target.value
                                        while isinstance(value, ast.Attribute):
                                            value = value.value
                                        if isinstance(value, ast.Name) and value.id == "self":
                                            attr = target.attr
                                            while isinstance(target.value, ast.Attribute):
                                                target = target.value
                                                attr = target.attr + "." + attr

                                            # Special cases to exclude.
                                            if attr == 'rect':
                                                attr = 'rect.center'
                                            if attr not in ['rect.x', 'rect.y', 'rect.w', 'rect.h',
                                                            'score'] and attr not in class_features[class_name]:
                                                class_features[class_name].append(attr)
    return [(class_name, attrs) for class_name, attrs in class_features.items()]


# Inputs: List of tuples, each containing a class name and its associated attributes.
# Output: A dictionary where keys are object types and values are lists of attributes.
# Description: Auto selects attributes by matching attributes from predefined json file and the tuple list attributes.
def match_attributes(game_attributes):
    # Reads the attribute json file
    with open(ATTRIBUTES_JSON, 'r') as f:
        json_data = json.load(f)

    match_dict = {}

    # Iterates through the classes and appends attributes that exists in the json file to the dictionary.
    for obj_type, obj_attrs in game_attributes:
        if obj_type != "BaseObject":
            attributes = []
            for attr in obj_attrs:
                if attr in json_data:
                    attributes.append(attr)
            if len(attributes) != 0:
                match_dict[obj_type] = attributes

    return match_dict
