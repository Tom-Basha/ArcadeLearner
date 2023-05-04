import json


def find_matching_attributes(attr_list, json_file):
    # Load the JSON file into a dictionary
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Get the "features" array from the JSON data
    features = json_data["features"]

    # Create an empty dictionary to store objects and their attributes
    objects = {}

    # Iterate through the attributes in the first list
    for obj_type, obj_attrs in attr_list.items():
        # Create an empty array to store the attributes of the current object type
        obj_attr_list = []

        # Iterate through the attributes in the object type
        for attr in obj_attrs:
            # Check if the attribute matches a feature string or is a part of a feature string
            if any(feature == attr or f" {attr} " in feature for feature in features):
                # Append the matching attribute to the object attribute list
                obj_attr_list.append(attr)

        # If the object type has at least one matching attribute, add it to the dictionary
        if obj_attr_list:
            objects[obj_type] = obj_attr_list

    return objects


attr_list = {'Bird': ['score', 'center'], 'Pillar': ['gap_height', 'x']}
json_file = 'attributes.json'

objects = find_matching_attributes(attr_list, json_file)

print(objects)