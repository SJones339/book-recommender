#---------------------------------------------------------
# SETUP
#---------------------------------------------------------
import pandas as pd
import string
string.punctuation

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data (run once if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

df = pd.read_pickle("../../data/raw/01_data_processed.pkl")

#---------------------------------------------------------
# HANDLING MISSING VALUES
#---------------------------------------------------------

#Checking how many missing values
missing_values = df.isnull().sum()
total_entries = len(df)
missing_percentage = (missing_values / total_entries) * 100

# Display the percentage of missing values per column
print("Percentage of Missing Values per Column:")
print(missing_percentage)

columns = list(df.columns)

#If the percent of missing values is below 20% then drop that column
threshold = 20

for column in columns:
    if missing_percentage[column] > threshold:
        df = df.drop(columns=column)

#Handle the rest of the missing values by just dropping rows with No value
df = df.dropna()

#---------------------------------------------------------
# PREPARING "DESCRIPTION" COLUMN FOR NLP
#---------------------------------------------------------
description_df = df.copy().reset_index()

# Punctuation Removal
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

# Storing the puntuation free text
description_df['clean_msg']= description_df['description'].apply(lambda x:remove_punctuation(x))
description_df["description"].iloc[0]
description_df["clean_msg"].iloc[0]

# Lowercasing all letters
description_df['msg_lower']= description_df['clean_msg'].apply(lambda x: x.lower())
description_df["description"].iloc[0]
description_df["msg_lower"].iloc[0]

# Tokenizing words
def tokenization(text):
    return word_tokenize(text)

description_df['msg_tokenized']= description_df['msg_lower'].apply(lambda x: tokenization(x))
description_df["description"].iloc[0]
description_df["msg_tokenized"].iloc[0]

# Removing stopwords
stop_words = set(stopwords.words('english'))
description_df['msg_no_stopwords'] = description_df['msg_tokenized'].apply(lambda x: [word for word in x if word not in stop_words])
description_df["description"].iloc[0]
description_df["msg_no_stopwords"].iloc[0]

#Lemmitizer
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text

description_df['msg_lemmatized']=description_df['msg_no_stopwords'].apply(lambda x:lemmatizer(x))
comparison_df = description_df[['msg_no_stopwords', 'msg_lemmatized']].head(10)

description_df.to_pickle("../../data/processed/tokenized_data.pkl")



