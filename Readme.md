
# Simple Search Engine

This is a simple search engine implementation using the BM25 algorithm for ranking documents. It is designed to index and search through a collection of documents, providing a ranked list of documents that best match a given query.

## Features

- **BM25 Ranking:** Uses the BM25 algorithm to rank documents based on their relevance to the search query.
- **Normalization:** Removes punctuation and converts text to lowercase for more effective indexing and searching.
- **JSON Loading:** Allows loading documents from JSON files for indexing.
- **Pickle Serialization:** Supports saving and loading the index to and from a file using pickle for persistence.

## Usage

### Indexing Documents

You can index documents individually or in bulk. Each document should have a unique URL and associated text content.

```python
from search_engine import SearchEngine

# Create a search engine instance
search_engine = SearchEngine()

# Index a single document
search_engine.index(url="https://example.com", content="This is an example document.")

# Index multiple documents at once
documents = [
    ("https://example.com/doc1", "First example document."),
    ("https://example.com/doc2", "Second example document."),
]
search_engine.bulk_index(documents)
```

### Searching

To search for a query, simply call the `search` method with your query string. The method will return a sorted dictionary of URLs with their corresponding BM25 scores.

```python
# Search for a query
results = search_engine.search("example query")
print(results)
```

### Loading and Saving Index

You can save the current index to a file and load it later to avoid re-indexing documents every time.

```python
# Save the index to a file
search_engine.save_index("search_index.pkl")

# Load the index from a file
search_engine.load_index("search_index.pkl")
```

### Loading Documents from JSON

You can also load documents directly from a JSON file. The JSON file should contain a list of objects, each with a `url` and `text` field.

```python
# Load documents from a JSON file
search_engine.load_from_json("documents.json")
```

## Requirements

- Python 3.6 or higher
- No external dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
