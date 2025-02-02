
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

def text_similarity(sentence1, sentence2):
    # Tokenize the sentences
    tokens1 = word_tokenize(sentence1.lower())
    tokens2 = word_tokenize(sentence2.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens1 = [word for word in tokens1 if word not in stop_words]
    tokens2 = [word for word in tokens2 if word not in stop_words]
    
    # Convert tokens to strings
    sentence1_processed = ' '.join(tokens1)
    sentence2_processed = ' '.join(tokens2)
    
    # Vectorize the sentences
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([sentence1_processed, sentence2_processed])

    # Calculate cosine similarity between the two sentences
    cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return cosine_similarities[0][0]

sentence1 = "This is a sentence."
sentence2 = "This is another sentence sentence."

cosine_similarity_score = text_similarity(sentence1, sentence2)
print("Cosine similarity score:", cosine_similarity_score)
