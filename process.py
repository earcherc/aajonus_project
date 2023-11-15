import pandas as pd
from nltk.tokenize import sent_tokenize
import os
from pathlib import Path
import re
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
nlp.add_pipe("sentencizer")

# Define the directory where your text files are stored
try:
    DATA_DIR = Path(__file__).resolve().parent / "data"
except NameError:
    DATA_DIR = Path.cwd() / "data"

DATA_DIR.mkdir(exist_ok=True)

# Initialize a list to store your data
data = []

# Iterate over each file in the directory (list directory)
for filename in os.listdir(DATA_DIR):
    print(filename)
    if filename.endswith(".txt"):
        # Create the full filepath
        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # Use spaCy to tokenize the content into sentences
            doc = nlp(content)
            sentences = [sent.text.strip() for sent in doc.sents]
            # Append each sentence to your data list, along with the filename
            for sentence in sentences:
                data.append({"filename": filename, "sentence": sentence})

# Create a DataFrame
df = pd.DataFrame(data)
print(df.head(10))


# Example preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers (optional, based on your need)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    # Tokenize into words
    words = text.split()
    # Remove stopwords (optional)
    words = [word for word in words if word not in stopwords.words("english")]
    # Stemming (optional)
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    # Join words back into a single string
    return " ".join(words)


# Apply the preprocessing function to each sentence
# df["cleaned_sentence"] = df["sentence"].apply(preprocess_text)
