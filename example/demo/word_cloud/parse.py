"""Analyzes and visualizes text from a structured content JSON file.

This script loads a JSON file specified by a command-line argument
(expecting an "Article Title" which maps to a local file, e.g.,
"data/My_Article_Title.json").

It recursively extracts plain text from all "section" and "paragraph"
components within the JSON, then performs a word frequency analysis
to generate and display two visualizations using Matplotlib:

1. A word cloud of the entire text.
2. A bar chart of the top 10 most frequent words.

The full extracted text is also printed to the console.
"""

import json
from collections import Counter
import re
import sys
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_sections(data_node):
    """Recursively extracts and joins text from sections and paragraphs.

    This function traverses the nested dictionary/list structure of the
    JSON data. It specifically looks for dictionaries with a "type" of
    "section". For these, it concatenates the section's "name" with the
    "value" of any child parts that have a "type" of "paragraph".

    It only recurses into lists or into the "has_parts" key of a dict.

    Args:
        data_node (dict | list): The JSON data (or sub-structure) to parse.

    Returns:
        str: A single, space-joined string of all extracted text found
             within the given data structure.
    """
    extracted_text = []

    if isinstance(data_node, list):
        # If it's a list, recurse on every item
        for item in data_node:
            extracted_text.append(extract_sections(item))

    elif isinstance(data_node, dict):
        # This is what we want:
        if data_node.get("type") == "section":
            section_name = data_node.get("name", "")
            paragraphs = []

            # Recurse *only* on the 'has_parts' key for this section
            for part in data_node.get("has_parts", []):
                if part.get("type") == "paragraph":
                    paragraphs.append(part.get("value", ""))
                else:
                    # This allows us to find nested sections
                    paragraphs.append(extract_sections(part))

            # We join all found paragraphs/sub-sections for this section
            section_text = ' '.join(filter(None, paragraphs))
            if section_text:
                extracted_text.append(f"{section_name}: {section_text}")

    return ' '.join(filter(None, extracted_text))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse.py \"Article Title\"")
        sys.exit(1)

    article_title = sys.argv[1]
    # Sanitize title to match the filename saved by get.py
    safe_title = article_title.replace(" ", "_").replace("/", "_")
    JSON_PATH = f"data/{safe_title}.json"

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("Error: File not found at %s", JSON_PATH)
        logger.error("Please run the 'get.py' script first to download the data.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Error: Could not parse JSON from %s.", JSON_PATH)
        logger.error("The file might be empty or corrupt. Try running 'get.py' again.")
        sys.exit(1)

    # Extract and output the text
    logger.info("Extracting text from JSON...")

    # --- THIS IS THE FIX ---
    # Look for 'article_sections', which is what get.py saves
    article_sections = data.get('article_sections', [])
    PLAIN_TEXT = extract_sections(article_sections)

    if not PLAIN_TEXT:
        # Updated the error message to be correct
        logger.error("Error: No text could be extracted from the 'article_sections' key.")
        logger.error("Please ensure the 'get.py' script ran successfully and created a valid JSON file.")
        sys.exit(1)

    print("--- Extracted Text ---")
    print(PLAIN_TEXT)
    print("----------------------")

    # Clean and split the plain text into words
    logger.info("Analyzing word frequency...")
    words = re.findall(r'\w+', PLAIN_TEXT.lower())
    word_freq = Counter(words)

    if not word_freq:
        logger.error("Error: No words were found after cleaning the text.")
        sys.exit(1)

    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

    # Display the word cloud
    logger.info("Displaying Word Cloud (close window to see next chart)...")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # Plotting the top 10 words in a bar chart
    logger.info("Displaying Top 10 Words (close window to exit)...")
    top_words = word_freq.most_common(10)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Words')
    plt.show()
