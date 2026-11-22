# ==========================================
# STUDENT PERFORMANCE ANALYSIS PROJECT
# ==========================================

# 1. Import Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return df.to_html()

# 2. Load Dataset

file_path = Path(__file__).with_name("students.csv")

df = pd.read_csv(file_path)

print("\n========== STUDENT DATASET ==========")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nColumn Names:")
print(df.columns.tolist())


# 3. Clean Column Names

df.rename(
    columns={"student_name": "name"},
    inplace=True
)

# Expected columns:
# name, gender, subject, attendance, marks

required_columns = [
    "name", "gender", "subject",
    "attendance", "marks"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Missing column: {column}. "
            "Please check your CSV column names."
        )


# 4. Handle Missing Values

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# Fill categorical missing values
for column in ["name", "gender", "subject"]:
    if df[column].isnull().any():
        df[column] = df[column].fillna(
            df[column].mode()[0]
        )

# Convert numeric columns
df["attendance"] = pd.to_numeric(
    df["attendance"], errors="coerce"
)

df["marks"] = pd.to_numeric(
    df["marks"], errors="coerce"
)

# Fill numeric missing values with median
for column in ["attendance", "marks"]:
    if df[column].isnull().any():
        df[column] = df[column].fillna(
            df[column].median()
        )

print("\nMissing values handled successfully!")


# 5. Remove Duplicate Records

print("\nDuplicate Records:")
print(df.duplicated().sum())

df = df.drop_duplicates()

print("Duplicate records removed!")


# 6. Calculate Average Marks

average_marks = df["marks"].mean()

print("\n========== STUDENT PERFORMANCE ==========")

print("Average Marks:", average_marks)


# 7. Highest Scoring Student

highest_student = df.loc[df["marks"].idxmax()]

print("\nHighest Scoring Student:")
print(highest_student)


# 8. Lowest Scoring Student

lowest_student = df.loc[df["marks"].idxmin()]

print("\nLowest Scoring Student:")
print(lowest_student)


# 9. Subject-wise Average Marks

subject_avg = df.groupby("subject")["marks"].mean()

print("\nSubject-wise Average Marks:")
print(subject_avg)


# 10. Students Scoring Above 75%

above_75 = df[df["marks"] > 75]

print("\nStudents Scoring Above 75%:")
print(above_75[["name", "marks"]])

print("Total Students Above 75%:", len(above_75))


# 11. NumPy Statistical Calculations

marks = df["marks"].to_numpy()

print("\n========== NUMPY STATISTICS ==========")

print("Mean:", np.mean(marks))

print("Median:", np.median(marks))

print("Standard Deviation:", np.std(marks))


# 12. Visualization 1: Bar Chart

plt.figure(figsize=(8, 5))

subject_avg.plot(kind="bar")

plt.title("Subject-wise Average Marks")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")

plt.tight_layout()

plt.savefig(
    Path(__file__).with_name("subject_average.png")
)

plt.show()
plt.close()


# 13. Visualization 2: Histogram

plt.figure(figsize=(8, 5))

plt.hist(df["marks"], bins=5, edgecolor="black")

plt.title("Distribution of Student Marks")
plt.xlabel("Marks")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig(
    Path(__file__).with_name("marks_histogram.png")
)

plt.show()
plt.close()


# 14. Visualization 3: Scatter Plot

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="attendance",
    y="marks"
)

plt.title("Attendance vs Marks")
plt.xlabel("Attendance (%)")
plt.ylabel("Marks")

plt.tight_layout()

plt.savefig(
    Path(__file__).with_name("attendance_marks.png")
)

plt.show()
plt.close()


# 15. Connect to SQLite Database

database_path = Path(__file__).with_name("students.db")

conn = sqlite3.connect(database_path)

# Store cleaned dataset in database
df.to_sql(
    "students",
    conn,
    if_exists="replace",
    index=False
)

print("\nDatabase Connected Successfully!")


# 16. SQL Query 1: Top 5 Students

query1 = """
SELECT name, marks
FROM students
ORDER BY marks DESC
LIMIT 5;
"""

result1 = pd.read_sql_query(query1, conn)

print("\n========== TOP 5 STUDENTS ==========")
print(result1)


# 17. SQL Query 2: Subject-wise Average

query2 = """
SELECT subject, AVG(marks) AS average_marks
FROM students
GROUP BY subject;
"""

result2 = pd.read_sql_query(query2, conn)

print("\n========== SUBJECT-WISE AVERAGE ==========")
print(result2)


# 18. SQL Query 3: Attendance Below 75%

query3 = """
SELECT name, attendance
FROM students
WHERE attendance < 75;
"""

result3 = pd.read_sql_query(query3, conn)

print("\n========== LOW ATTENDANCE STUDENTS ==========")
print(result3)


# 19. Close Database Connection

conn.close()

print("\nDatabase Connection Closed!")


# 20. Project Completed

print("\n====================================")
print("STUDENT PERFORMANCE ANALYSIS")
print("PROJECT COMPLETED SUCCESSFULLY!")
print("====================================")
