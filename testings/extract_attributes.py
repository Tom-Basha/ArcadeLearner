import ast


def extract_features(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
        features = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for subnode in node.body:
                    if isinstance(subnode, ast.Assign):
                        for target in subnode.targets:
                            if isinstance(target, ast.Attribute):
                                features.append(target.attr)
        return features
