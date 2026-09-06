import csv
import os
from datetime import datetime

attendance_file = "attendance.csv"
dataset_path = "dataset"

today = datetime.now().strftime("%Y-%m-%d")

# Total registered students
total_students = 0

for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)

    if os.path.isdir(folder_path):
        total_students += 1


# Read today's attendance
present_students = set()

with open(attendance_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    print("\n========== ATTENDANCE REPORT ==========\n")

    print(
        f"{'Roll No':<10}"
        f"{'Name':<15}"
        f"{'Date':<15}"
        f"{'Time':<12}"
        f"{'Status'}"
    )

    print("-" * 65)

    for row in reader:

        print(
            f"{row['Roll No']:<10}"
            f"{row['Name']:<15}"
            f"{row['Date']:<15}"
            f"{row['Time']:<12}"
            f"{row['Status']}"
        )

        if row["Date"] == today and row["Status"] == "Present":
            present_students.add(row["Roll No"])


# Calculate summary
present_count = len(present_students)
absent_count = total_students - present_count

if total_students > 0:
    percentage = (present_count / total_students) * 100
else:
    percentage = 0


print("\n========== ATTENDANCE SUMMARY ==========")

print(f"Total Students : {total_students}")
print(f"Present        : {present_count}")
print(f"Absent         : {absent_count}")
print(f"Attendance     : {percentage:.2f}%")

print("========================================")