import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from nltk.util import ngrams
import nltk

nltk.download('punkt')

# JSON data and dataframe
try:
    with open('data/fomc_minutes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: The file 'fomc_minutes.json' was not found.")
    raise

df = pd.DataFrame(data)

# text length
df['text_length'] = df['text'].apply(len)

# Average text length
average_text_length = df['text_length'].mean()
print(f"Average text length: {average_text_length}")

# Distribution of text lengths
plt.figure(figsize=(10, 6))
sns.histplot(df['text_length'], bins=30, kde=True)
plt.title('Distribution of Text Lengths')
plt.xlabel('Text Length')
plt.ylabel('Frequency')
plt.show()

# TF-IDF 
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['text'])
tfidf_feature_names = vectorizer.get_feature_names_out()

# TF-IDF matrix to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_feature_names)

# top 10 words by TF-IDF score
tfidf_scores = tfidf_df.sum().sort_values(ascending=False)
print("Top 10 words by TF-IDF score:")
print(tfidf_scores.head(10))

# N-grams Analysis
def get_ngrams(text, n):
    tokens = nltk.word_tokenize(text)
    n_grams = ngrams(tokens, n)
    return [' '.join(grams) for grams in n_grams]

# check bigrams and trigrams
df['bigrams'] = df['text'].apply(lambda x: get_ngrams(x, 2))
df['trigrams'] = df['text'].apply(lambda x: get_ngrams(x, 3))

# Flatten the list of bigrams and trigrams
all_bigrams = [bigram for sublist in df['bigrams'] for bigram in sublist]
all_trigrams = [trigram for sublist in df['trigrams'] for trigram in sublist]

# extract the most common bigrams and trigrams
bigram_counts = Counter(all_bigrams)
trigram_counts = Counter(all_trigrams)

print("Top 10 bigrams:")
print(bigram_counts.most_common(10))

print("Top 10 trigrams:")
print(trigram_counts.most_common(10))

# Plot the most common bigrams
bigram_df = pd.DataFrame(bigram_counts.most_common(10), columns=['bigram', 'count'])
plt.figure(figsize=(10, 6))
sns.barplot(x='count', y='bigram', data=bigram_df)
plt.title('Top 10 Bigrams')
plt.xlabel('Count')
plt.ylabel('Bigram')
plt.show()

# Plot the most common trigrams
trigram_df = pd.DataFrame(trigram_counts.most_common(10), columns=['trigram', 'count'])
plt.figure(figsize=(10, 6))
sns.barplot(x='count', y='trigram', data=trigram_df)
plt.title('Top 10 Trigrams')
plt.xlabel('Count')
plt.ylabel('Trigram')
plt.show()