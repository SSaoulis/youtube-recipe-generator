from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
    HRFlowable,
)
from reportlab.lib import colors

from src.logger import logger


class RecipePDFGenerator:
    """A class for generating recipe PDF reports from recipe data."""

    def __init__(self):
        """Initialize the PDF generator with default styles."""
        self.styles = getSampleStyleSheet()
        self.doc = None  # Will be set in generate method

        # Define custom paragraph styles
        self.h1 = ParagraphStyle(
            "RecipeTitle", parent=self.styles["Title"], alignment=1, spaceAfter=12
        )
        self.h2 = ParagraphStyle(
            "SectionTitle", parent=self.styles["Heading2"], spaceBefore=12, spaceAfter=6
        )
        self.h3 = ParagraphStyle(
            "Author",
            parent=self.styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=colors.grey,
            alignment=1,
            spaceAfter=12,
        )
        self.body = self.styles["BodyText"]

    @staticmethod
    def letter_index(n: int) -> str:
        """Convert a number to its corresponding lowercase letter.

        Args:
            n (int): The number to convert (1-based)

        Returns:
            str: The corresponding lowercase letter (1 → a, 2 → b, etc.)
        """
        return chr(96 + n)

    def generate(self, recipe_data: dict, output_filename: str) -> None:
        """Generates the recipe PDF from the recipe data.

        Args:
            recipe_data (dict): Dictionary of recipe entries
            output_filename (str): Where to save the rendered PDF
        """
        logger.info("Generating Recipe PDF")

        # Set up the document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            leftMargin=1 * cm,
            rightMargin=1 * cm,
            topMargin=1 * cm,
            bottomMargin=1 * cm,
        )

        story = []

        # Add title and author
        self._add_title_section(story, recipe_data)

        # Add ingredients section
        self._add_ingredients_section(story, recipe_data, doc.width)

        # Add preparation section
        self._add_preparation_section(story, recipe_data)

        # Add steps section
        self._add_steps_section(story, recipe_data)

        # Add notes section
        self._add_notes_section(story, recipe_data)

        # Build the PDF
        doc.build(story)
        logger.info(f"Generated PDF, saved to '{output_filename}'")

    def _add_title_section(self, story: list, recipe_data: dict) -> None:
        """Add the title and author section to the story.

        Args:
            story (list): The story list to append elements to
            recipe_data (dict): The recipe data dictionary
        """
        story.append(Paragraph(recipe_data["title"], self.h1))
        self._add_horizontal_line(story, color=colors.black, width=40)
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"by {recipe_data['author']}", self.h3))
        story.append(Spacer(1, 12))

    def _add_horizontal_line(
        self, story: list, color: colors.Color, width: int
    ) -> None:
        """Add a horizontal line to the story.

        Args:
            story (list): The story list to append elements to
        """
        # Using ReportLab's HRFlowable for a proper horizontal line
        story.append(
            HRFlowable(
                width=f"{width}%",
                thickness=1,
                color=color,
                spaceBefore=4,
                spaceAfter=4,
            )
        )

    def _add_ingredients_section(
        self, story: list, recipe_data: dict, page_width: float
    ) -> None:
        """Add the ingredients section to the story.

        Args:
            story (list): The story list to append elements to
            recipe_data (dict): The recipe data dictionary
            page_width (float): The width of the page
        """
        ingredients = recipe_data[
            "ingredients"
        ]  # list of {'ingredient': str, 'quantity': str}

        story.append(Paragraph("Ingredients", self.h2))

        # Create ingredients grid (3 columns)
        cols = 3
        rows = (len(ingredients) + cols - 1) // cols
        data = []

        # Define a fixed row height
        fixed_row_height = 1.2 * cm

        for r in range(rows):
            row = []
            for c in range(cols):
                idx = r + c * rows
                if idx < len(ingredients):
                    item = ingredients[idx]
                    txt = f"<b>{item['ingredient']}</b>"
                    if item.get("quantity") and item["quantity"] != "N/A":
                        txt += f": {item['quantity']}"
                    row.append(Paragraph(txt, self.body))
                else:
                    row.append("")
            data.append(row)

        table = Table(
            data,
            colWidths=[page_width / cols] * cols,
            rowHeights=[fixed_row_height] * rows,
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.wheat),
                    ("LEFTPADDING", (0, 0), (-1, -1), 15),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    # Ensure text wraps rather than expanding the row
                    ("WORDWRAP", (0, 0), (-1, -1), True),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 12))

    def _add_preparation_section(self, story: list, recipe_data: dict) -> None:
        """Add the preparation section to the story.

        Args:
            story (list): The story list to append elements to
            recipe_data (dict): The recipe data dictionary
        """
        story.append(Paragraph("Preparation", self.h2))
        self._add_horizontal_line(story, color=colors.gray, width=100)

        prep_items = []
        for i, step in enumerate(recipe_data["preparation"], start=1):
            prep_items.append(ListItem(Paragraph(f"{step}", self.body), leftIndent=20))

        story.append(ListFlowable(prep_items, bulletType="bullet", bulletOffsetY=0))
        story.append(Spacer(1, 12))

    def _add_steps_section(self, story: list, recipe_data: dict) -> None:
        """Add the steps section to the story.

        Args:
            story (list): The story list to append elements to
            recipe_data (dict): The recipe data dictionary
        """
        story.append(Paragraph("Steps", self.h2))
        self._add_horizontal_line(story, color=colors.gray, width=100)

        step_items = []
        for step in recipe_data["steps"]:
            step_items.append(ListItem(Paragraph(step, self.body), leftIndent=20))

        story.append(ListFlowable(step_items, bulletType="1", bulletOffsetY=1))
        story.append(Spacer(1, 12))

    def _add_notes_section(self, story: list, recipe_data: dict) -> None:
        """Add the notes section to the story.

        Args:
            story (list): The story list to append elements to
            recipe_data (dict): The recipe data dictionary
        """
        story.append(Paragraph("Notes", self.h2))
        self._add_horizontal_line(story, color=colors.gray, width=100)

        notes = []
        for note in recipe_data["notes"]:
            notes.append(ListItem(Paragraph(note, self.body), leftIndent=20))

        story.append(ListFlowable(notes, bulletType="bullet"))
