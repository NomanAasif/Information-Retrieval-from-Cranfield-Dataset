# Information Retrieval from Cranfield Dataset

Following are the tasks addressed in this project

- Tokenized documents from [cranfield dataset](https://ir-datasets.com/cranfield.html).
- Applied case folding & sorted distinct words in descending order of their frequencies to remove top 30 stopwords. 
- Applied Porter Stemming algorithm and listed all terms to be included in the dictionary.
- Generated all (term, docID) pairs and a sort-based algorithm to build the non-positional inverted index (stored in dictionary data structure and that includes document frequency).
- Randomly chosen 10 information need. Documents are termed 'relevant' only if relevance score < 3, based on which precision and recall are obtained.
