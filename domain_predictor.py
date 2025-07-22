from transformers import pipeline
from tqdm import tqdm
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("./input/scraped_repo_list.csv", sep=",")
# df.columns = ['name','full_name','html_url','description','fork',
#               'created_at','updated_at','size','stargazers_count',
#               'watchers_count','language','forks_count','archived',
#               'disabled','open_issues_count','license','allow_forking',
#               'visibility','forks','topics','open_issues']

def build_input_text(row):
    parts = [
        str(row.get("name", "")),
        str(row.get("description", "")),
        str(row.get("language", ""))
    ]
    return " ".join(part for part in parts if part and part != 'nan').strip()

candidate_labels = [
    "Machine Learning",
    "Web Development",
    "DevOps",
    "Mobile Development",
    "Security",
    "Data Science",
    "Healthtech",
    "AI",
    "Blockchain",
    "Game Development"
]


device = 0 if torch.cuda.is_available() else -1

classifier = pipeline("zero-shot-classification",
                      model="typeform/distilbert-base-uncased-mnli",
                      device=device)
predicted_domains = []
scores = []

if torch.cuda.is_available():
    total_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
    if total_mem < 4:
        batch_size = 8
    else:
        batch_size = 16
else:
    batch_size = 4

texts = [build_input_text(row) for _, row in df.iterrows()]
for i in tqdm(range(0, len(texts), batch_size)):
    batch_texts = texts[i:i+batch_size]
    filtered_texts = [t for t in batch_texts if t.strip()]
    if not filtered_texts:
        predicted_domains.extend(["Unknown"]*len(batch_texts))
        scores.extend([0.0]*len(batch_texts))
        continue
    results = classifier(filtered_texts, candidate_labels)
    if isinstance(results, dict):
        results = [results]
    j = 0
    for t in batch_texts:
        if not t.strip():
            predicted_domains.append("Unknown")
            scores.append(0.0)
        else:
            res = results[j]
            predicted_domains.append(res["labels"][0])
            scores.append(res["scores"][0])
            j += 1
# for _, row in tqdm(df.iterrows(), total=len(df)):
#     input_text = build_input_text(row)
#     if not input_text.strip():
#         predicted_domains.append("Unknown")
#         scores.append(0.0)
#         continue
#
#     result = classifier(input_text, candidate_labels)
#     predicted_domains.append(result["labels"][0])
#     scores.append(result["scores"][0])

df["predicted_domain"] = predicted_domains
df["domain_confidence"] = scores

df["popularity_score"] = (
    df["stargazers_count"].fillna(0)
    + 2 * df["forks_count"].fillna(0)
    + df["watchers_count"].fillna(0)
)

scaler = MinMaxScaler()
df["popularity_score_normalized"] = scaler.fit_transform(df[["popularity_score"]])

df.to_csv("github_projects_with_domains.csv", index = False)
print("Domains predicted and saved to 'github_projects_with_domains.csv")