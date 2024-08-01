# -*- coding: utf-8 -*-
"""LLM ASSIGNMENT 3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qx1kt6O2g7du087S4Tn540Tc3HQnC5X1
"""

# Install the datasets library
!pip install datasets
from datasets import load_dataset

import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn
import pandas as pd

"""Emotion is a dataset of English Twitter messages with six basic emotions: anger, fear, joy, love, sadness, and surprise. For more detailed information please refer to the paper."""

# Load the emotion dataset which contains the twitter dataset labelled as emotions.
dataset = load_dataset("dair-ai/emotion","split", trust_remote_code=True)

# Display the dataset structure
print(dataset)

"""Purpose: Convert the dataset splits into Pandas DataFrames for easier manipulation and analysis."""

# Convert to pandas DataFrame
df_train = dataset['train'].to_pandas()
df_valid = dataset['validation'].to_pandas()
df_test = dataset['test'].to_pandas()

# Display basic information
print(df_train.info())

# Display the first few rows of the training set
print(df_train.head())

# Display unique values in the 'label' column
print("Unique labels in training set:")
print(df_train['label'].unique())

# Define the label-to-emotion mapping based on the dataset's documentation
emotion_labels = {
    0: 'sadness',
    1: 'joy',
    2: 'love',
    3: 'anger',
    4: 'fear',
    5: 'surprise'
}

# Map numeric labels to emotion labels
df_train['emotion'] = df_train['label'].map(emotion_labels)

# Display the mapping for verification
print(df_train[['label', 'emotion']].drop_duplicates())

# Method to convert numeric labels to string emotions
def int2str(label):
    return emotion_labels[label]

# Apply the method to the DataFrame
df_train['emotion'] = df_train['label'].apply(int2str)

# Display the mapping for verification
print(df_train[['label', 'emotion']].drop_duplicates())

# Display a few rows to verify the mapping
print(df_train[['text', 'label', 'emotion']].head())

# Plot the distribution of emotion labels
plt.figure(figsize=(10, 6))
sns.countplot(data=df_train, x='emotion', order=df_train['emotion'].value_counts().index)
plt.title('Distribution of Emotion Labels in the Training Set')
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.show()

"""So here the most common is joy and least sentences are of surprise

Analyze if text length varies across different emotions using a boxplot.
"""

# Calculate text lengths
df_train['text_length'] = df_train['text'].apply(len)

# Plot text length distribution by emotion
plt.figure(figsize=(12, 8))
sns.boxplot(data=df_train, x='emotion', y='text_length', order=df_train['emotion'].value_counts().index)
plt.title('Text Length Distribution by Emotion')
plt.xlabel('Emotion')
plt.ylabel('Text Length')
plt.show()

"""Text length doesnt influence the emotion"""

# Display sample texts for each emotion
for emotion in df_train['emotion'].unique():
    print(f"\nSamples for emotion: {emotion}")
    print(df_train[df_train['emotion'] == emotion]['text'].head(), "\n")

from wordcloud import WordCloud

# Combine all text into a single string
text = ' '.join(df_train['text'].tolist())

# Generate a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Plot the word cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for Training Set')
plt.show()

"""most common words are feel, feeling, know, will, think, make, really, thing , way etc.

Verify unique emotions and their counts in the training set.
"""

# Display the unique emotions in the training set
unique_emotions = df_train['emotion'].unique()
print("\nUnique emotions in the training set:")
print(unique_emotions)

# Display the distribution of emotions in the training set
emotion_counts = df_train['emotion'].value_counts()
print("\nDistribution of emotions in the training set:")
print(emotion_counts)

# Display sample texts for each emotion
for emotion in unique_emotions:
    print(f"\nSamples for emotion: {emotion}")
    print(df_train[df_train['emotion'] == emotion]['text'].head(), "\n")

!pip install nltk
# Install necessary libraries
!pip install datasets nltk wordcloud seaborn
import nltk
from nltk.tokenize import word_tokenize
# Download necessary NLTK data
nltk.download('punkt')

# Calculate the number of words in each tweet
df_train['word_count'] = df_train['text'].apply(lambda x: len(x.split()))

# Plot the distribution of word counts
plt.figure(figsize=(10, 6))
sns.histplot(df_train['word_count'], bins=30, kde=True)
plt.title('Distribution of Word Counts in Tweets')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

# Ensure nltk is imported and the necessary resources are downloaded
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
# Tokenize the text data
df_train['tokens'] = df_train['text'].apply(word_tokenize)

# Display a few rows to verify the tokenization
print(df_train[['text', 'tokens', 'emotion']].head())

# Calculate the number of tokens in each tweet (using the previously tokenized text)
df_train['token_count'] = df_train['tokens'].apply(len)

# Plot the distribution of token counts
plt.figure(figsize=(10, 6))
sns.histplot(df_train['token_count'], bins=30, kde=True)
plt.title('Distribution of Token Counts in Tweets')
plt.xlabel('Token Count')
plt.ylabel('Frequency')
plt.show()

# Display summary statistics for word and token counts
print(df_train[['word_count', 'token_count']].describe())

# Character Tokenization
df_train['char_tokens'] = df_train['text'].apply(list)

# Display a few rows to verify the tokenization
print(df_train[['text', 'char_tokens']].head())

""" Tokenize the text data to prepare for further text analysis tasks."""

# Create a set of all unique characters in the text data
unique_chars = set(''.join(df_train['text'].tolist()))

# Display the unique characters
print(f"Unique characters: {unique_chars}")

# Create a mapping from each character to a unique integer
token2idx = {char: idx for idx, char in enumerate(unique_chars)}

# Display the token2idx mapping
print(f"Character to Integer Mapping (token2idx): {token2idx}")

# Convert each character in the text to its corresponding integer
df_train['char_ids'] = df_train['text'].apply(lambda x: [token2idx[char] for char in x])

# Display a few rows to verify the conversion
print(df_train[['text', 'char_ids']].head())

# Create a reverse mapping from integer to character
idx2token = {idx: char for char, idx in token2idx.items()}

# Display the reverse mapping
print(f"Integer to Character Mapping (idx2token): {idx2token}")

# Define a function to reconstruct text from character IDs
def reconstruct_text(char_ids):
    return ''.join([idx2token[idx] for idx in char_ids])

# Apply the function to the DataFrame
df_train['reconstructed_text'] = df_train['char_ids'].apply(reconstruct_text)

# Display a few rows to verify the reconstruction
print(df_train[['text', 'char_ids', 'reconstructed_text']].head())

# Tokenize the text data using DistilBERT's tokenizer
df_train['bert_tokens'] = df_train['text'].apply(lambda x: tokenizer.tokenize(x))

# Display a few rows to verify the tokenization
print(df_train[['text', 'bert_tokens']].head())

from sklearn.preprocessing import MinMaxScaler

# Check for missing values
print(df_train.isnull().sum())

# If there are missing values, handle them (e.g., fill with a placeholder or drop rows)
df_train.dropna(inplace=True)

# Apply MinMaxScaler to scale 'text_length', 'word_count', and 'token_count'
scaler = MinMaxScaler()

# Fit and transform the columns
df_train[['text_length', 'word_count', 'token_count']] = scaler.fit_transform(df_train[['text_length', 'word_count', 'token_count']])

# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("Tahsin/distilbert-base-uncased-finetuned-emotion")
model = AutoModelForSequenceClassification.from_pretrained("Tahsin/distilbert-base-uncased-finetuned-emotion")

# Define a function to tokenize, encode, and pad sequences
def tokenize_and_encode(text):
    encoded = tokenizer.encode_plus(
        text,
        add_special_tokens=True,  # Add [CLS] and [SEP] tokens
        max_length=512,  # Pad & truncate all sentences to 512 tokens
        padding='max_length',  # Pad sentences to the max length
        truncation=True,  # Truncate sentences to the max length
        return_attention_mask=True,  # Return attention mask
        return_tensors='pt',  # Return PyTorch tensors
    )
    return encoded['input_ids'].flatten(), encoded['attention_mask'].flatten()

# Apply the function to the DataFrame
df_train['bert_input'] = df_train['text'].apply(tokenize_and_encode)

# Split the tuple into separate columns
df_train[['input_ids', 'attention_mask']] = pd.DataFrame(df_train['bert_input'].tolist(), index=df_train.index)

# Display a few rows to verify the encoding
print(df_train[['text', 'input_ids', 'attention_mask']].head())

# Apply the function to the DataFrame
df_train['bert_input'] = df_train['text'].apply(tokenize_and_encode)

# Split the tuple into separate columns
df_train[['input_ids', 'attention_mask']] = pd.DataFrame(df_train['bert_input'].tolist(), index=df_train.index)

# Display a few rows to verify the encoding
print(df_train[['text', 'input_ids', 'attention_mask']].head())