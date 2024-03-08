import mysql.connector
import pandas as pd
import numpy as np
import tensorflow as tf
import py_vncorenlp

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nln"
)
cursor = db.cursor()
global data

rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='F:/Nien_luan_nganh/NLN/VnCoreNLP-master/')

cursor.execute("SELECT * FROM `data`;")
data = cursor.fetchall()
for row in data:
    text = row[3] + '. ' + row[8] + '. ' + row[9] + '. ' + row[10]
    output = rdrsegmenter.word_segment(text)
    output_text = ' '.join(output).lower()
    
    update_query = "UPDATE `data` SET `segmented_text` = %s WHERE `data`.`id` = %s;"
    cursor.execute(update_query, (output_text, row[0]))
    db.commit()