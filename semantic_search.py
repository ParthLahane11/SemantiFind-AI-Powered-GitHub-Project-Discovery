import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
from parser import extract_k_category_metric

df = pd.read_parquet("project_embeddings.parquet")

embeddings = np.array(df["embedding"].to_list()).astype("float32")

faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "project_index.faiss")

df.drop(columns=["embedding"]).to_parquet("project_metadata.parquet",
                                          index=False)
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda" if torch.cuda.is_available() else "cpu")


def search_projects(query: str, df, index, model):
    k, category, metric = extract_k_category_metric(query)

    filtered_df = df
    if category:
        filtered_df = df[df["predicted_domain"].str.lower() == category]

    if filtered_df.empty:
        return pd.DataFrame()

    embeddings = np.array(filtered_df["embedding"].tolist()).astype("float32")
    faiss.normalize_L2(embeddings)

    filtered_index = faiss.IndexFlatIP(embeddings.shape[1])
    filtered_index.add(embeddings)

    query_vec = model.encode(query, normalize_embeddings=True)
    query_vec = np.array([query_vec], dtype="float32")

    scores, indices = filtered_index.search(query_vec, k)

    results = filtered_df.iloc[indices[0]].copy()
    results["score"] = scores[0]

    if metric and metric in results.columns:
        results = results.sort_values(by=metric, ascending=False)

    return results.head(k)

# query = "Top seven most popular projects in DevOps category"
# query = "Most popular project in AI category"
# query = "Framework for training neural networks"
query = "Top 10 tools for Python data visualization"
results = search_projects(query, df, index, model)
print(results[["name", "full_name", "html_url"]])