import os
import json

from src.components.get_youtube_response import (
    get_transcript_from_url,
    get_video_metadata,
)
from src.components.parse_transcript import get_gemini_response, parse_sections
from src.components.generate_pdf import RecipePDFGenerator
from src.logger import logger

pdf_generator = RecipePDFGenerator()


def process_url(url: str, recipe_output_dir: str, save_sections_json: bool) -> None:
    """Generates the report output from the youtube video URL.
    1. Gets the youtube transcript and metadata
    2. Pass the transcript to gemini and get the parsed information
    3. Generate the output PDF.

    Args:
        url (str): Youtube video URL.
        recipe_output_dir (str, optional): A specified dir to save the pdf in. Defaults to None.
        save_output (bool, optional): Whether to save the gemini response and metadata.
          Defaults to False.
    """
    # 1. Download the transcript and metadata
    transcript = get_transcript_from_url(url)
    metadata = get_video_metadata(url)

    # 2. Read the transcript and get the parsed sections:
    # (ingredients, preparatation, steps, notes)
    response = get_gemini_response(transcript)

    logger.info("Parsing Gemini output to sections")
    sections = parse_sections(response.text)

    sections.update(metadata)

    # Save the sections to a json file
    if save_sections_json:
        # Make the output directory if it doesn't exist
        recipe_section_output_dir = os.path.join(recipe_output_dir, "sections")
        if not os.path.exists(recipe_section_output_dir):
            os.makedirs(recipe_section_output_dir, exist_ok=True)

        # Save the sections to a json file
        section_output_filename = os.path.join(
            recipe_section_output_dir, "sections.json"
        )
        with open(section_output_filename, "w") as f:
            json.dump(sections, f, indent=4)
        logger.info(f"Saved sections to '{section_output_filename}'")

    # 3. Generate the output pdf
    if not os.path.exists(recipe_output_dir):
        os.makedirs(recipe_output_dir, exist_ok=True)
    output_filename = os.path.join(recipe_output_dir, sections["title"] + ".pdf")

    pdf_generator.generate(sections, output_filename=output_filename)


def generate_from_txt(recipe_output_dir: str, response_path: str) -> None:
    """Generate the recipe PDF from the gemini parsed section file.

    1. Read the gemini section file
    2. Generate the output PDF.


    Args:
        recipe_output_dir (str): A specified dir to save the pdf in.
        response_path (str, optional): Path to the parsed gemini section json.
    """

    # 1. Read the section json
    try:
        with open(response_path, "r") as f:
            sections = json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {response_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {response_path}")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return

    logger.info("Parsed sections from json file")

    # 2. Generate the output pdf
    if not os.path.exists(recipe_output_dir):
        os.makedirs(recipe_output_dir, exist_ok=True)
    output_filename = os.path.join(recipe_output_dir, sections["title"] + ".pdf")

    pdf_generator.generate(sections, output_filename=output_filename)
