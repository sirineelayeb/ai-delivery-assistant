AI Delivery Assistant

An AI-powered delivery tracking assistant using Python, MongoDB, MiniLM embeddings, and FAISS for semantic search.

🚀 Features

**Track deliveries by package ID
** Semantic search using MiniLM + FAISS
**Natural language answers
**MongoDB integration (Deliveries, Users, Vehicles, Companies)

📦 Requirements

**Python 3.9+

**Install packages:
    pip install pymongo python-dotenv sentence-transformers faiss-cpu

🔧 Environment Variables

**Create a .env file:
    MONGO_USER=your_mongo_user
    MONGO_PASSWORD=your_mongo_password
    MONGO_CLUSTER=delivery-tracker.le6ss7w.mongodb.net
    MONGO_DB=test

▶️ Running the Project

**python main.py
=> You should see: 
        MongoDB connected successfully!
        Loaded X deliveries from database.

💡 Usage Example

from search_engine import search
result = search("Where is package 69230713c60f09cd1d66fb48?")
print(result)

**Sample Output:
Delivery 69230713c60f09cd1d66fb48 for user Ahmed Azlouk
is in-progress via vehicle Toyota Van (ABC-124)
for company ARAMEX.

📌 Future Enhancements
**FastAPI REST API
**GPS real-time updates
**IoT/MQTT integration
**React + Tailwind dashboard