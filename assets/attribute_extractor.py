import ast


def extract_features(file_path):
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
