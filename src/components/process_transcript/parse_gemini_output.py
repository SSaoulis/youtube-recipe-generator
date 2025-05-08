from typing import List, Dict
import re


# This is disgusting because I wanted to make it O(n) for some reason
def parse_sections(response_text: str) -> List[Dict[str, str]]:
    """Turns the ingredients into a list of dictionaries containing the ingredient (key) and
    quantity (value)

    Args:
        response_text (str): The input recipe text

    Returns:
        List[Dict[str, str]]: List of dictionaries with 'ingredient' and 'quantity' keys
    """
    lines = response_text.splitlines()

    ingredients, preparation_steps, instructions, notes = [], [], [], []
    in_ingredients_section = False
    in_preparation_steps = False
    in_instructions = False
    in_notes = False

    # Parse through the lines
    for line in lines:
        line = line.strip()

        # Ingredients section
        if line.startswith("1. Ingredients"):
            in_ingredients_section = True
            continue
        if in_ingredients_section:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_ingredients_section = False
                continue
            if "|" in line:  # Parse the "ingedient | quantity" format
                parts = [part.strip() for part in line.split("|", 1)]
                if len(parts) == 2:
                    ingredient, quantity = parts
                    ingredients.append({"ingredient": ingredient, "quantity": quantity})

        # Preparation Section
        if line.startswith("2. Preparation required before cooking"):
            in_preparation_steps = True
            continue
        if in_preparation_steps:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_preparation_steps = False
                continue
            preparation_steps.append(line)

        # Recipe Instuctions Section
        if line.startswith("3. Recipe Instructions"):
            in_instructions = True
            continue
        if in_instructions:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_instructions = False
                continue
            instructions.append(line)

        # Notes Section
        if line.startswith("4. Notes"):
            in_notes = True
            continue
        if in_notes:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_notes = False
                continue
            notes.append(line)

    return {
        "ingredients": ingredients,
        "preparation_steps": preparation_steps,
        "instructions": instructions,
        "notes": notes,
    }
