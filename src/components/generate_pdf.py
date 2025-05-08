import os
import tempfile
from pathlib import Path
from typing import Dict, List, Union

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


templates_path = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(templates_path))


# Custom filter to convert numbers to letters
def letter_index(number):
    return chr(96 + number)  # 97 is ASCII for 'a'


env.filters["letter_index"] = letter_index

template = env.get_template("recipe_template.html")


def generate_recipe_pdf(
    recipe_data: Dict[str, Union[List[str], Dict[str, str]]],
    output_filename: str,
    save_html: bool,
) -> None:
    """Generates the recipe PDF from the parsed gemini output and the HTML Template.
    See templates/recipe_template.html.

    Writes the output to the specified filepath as a PDF.

    Args:
        recipe_data (Dict[str, Union[List[str], Dict[str, str]]]): The recipe data parsed from
          gemini response
        output_filename (str): Place to save the output pdf.
        save_html (bool): Whether to save the html (if manual changes are needed).
    """
    html_content = template.render(**recipe_data)

    # Save to a tempfile
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False
    ) as tmp_html:
        tmp_html.write(html_content)
        temp_html_path = tmp_html.name

    if save_html:
        html_filename = f"{Path(output_filename).stem}.html"
        with open(html_filename, "w") as f:
            f.write(html_content)

    # Render the PDF from the temporary HTML file
    render_html_to_pdf(temp_html_path, output_filename)


def render_html_to_pdf(html_filename: str, output_filename: str) -> None:
    """Renders an HTML file into pdf.

    Args:
        html_filename (str): _description_
        output_filename (str): _description_
    """

    HTML(html_filename).write_pdf(output_filename)
