import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os

url = "https://aajonus.net/"

try:
    DATA_DIR = Path(__file__).resolve().parent / "data"
except NameError:
    DATA_DIR = Path.cwd() / "data"

DATA_DIR.mkdir(exist_ok=True)

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("div", class_="card-md")

    # Iterate over each article to extract information
    for article in articles:
        # Find the 'a' tag with class 'read-more' which contains the link to the full article
        link_element = article.find("a", class_="read-more")
        if link_element and link_element.get("href"):
            # Get the full URL by appending the href to the base URL
            article_url = url + link_element.get("href").lstrip("/")
            # Fetch the article page
            article_response = requests.get(article_url)
            if article_response.status_code == 200:
                # Parse the article page
                article_soup = BeautifulSoup(article_response.text, "html.parser")
                # Find the 'div' element with class 'content' which contains the text
                content_div = article_soup.find("div", class_="content")
                if content_div:
                    # Extract all paragraph texts from the content div
                    paragraphs = content_div.find_all("p")
                    article_text = "\n\n".join(
                        paragraph.text.strip() for paragraph in paragraphs
                    )
                    # Sanitize the title to be used as a filename
                    title = link_element.text.strip()
                    filename = (
                        title.replace(" ", "_").replace("/", "_").replace('"', "")
                        + ".txt"
                    )
                    # Save the content to a file
                    with open(os.path.join(DATA_DIR, filename), "w") as file:
                        file.write(article_text)
                    print(f'Article "{title}" saved as {filename}.')


# MVP
# Parse per sentence/paragraph

# SciKitLearn TFIDF for search
# Sparse array NumPy
# Create dataframe with this, dataframe.from.sparse

# Sparse vector from input
# dot product against entire dataframe
# Dont remove stop words
# Stemming or not (done before transforming into TFIDF vector)


# Signle column with text in it
# TFIDF vectoriser
# Dot product
