import os
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "students.csv")
DB_PATH = os.path.join(BASE_DIR, "students.db")
CHART_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(CHART_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(CSV_PATH)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    df = df.drop_duplicates()
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
    df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")
    df = df.dropna(subset=["student_name", "subject", "marks", "attendance"])
    return df


def create_charts(df):
    # 1. Subject-wise average marks
    subject_avg = df.groupby("subject")["marks"].mean()
    plt.figure(figsize=(8, 5))
    subject_avg.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "subject_avg.png"))
    plt.close()

    # 2. Marks histogram
    plt.figure(figsize=(8, 5))
    plt.hist(df["marks"], bins=10, edgecolor="black")
    plt.title("Student Marks Distribution")
    plt.xlabel("Marks")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "marks_hist.png"))
    plt.close()

    # 3. Attendance vs marks scatter plot
    plt.figure(figsize=(8, 5))
    plt.scatter(df["attendance"], df["marks"])
    plt.title("Attendance vs Marks")
    plt.xlabel("Attendance")
    plt.ylabel("Marks")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "attendance_vs_marks.png"))
    plt.close()


@app.route("/")
def index():
    df = load_data()
    create_charts(df)

    # Save cleaned data into SQLite database
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("students", conn, if_exists="replace", index=False)

    # SQL Query 1: Top 5 students by marks
    top_students = pd.read_sql_query(
        "SELECT student_name, subject, marks, attendance FROM students ORDER BY marks DESC LIMIT 5",
        conn,
    ).to_dict("records")

    # SQL Query 2: Subject-wise average marks
    subject_average = pd.read_sql_query(
        "SELECT subject, AVG(marks) AS avg_marks FROM students GROUP BY subject",
        conn,
    ).to_dict("records")

    # SQL Query 3: Attendance below 75
    low_attendance = pd.read_sql_query(
        "SELECT student_name, subject, marks, attendance FROM students WHERE attendance < 75",
        conn,
    ).to_dict("records")

    conn.close()

    total_students = len(df)
    average_marks = round(df["marks"].mean(), 2)
    highest_marks = df["marks"].max()
    lowest_marks = df["marks"].min()
    above_75 = int((df["marks"] > 75).sum())

    lowest_idx = df["marks"].idxmin()
    highest_idx = df["marks"].idxmax()
    lowest_student = df.loc[lowest_idx, "student_name"]
    highest_student = df.loc[highest_idx, "student_name"]

    return render_template(
        "index.html",
        total_students=total_students,
        average_marks=average_marks,
        highest_marks=highest_marks,
        lowest_marks=lowest_marks,
        above_75=above_75,
        lowest_student=lowest_student,
        highest_student=highest_student,
        top_students=top_students,
        subject_average=subject_average,
        low_attendance=low_attendance,
    )


if __name__ == "__main__":
    app.run(debug=True)