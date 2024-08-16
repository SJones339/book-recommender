#-------------------------------------------------------------
#SETUP
#-------------------------------------------------------------
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()
BASE_PATH = os.getenv("BASE_PATH")

df = pd.read_pickle(f'{BASE_PATH}/data/processed/tokenized_data.pkl')
#Put this in the .env
#/Users/stephen/Desktop/book_recommender/data/processed
#-------------------------------------------------------------
#CLEANING DATAFRAME AND JOINING TOKENS
#-------------------------------------------------------------
#Combining tokens in lemmatized_text
cleaned_df = df.copy()
cleaned_df['lemmatized_text'] = cleaned_df['msg_lemmatized'].apply(lambda x: ' '.join(x))

#dropping unnecesarry features
columns_to_drop = ["msg_lemmatized", "msg_no_stopwords", "msg_tokenized", "msg_tokenied", "msg_lower", "clean_msg", "description", "authors", "published_date", "index"]
cleaned_df.drop(columns=columns_to_drop, inplace=True, axis=1)

#-------------------------------------------------------------
#COMBINING FEATURES
#-------------------------------------------------------------

#Combining features
cleaned_df["book_info"] = cleaned_df["lemmatized_text"] + " " + cleaned_df["categories"] 
#deleting the lemmatized_text and categories columns
cleaned_df.drop(['lemmatized_text','categories'],inplace=True, axis=1)
cleaned_df.sample(3)

cleaned_df.to_pickle("../../data/processed/FINAL_DF.pkl")

"""""
#-------------------------------------------------------------
#TF-IDF VECTORIZATION and COSINE SIMILARITY
#-------------------------------------------------------------
tf = TfidfVectorizer(analyzer = "word", ngram_range=(1,2), min_df=0.0, stop_words='english')

tfidf_matrix = tf.fit_transform(cleaned_df['book_info'])

cosine_sim =  cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim)

#-------------------------------------------------------------
#NEXT STEPS + RECOMMENDATION FUNCTION
#-------------------------------------------------------------
#Converting the book title column into a PD Series
indices = pd.Series(cleaned_df['title'])
indices[:5]

#Recommendation Function

def recommend(title, cosine_sim = cosine_sim):
    if title not in indices.values:
        return "Title not found in the database."
    recommended_books = []
    idx = indices[indices == title].index[0]   # to get the index of book name matching the input book_name
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)   # similarity scores in descending order
    top_10_indices = list(score_series.iloc[1:11].index)   # to get the indices of top 10 most similar books
    # [1:11] to exclude 0 (index 0 is the input book itself)
    
    for i in top_10_indices:   # to append the titles of top 10 similar booksto the recommended_books list
        recommended_books.append(list(cleaned_df['title'])[i])
        
    return recommended_books

recommend('Fantasy')

"""


