import argparse
import logging

from src.processor import process_url, generate_from_txt
from src.logger import logger


def main() -> None:
    """Main function to handle command line arguments and process the recipe generation."""
    args = parser.parse_args()

    if args.verbose:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    logger.info("Starting recipe creation process...")
    logger.info(f"Video URL: {args.url}")
    logger.info(f"Saving to: {args.output_dir}")

    if args.url:
        process_url(
            url=args.url,
            recipe_output_dir=args.output_dir,
            save_sections_json=args.save_sections_file,
        )
    elif args.section_file:
        generate_from_txt(
            recipe_output_dir=args.output_dir,
            response_path=args.section_file,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        required=False,
        type=str,
        help="URL to youtube video to generate recipe from",
    )
    parser.add_argument(
        "--output_dir",
        required=False,
        type=str,
        default="recipes/",
        help="Directory to save recipes to",
    )
    parser.add_argument(
        "--section_file",
        required=False,
        type=str,
        help="Directory to save recipes to",
    )
    parser.add_argument(
        "--save_sections_file",
        required=False,
        action="store_true",
        help="Path to the file containing the previously generated parsed sections",
    )
    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="Whether to display logs",
    )

    # verfy inputs
    args = parser.parse_args()
    if args.url is None and args.section_file is None:
        parser.error(
            "Either a URL or a section file is required. Please provide one of them."
        )
    if args.url and args.section_file:
        parser.error(
            "Please provide either a URL or a section file, not both. "
            "The URL will be used to generate the recipe PDF."
        )
    logger.info("Arguments parsed successfully.")
    main()
