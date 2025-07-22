# SemantiFind – AI-Powered GitHub Project Discovery

**SemantiFind** is a semantic search tool designed to help users discover open-source GitHub projects that align with specific topics, domains, and potential licensing interests. Leveraging state-of-the-art language models and vector search (FAISS), the system enables natural language queries like:

> "Top 7 most popular projects in DevOps"  
> "Find Python projects related to medical imaging"  
> "Most starred AI projects in healthcare"

---

## 🚀 Features

- 🔍 **Natural Language Querying**  
  Search for GitHub repositories using intuitive, flexible queries.

- 💡 **Semantic Search with Sentence Transformers**  
  Embeddings powered by `all-MiniLM-L6-v2`.

- ⚡ **Fast Retrieval with FAISS**  
  High-performance approximate nearest neighbor search.

- 📊 **Enriched Metadata**  
  Each project includes name, description, domain, language, and popularity indicators (e.g., stars).

---

## 📂 Project Structure

```
SemantiFind/
├── app.py                        # Flask app entrypoint
├── embedding_projects.py         # Embeds project descriptions using SentenceTransformer
├── build_index.py                # Builds FAISS index from the embeddings
├── query_engine.py               # Parses and executes semantic queries
├── github_projects_with_domains.csv  # Source dataset
├── project_embeddings.parquet    # Output embeddings
├── faiss_index.index             # Serialized FAISS index
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SemantiFind-AI-Powered-GitHub-Project-Discovery.git
cd SemantiFind-AI-Powered-GitHub-Project-Discovery
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Build Embeddings and FAISS Index

```bash
python embedding_projects.py
python build_index.py
```

### 5. Run the Web App

```bash
python app.py
```

---

## 🧠 Example Queries

- "Top 10 machine learning projects in healthcare"
- "Most popular Python projects for data visualization"
- "Find licensing-friendly cybersecurity tools"

---

## 📈 Technology Stack

- [Sentence Transformers](https://www.sbert.net/)
- [FAISS – Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
- [spaCy NLP](https://spacy.io/)
- Flask (for web serving)

---

## 📘 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙌 Acknowledgments

Thanks to the open-source community and the developers of Sentence Transformers, FAISS, and spaCy for making semantic search both powerful and accessible.

