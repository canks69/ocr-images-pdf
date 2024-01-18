def auto_correction(text):
    # Define replacements
    replacements = {"Tanslor": "Transfer", "HANK": "BANK"}

    # Perform autocorrection
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    return text