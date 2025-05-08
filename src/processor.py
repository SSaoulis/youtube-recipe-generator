import os

from src.components.get_youtube_response import (
    get_transcript_from_url,
    get_video_metadata,
)
from src.components.parse_transcript import get_gemini_response
from src.components.generate_pdf import generate_recipe_pdf


def process_url(url: str, recipe_output_dir: str) -> None:
    """Generates the report output from the youtube video URL.
    1. Gets the youtube transcript and metadata
    2. Pass the transcript to gemini and get the parsed information
    3. Generate the output PDF.

    Args:
        url (str): Youtube video URL.
        recipe_output_dir (str, optional): A specified dir to save the pdf in. Defaults to None.
    """
    # 1. Download the transcript and metadata
    transcript = get_transcript_from_url(url)
    metadata = get_video_metadata(url)

    # 2. Read the transcript and get the parsed sections:
    # (ingredients, preparatation, steps, notes)
    sections = get_gemini_response(transcript)

    sections.update(metadata)

    # 3. Generate the output pdf
    if not os.path.exists(recipe_output_dir):
        os.makedirs(recipe_output_dir, exist_ok=True)
    output_filename = os.path.join(recipe_output_dir, sections["title"] + ".pdf")

    generate_recipe_pdf(sections, output_filename=output_filename)
