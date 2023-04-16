import json


def find_matching_attributes(attr_list, json_file):
    # Load the JSON file into a dictionary
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Get the "features" array from the JSON data
    features = json_data["features"]

    # Create an empty list to store matching attributes
    matching_attributes = []

    # Iterate through the attributes in the first list
    for obj_type, obj_attrs in attr_list.items():
        # Iterate through the attributes in the object type
        for attr in obj_attrs:
            # Check if the attribute is in the "features" array or overlaps with part of a feature
            if any([overlap in features for overlap in attr.split()]) or any(
                    [overlap in feature for feature in features for overlap in attr.split('_')]):
                matching_attributes.append(f"{obj_type}_{attr}")

    return matching_attributes


attr_list = {'Bird': ['score', 'center'], 'Pillar': ['gap_height', 'x']}
json_file = 'attributes.json'

matching_attributes = find_matching_attributes(attr_list, json_file)

print(matching_attributes)
