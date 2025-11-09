# train_chatbot.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# -------------------------------
# 1️⃣ Check if dataset exists
# -------------------------------
if not os.path.exists('dataset.csv'):
    print("❌ dataset.csv not found! Please make sure it exists in this folder.")
    exit()

# -------------------------------
# 2️⃣ Load dataset
# -------------------------------
data = pd.read_csv('dataset.csv')

# Validate required columns
if 'Question' not in data.columns or 'Answer' not in data.columns:
    print("❌ dataset.csv must contain 'Question' and 'Answer' columns!")
    exit()

# -------------------------------
# 3️⃣ Prepare features and labels
# -------------------------------
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['Question'])
y = data['Answer']

# -------------------------------
# 4️⃣ Train the model
# -------------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# -------------------------------
# 5️⃣ Save model and vectorizer
# -------------------------------
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

print("✅ Model trained and saved successfully!")
print("Files saved as: model.pkl and vectorizer.pkl")
