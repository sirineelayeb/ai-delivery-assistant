import os
from dotenv import load_dotenv
from pymongo import MongoClient
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from bson import ObjectId

# --- Load environment variables ---
load_dotenv()

# --- MongoDB connection ---
uri = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@" \
      f"{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client[os.getenv("MONGO_DB")]

# Collections
deliveries_col = db["deliveries"]
users_col = db["users"]
companies_col = db["companies"]
vehicles_col = db["vehicles"]

print("MongoDB connected successfully!")

# --- Load deliveries from DB ---
deliveries = list(deliveries_col.find())
print(f"Loaded {len(deliveries)} deliveries from database.")

# --- Human-readable info helper ---
def get_human_readable_info(delivery):
    """Replace IDs with readable names or meaningful info."""
    user_doc = users_col.find_one({"_id": ObjectId(delivery.get("user"))}) if delivery.get("user") else None
    company_doc = companies_col.find_one({"_id": ObjectId(delivery.get("company"))}) if delivery.get("company") else None
    vehicle_doc = vehicles_col.find_one({"_id": ObjectId(delivery.get("vehicleId"))}) if delivery.get("vehicleId") else None

    vehicle_info = f"{vehicle_doc.get('model', 'Unknown Model')} ({vehicle_doc.get('licensePlate', 'Unknown Plate')})" if vehicle_doc else "Unknown Vehicle"

    return {
        "user": user_doc.get("name") if user_doc else "Unknown User",
        "company": company_doc.get("name") if company_doc else "Unknown Company",
        "vehicle": vehicle_info,
        "status": delivery.get("status", "Unknown Status"),
        "package_id": str(delivery.get("_id"))
    }

# --- Prepare embeddings for semantic search ---
texts = [
    f"Delivery {str(d.get('_id'))} for user {d.get('user')} is {d.get('status')} via vehicle {d.get('vehicleId')} for company {d.get('company')}"
    for d in deliveries
]

emb_model = SentenceTransformer('all-MiniLM-L6-v2')
if texts:
    embeddings = np.array([emb_model.encode(t) for t in texts], dtype='float32')
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
else:
    index = None

# --- Search function with threshold ---
def search(query: str):
    query_clean = query.strip()
    if not query_clean:
        return "No valid question provided."

    if not deliveries:
        return "No deliveries in the database yet."

    # --- Exact match on package ID ---
    for d in deliveries:
        if str(d["_id"]) == query_clean or str(d["_id"]) in query_clean:
            info = get_human_readable_info(d)
            return (f"Delivery {info['package_id']} for user {info['user']} "
                    f"is {info['status']} via vehicle {info['vehicle']} "
                    f"for company {info['company']}.")

    # --- Semantic search fallback with similarity threshold ---
    if index is not None:
        q_emb = np.array([emb_model.encode(query_clean)], dtype='float32')
        D, I = index.search(q_emb, k=1)
        distance = D[0][0]  # smaller is better
        threshold = 0.5  # adjust depending on embeddings
        if distance < threshold:
            closest = deliveries[I[0][0]]
            info = get_human_readable_info(closest)
            return (f"Closest match found: Delivery {info['package_id']} for user {info['user']} "
                    f"is {info['status']} via vehicle {info['vehicle']} "
                    f"for company {info['company']}.")
        else:
            return "Package not found in records. Please check the package ID."

    return "Package not found in records. Please check the package ID."
