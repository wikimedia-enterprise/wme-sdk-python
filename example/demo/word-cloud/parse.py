import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import sys


# Function to extract sections and paragraphs
def extract_sections(json_data):
    extracted_text = []
    if isinstance(json_data, list):
        for item in json_data:
            extracted_text.append(extract_sections(item))
    elif isinstance(json_data, dict):
        if json_data.get("type") == "section":
            section_name = json_data.get("name", "")
            paragraphs = []
            for part in json_data.get("has_parts", []):
                if part.get("type") == "paragraph":
                    paragraphs.append(part.get("value", ""))
            extracted_text.append(f"{section_name}: {' '.join(paragraphs)}")
        for value in json_data.values():
            extracted_text.append(extract_sections(value))
    return ' '.join(filter(None, extracted_text))


# Function to extract sections and paragraphs
if __name__ == '__main__':
    # Check if the title is provided in command-line arguments

    if len(sys.argv) < 2:
        print("Usage: python get.py \"Article Title\"")
        sys.exit(1)

    # Get the article title from the command line
    article_title = sys.argv[1]
    json_path = f"data/{article_title}.json"

    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract and output the text

    plain_text = extract_sections(data)
    print("Extracted text:")
    print(plain_text)

    # Clean and split the plain text into words
    words = re.findall(r'\w+', plain_text.lower())
    word_freq = Counter(words)

    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(plain_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # Plotting the top 10 words in a bar chart
    top_words = word_freq.most_common(10)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Words')
    plt.show()
