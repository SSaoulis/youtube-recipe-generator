import os

from components.get_transcript.get import get_transcript_from_url, get_video_metadata
from components.process_transcript.prompt import get_gemini_response
from components.process_transcript.parse_gemini_output import parse_sections
from components.pdf_generator.generate_pdf import generate_recipe_pdf


def process_url(url: str, recipe_output_dir: str, save_html: bool) -> None:
    """Generates the report output from the youtube video URL.
    1. Gets the youtube transcript and metadata
    2. Pass the transcript to gemini and get the parsed information
    3. Parse the gemini output to get the sections into nice data structures
    4. Generate the output PDF.

    Args:
        url (str): Youtube video URL.
        recipe_output_dir (str, optional): A specified dir to save the pdf in. Defaults to None.
    """

    # 1. Download the transcript and metadata
    transcript = get_transcript_from_url(url)
    metadata = get_video_metadata(url)

    # 2. Read the transcript and get the ingredients and recipe
    response = get_gemini_response(transcript)

    # 3. Parse the gemini output into the respective sections
    # (ingredients, preparatation, directions, instructions, notes)
    sections = parse_sections(response)
    sections.update(metadata)

    # 4. Generate the output pdf
    if not os.path.exists(recipe_output_dir):
        os.makedirs(recipe_output_dir, exist_ok=True)

    output_filename = os.path.join(recipe_output_dir, sections["title"] + ".pdf")

    # Generate the PDF from the parsed sections
    generate_recipe_pdf(sections, output_filename=output_filename, save_html=save_html)


def main():
    url = "https://www.youtube.com/watch?v=VIdlVi-VzPY"

    output_dir = os.path.abspath("recipes")

    process_url(url, output_dir, save_html=True)


main()
