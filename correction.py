import json

def auto_correction(text):
    # Define replacements
    with open('correction.json') as f:
        replacements = json.load(f)

    # Perform autocorrection
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    return text