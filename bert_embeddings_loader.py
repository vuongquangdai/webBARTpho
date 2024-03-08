import torch
from transformers import AutoModel, AutoTokenizer
import mysql.connector
import numpy as np

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nln"
)
cursor = db.cursor()
cursor.execute("SELECT * FROM `data`;")
data = cursor.fetchall()

bert_embeddings = None
tokenizer = AutoTokenizer.from_pretrained("vinai/bartpho-word")
model = AutoModel.from_pretrained("vinai/bartpho-word")

def load_data_and_build_bartpho_embeddings():
    global data, bert_embeddings
    bert_embeddings = []

    for row in data:
        text = row[11]
        tokens = tokenizer(text, return_tensors='pt')['input_ids']

        with torch.no_grad():
            outputs = model(tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy() 
        bert_embeddings.append(embeddings)

    # Lưu embeddings vào một tệp
    np.save('bert_embeddings.npy', bert_embeddings)

if __name__ == '__main__':
    load_data_and_build_bartpho_embeddings()