#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM flocks')
flocks = cursor.fetchall()

print("=== Flocks in Database ===")
for flock in flocks:
    print(f"ID: {flock[0]}, Name: {flock[1]}, Initial Size: {flock[2]}, Age: {flock[3]}, Mortality: {flock[4]}, Feed: {flock[5]}")

conn.close()
