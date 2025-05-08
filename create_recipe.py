import argparse
import logging

from src.processor import process_url
from src.logger import logger


def main():
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
    if args.save_html:
        logger.info("HTML saving is enabled.")

    process_url(
        url=args.url, recipe_output_dir=args.output_dir, save_html=args.save_html
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        required=True,
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
        "--save_html",
        required=False,
        action="store_true",
        help="Flag to save the HTML of the page",
    )
    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="Whether to display logs",
    )

    main()
