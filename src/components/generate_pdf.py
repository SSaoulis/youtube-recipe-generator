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
)
from reportlab.lib import colors

from src.logger import logger


def letter_index(n: int) -> str:
    """1 → a, 2 → b, …"""
    return chr(96 + n)


def generate_recipe_pdf(recipe_data: dict, output_filename: str) -> None:
    """Generates the report pdf from the recipe data extracted with gemini.

    Args:
        recipe_data (dict): Dictionary of recipe entries
        output_filename (str): Where to save the rendered PDF.
    """
    logger.info("Generating Recipe PDF")
    # 1) Set up the document
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
    )
    styles = getSampleStyleSheet()

    h1 = ParagraphStyle(
        "RecipeTitle", parent=styles["Title"], alignment=1, spaceAfter=12
    )
    h2 = ParagraphStyle(
        "SectionTitle", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6
    )
    h3 = ParagraphStyle(
        "Author",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=colors.grey,
        alignment=1,
        spaceAfter=12,
    )

    body = styles["BodyText"]

    story = []

    # Title + author
    story.append(Paragraph(recipe_data["title"], h1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"by {recipe_data['author']}", h3))
    story.append(Spacer(1, 12))

    # 3) Ingredients grid (2 columns)
    ingredients = recipe_data[
        "ingredients"
    ]  # list of {'ingredient': str, 'quantity': str}
    cols = 3
    rows = (len(ingredients) + cols - 1) // cols
    data = []
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = r + c * rows
            if idx < len(ingredients):
                item = ingredients[idx]
                txt = f"<b>{item['ingredient']}</b>"
                if item.get("quantity") and item["quantity"] != "N/A":
                    txt += f": {item['quantity']}"
                row.append(Paragraph(txt, body))
            else:
                row.append("")
        data.append(row)

    table = Table(data, colWidths=[doc.width / cols] * cols)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.wheat),
                ("LEFTPADDING", (0, 0), (-1, -1), 15),
                ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(Paragraph("Ingredients", h2))
    story.append(table)
    story.append(Spacer(1, 12))

    # 4) Preparation list
    story.append(Paragraph("Preparation", h2))
    prep_items = []
    for i, step in enumerate(recipe_data["preparation"], start=1):
        prep_items.append(ListItem(Paragraph(f"{step}", body), leftIndent=12))
    story.append(ListFlowable(prep_items, bulletType="bullet"))
    story.append(Spacer(1, 12))

    # 5) Steps
    story.append(Paragraph("Steps", h2))
    step_items = []
    for step in recipe_data["steps"]:
        step_items.append(ListItem(Paragraph(step, body), leftIndent=12))
    story.append(ListFlowable(step_items, bulletType="1"))
    story.append(Spacer(1, 12))

    # 6) Notes (two‐column if you like)
    story.append(Paragraph("Notes", h2))
    notes = recipe_data.get("notes", [])
    for note in notes:
        story.append(Paragraph(f"– {note}", body))

    doc.build(story)
    logger.info(f"Generated PDF, saved to '{output_filename}'")
