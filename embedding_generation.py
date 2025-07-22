from sentence_transformers import SentenceTransformer
import pandas as pd
import torch

df = pd.read_csv("./github_projects_with_domains.csv")

df["embedding_text"] = (
    df["name"].fillna("") + " " +
    df["description"].fillna("") + " " +
    df["predicted_domain"].fillna("") + " " +
    df["language"].fillna("")
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

embeddings = model.encode(
    df["embedding_text"].tolist(),
    normalize_embeddings=True,
    show_progress_bar=True,
    batch_size=8
)

df["embedding"] = embeddings.tolist()
df.to_parquet("project_embeddings.parquet", index=False)
