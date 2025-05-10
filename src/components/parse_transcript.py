import os
import re
import traceback
import sys
from typing import List, Dict, Union

from google import genai

from src.logger import logger

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

base_prompt_path = os.path.join(
    os.path.dirname(__file__), "templates", "base_prompt.txt"
)

with open(base_prompt_path, "r") as f:
    BASE_PROMPT = f.read()
logger.info("Successfully read base prompt")


def get_gemini_response(transcript: str) -> Dict[str, Union[List[str], Dict[str, str]]]:
    """Passes the prompt + transcript into Gemini to get recipe information out.

    Args:
        transcript (str): The youtube audio transcript

    Returns:
        Dict[str, Union[List[str], Dict[str, str]]]: The parsed sections for the recipe PDF.
        Contains:
        {
            "ingredients" : A list of ingredients dictionaries, with keys "ingredient" and
                            "quantities"
            "prepraration_steps" : A list of preparation steps (strings)
            "instructions" : A list of instructions steps for the recipe (strings)
            "notes" : A list of additional information from the video transcript (strings)
        }
    """

    gemini_input = BASE_PROMPT + "\n" + transcript
    logger.info("Submitting transcript to Gemini")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=gemini_input,
        )
    except Exception as e:
        logger.error(f"Failed to get Gemini response: {e}")
        traceback.print_exc()
        sys.exit(1)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    logger.info(
        f"Got response; used {prompt_tokens} tokens for prompt, {response_tokens} for response."
    )
    return response


# This is disgusting because I wanted to make it O(n) for some reason
def parse_sections(response_text: str) -> Dict[str, Union[List[str], Dict[str, str]]]:
    """Parses the Gemini text response into sections. These sections are lists of objects which
    are used to generate the output PDF.

    Args:
        response_text (str): The input recipe text

    Returns:
    A dictionary containing:
        {
            "ingredients" : A list of ingredients dictionaries, with keys "ingredient" and
                            "quantities"
            "preparation" : A list of preparation steps (strings)
            "steps" : A list of instructions steps for the recipe (strings)
            "notes" : A list of additional information from the video transcript (strings)
        }
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
        if line.startswith("1."):
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
        if line.startswith("2."):
            in_preparation_steps = True
            continue
        if in_preparation_steps:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_preparation_steps = False
                continue
            preparation_steps.append(line)

        # Recipe Instuctions Section
        if line.startswith("3."):
            in_instructions = True
            continue
        if in_instructions:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_instructions = False
                continue
            instructions.append(line)

        # Notes Section
        if line.startswith("4."):
            in_notes = True
            continue
        if in_notes:
            if not line or re.match(r"\d+\.\s", line):  # End of section
                in_notes = False
                continue
            notes.append(line)

    return {
        "ingredients": ingredients,
        "preparation": preparation_steps,
        "steps": instructions,
        "notes": notes,
    }
