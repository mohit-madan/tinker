def flatten_json(nested_json: dict[str, any], prefix = "") -> dict[str, any]:
    """
    Flatten a nested JSON object into a single level.
    """
    items = []
    for key, value in nested_json.items():
        new_key = prefix + key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key + "."))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                items.extend(flatten_json(item, new_key + "[" + str(i) + "]."))
        else:
            items.append((new_key, value))
    return items

data = {
    "user": {
        "name": "Alice",
        "settings": {
            "theme": "dark",
            "notifications": True
        },
        "friends": [
            {
                "name": "Bob",
                "age": 25
            },
            {
                "name": "Charlie",
                "age": 30
            }
        ]
    },
    "id": 123
}

print(flatten_json(data))