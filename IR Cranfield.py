# Importing necessary packages and libraries
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Loading the dataset
file_path = os.path.join(os.getcwd(), 'cran.all.1400')
docs=[]
# reading the contents of the file into a string
with open(file_path, 'r') as f:
    docs.append(f.read())

# Loading the stop words
stop_words = set(stopwords.words('english'))

# Initializing the Porter Stemmer
porter=PorterStemmer()

doc_tokens = []
for i, doc in enumerate(docs):
    # Tokenizing the documents
    tokens = nltk.word_tokenize(doc)
    
    # Case folding and removing punctuation
    tokens = [token.lower() for token in tokens if token.isalpha()]
    
    # Removing stop words
    tokens = [token for token in tokens if token not in stop_words]
    
    # Applying Porter stemming algorithm
    tokens = [porter.stem(token) for token in tokens]
    
    # Adding (term, docID) pairs to list
    for token in set(tokens):
        doc_tokens.append((token, i))

inverted_index = {}
for token, docID in doc_tokens:
    if token in inverted_index:
        if docID in inverted_index[token]:
            inverted_index[token][docID] += 1
        else:
            inverted_index[token][docID] = 1
    else:
        inverted_index[token] = {docID: 1}

term_freqs = [(token, sum(postings.values())) for token, postings in inverted_index.items()]
term_freqs = sorted(term_freqs, key=lambda x: x[1], reverse=True)

term_freqs = term_freqs[30:]

dictionary = [term for term, freq in term_freqs]


doc_tokens = sorted(doc_tokens, key=lambda x: (x[0], x[1]))

nonpositional_index = {}
for i, (token, docID) in enumerate(doc_tokens):
    if token in dictionary:
        if token in nonpositional_index:
            if docID in nonpositional_index[token]:
                nonpositional_index[token][docID].append(i)
            else:
                nonpositional_index[token][docID] = [i]
        else:
            nonpositional_index[token] = {docID: [i]}

# Tokens and their respective docIDs and positions
for token, postings in nonpositional_index.items():
    print(token + ':')
    for docID, positions in postings.items():
        print('\t' + str(docID) + ':', len(positions))


file_path = os.path.join(os.getcwd(), 'cran.all.1400')
# reading the contents of the file into a string
with open(file_path, 'r') as f:
    text=f.read()

docs = nltk.sent_tokenize(text.lower())

inverted_index = {}
stopwords = set(stopwords.words('english'))

stemmer = PorterStemmer()


import re
for i, doc in enumerate(docs):
    # tokenizing the document and removing the stopwords
    words = re.findall('\w+', doc)
    words = [w for w in words if w not in stopwords]
    words = [stemmer.stem(w) for w in words]
    
    # updating the inverted index
    for word in words:
        if word in inverted_index:
            if i not in inverted_index[word]:
                inverted_index[word].append(i)
        else:
            inverted_index[word] = [i]


import random
random.seed(42)
# 10 Information needfrom the dataset
info_needs = random.sample(range(1, 1411), 10)


print("\n\nDictionary: \n", dictionary)
print("\n\nInverted Index: \n", inverted_index)

file_path1 = os.path.join(os.getcwd(), 'cran.qry')
file_path2= os.path.join(os.getcwd(),'cranqrel')
for info_need in info_needs:
    print(f"Information Need {info_need}:")
    with open(file_path1, 'r') as f:
        query = f.read().lower()
    query_words = re.findall('\w+', query)
    query_words = [w for w in query_words if w not in stopwords]
    query_words = [stemmer.stem(w) for w in query_words]

    # Relevant documents which has relevance score < 3
    relevant_docs = [int(line.split()[1]) for line in open(file_path2, 'r') if int(line.split()[2]) < 3]
    relevant_docs = set(relevant_docs)
    retrieved_docs = set()
    
    # Precision and Recall
    for word in query_words:
        if word in inverted_index:
            retrieved_docs.update(set(inverted_index[word]))
    tp = len(relevant_docs.intersection(retrieved_docs))
    fp = len(retrieved_docs.difference(relevant_docs))
    fn = len(relevant_docs.difference(retrieved_docs))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print(f"Precision: {precision:.3f}, Recall: {recall:.3f}\n")
print("\n\nRelevant Docs: \n", relevant_docs)
