from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()
BASE_PATH = os.getenv("BASE_PATH")

app = Flask(__name__)

# Load your processed data (make sure the path is correct)
data_path = f"{BASE_PATH}/data/processed/FINAL_DF.pkl"
df = pd.read_pickle(data_path)

# TF-IDF Vectorization
tf = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=0.0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['book_info'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Get book titles
indices = pd.Series(df['title'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title'].lower()  # Convert input title to lowercase
    lowercase_titles = indices.str.lower()  # Convert all titles in the series to lowercase
    
    if title not in lowercase_titles.values:
        return render_template('index.html', prediction_text="Book not found in the database.")
    
    recommended_books = []
    idx = lowercase_titles[lowercase_titles == title].index[0]  # Find index with case-insensitive match
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_books.append(df['title'].iloc[i])
        
    return render_template('index.html', prediction_text="Top 10 book recommendations:", recommendations=recommended_books)


if __name__ == "__main__":
    app.run(debug=True)
    
##Run "FLASK_APP=src/webapp/app.py flask run"
