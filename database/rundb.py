import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Connect to the attendance database
conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()

# Fetch all attendance records
cursor.execute("SELECT * FROM attendance")
records = cursor.fetchall()

# Print the records
if records:
    print("📋 Attendance Records:")
    for record in records:
        print(f"ID: {record[0]}, Name: {record[1]}, Date: {record[2]}, Time: {record[3]}")
else:
    print("⚠️ No attendance records found.")

conn.close()
