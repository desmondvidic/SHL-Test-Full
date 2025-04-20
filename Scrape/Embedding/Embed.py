import json
from sentence_transformers import SentenceTransformer

with open('shl_self_test.json', 'r', encoding='utf-8') as f:
    assessments = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

descriptions = [a["description"] for a in assessments]

embeddings = model.encode(descriptions, show_progress_bar=True)

for i, emb in enumerate(embeddings):
    assessments[i]["embedding"] = emb.tolist()  # Convert NumPy array to list for JSON serialization

with open('embed.json', 'w', encoding='utf-8') as f:
    json.dump(assessments, f, indent=2)
