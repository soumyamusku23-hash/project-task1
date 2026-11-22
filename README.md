# Student Performance Analysis

A beginner-friendly Python project that loads student records from a CSV, handles incomplete values, summarizes marks and attendance, and displays the results in a Flask dashboard. The included sample data lets you run it before adding your own dataset.

> **Project type:** descriptive data analysis. This project does not train a predictive model, so a train/test split is not appropriate. If you later build a model to predict outcomes, split data by student to avoid records for the same student appearing in both sets.

## Dashboard preview

Run the app using the steps below to see the dashboard and its live charts:

- **Subject averages:** bar chart of average marks for each subject.
- **Marks distribution:** histogram of marks across subject records.
- **Attendance vs marks:** scatter plot with one point per subject record.

The dashboard also shows mean, median, standard deviation, highest and lowest marks, counts above 70% and below 70% attendance, and the five students with the highest average marks.

## What this project does

1. Loads `data/students.csv` with Pandas.
2. Normalizes common column-name variations such as `Name`, `Student Name`, `Score`, and `Attendance Percentage`.
3. Checks for required fields and handles missing names, subjects, marks, and attendance. Missing numeric values are replaced with that column's median; if the whole column is missing or invalid, the fallback is 0. Marks and attendance are limited to the 0–100 range.
4. Uses NumPy to calculate mean, median, population standard deviation (`ddof=0`), highest, and lowest marks.
5. Uses Pandas to group rows by subject and student. A student's top-five ranking is based on their average marks across their subject records.
6. Creates the three charts with Matplotlib and Seaborn.
7. Serves the dashboard with Flask and the page template in `templates/index.html`.

Cleaning assumptions matter: a value below 0 or above 100 is clipped to the nearest valid boundary. Review the source data before using this analysis for decisions. The missing-cell count shown in the dashboard counts blank CSV cells before cleaning; nonnumeric text in numeric columns is also treated as missing for calculation purposes.

## Project structure

```text
student-performance-analysis/
├── app.py                    # Flask web application
├── main.py                   # Data loading, cleaning, statistics, charts
├── requirements.txt          # Python dependencies
├── Procfile                  # Render start command
├── render.yaml               # Optional Render Blueprint configuration
├── data/
│   └── students.csv          # Sample dataset; replace with your class data
├── templates/
│   └── index.html            # Dashboard structure and dynamic data
└── static/
    └── style.css             # Responsive dashboard styling
```

### How the parts work together

```text
data/students.csv
       ↓
main.py: load → clean → summarize → make charts
       ↓
app.py: Flask route passes the report to the template
       ↓
templates/index.html + static/style.css
       ↓
Browser dashboard
```

The backend is the Python code that reads and processes the CSV and prepares chart images. The frontend is the HTML template and CSS that display those results in a browser.

## Dataset format

The sample CSV uses one row per student and subject. Use these columns (case and spaces are flexible):

| Column | Example | Notes |
|---|---|---|
| `student_name` | `Aarav` | Required; common alternatives include `name` and `student` |
| `gender` | `F` | Optional; displayed data analysis does not depend on it |
| `subject` | `Mathematics` | Required; common alternative: `course` |
| `attendance` | `95` | Required, percentage from 0 to 100 |
| `marks` | `88` | Required, percentage/score from 0 to 100 |

Example:

```csv
student_name,gender,subject,attendance,marks
Aarav,M,Mathematics,95,88
Aarav,M,Science,92,91
Diya,F,Mathematics,88,78
```

If your CSV uses a different filename or location, update `DEFAULT_DATASET` in `main.py`. If your headers use a new name, add that alias to `ALIASES` in the same file.

## Run locally in PyCharm

1. Download and extract the ZIP, then open the `student-performance-analysis` folder in PyCharm.
2. Use Python 3.10 or newer. Create/select a virtual environment when PyCharm prompts you.
3. Open the PyCharm terminal in the project folder and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the web dashboard:

   ```bash
   python app.py
   ```

5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

To print a text summary and rankings in the terminal instead, run `python main.py`. The web page reads the sample CSV on each page load, so replacing the CSV updates the dashboard after refresh.

## SQL examples

These queries use a table named `student_scores` with columns `student_name`, `subject`, `attendance`, and `marks`. Load your CSV into a database table with matching columns before running them. SQL syntax varies slightly by database; these examples use widely supported syntax.

### 1. Top five students by average marks

```sql
SELECT student_name, AVG(marks) AS average_marks
FROM student_scores
GROUP BY student_name
ORDER BY average_marks DESC
LIMIT 5;
```

### 2. Average marks for every student

```sql
SELECT student_name, AVG(marks) AS average_marks
FROM student_scores
GROUP BY student_name
ORDER BY student_name;
```

### 3. Students with attendance below 70%

```sql
SELECT DISTINCT student_name
FROM student_scores
WHERE attendance < 70
ORDER BY student_name;
```

The app counts subject records below 70% attendance. The SQL query returns each student once if any of their subject records is below 70%.

## Publish on GitHub

1. Create a new repository on GitHub.
2. In PyCharm, open the terminal at the project root and initialize Git if needed: `git init`.
3. Add the project files, commit them, and connect/push to your GitHub repository using the URL GitHub provides.
4. Keep private student data out of a public repository. Replace the sample data with anonymized or synthetic records before publishing.

**GitHub repository:** `[Add your GitHub repository link here]`  
**LinkedIn profile:** `[Add your LinkedIn profile link here]`  
**Live Render app:** `[Add your Render URL here after deployment]`

These are placeholders, not real profile or project links. Replace them with your own URLs when available.

## Deploy on Render

1. Push the project to GitHub.
2. Sign in to Render and create a **New Web Service**, then connect the repository.
3. Select the project repository and set:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
4. Choose the free or paid instance that suits your needs and create the service.
5. When the deploy finishes, open the Render-provided URL. Render will use the included `Procfile`; `render.yaml` is also available for Blueprint deployment.

The included `render.yaml` defines the same build and start commands. For a small teaching project, local CSV storage is sufficient. On hosted services, changes made to the file system may not persist across deployments, so treat the bundled CSV as read-only sample data or connect a persistent database if users need to edit records online.

## Tools used

- **Python** for the analysis logic
- **Pandas** for CSV loading, cleanup, and grouping
- **NumPy** for numerical statistics
- **Matplotlib and Seaborn** for charts
- **Flask** for the web server and routes
- **HTML and CSS** for the dashboard
- **Gunicorn and Render** for deployment

## Learning notes

- This is an analysis project, not a machine-learning model. “Train the data” is not a step in this version because it does not predict a label or future result.
- Attendance/marks scatter plots can show association, but do not prove that attendance caused a mark to change.
- The sample dataset is fictional and included only to demonstrate the workflow.

## Profile and project links

Add links after creating or deploying your project:

- GitHub: `https://github.com/YOUR_USERNAME/student-performance-analysis`
- LinkedIn: `https://www.linkedin.com/in/YOUR_PROFILE/`
- Render: `https://YOUR-SERVICE-NAME.onrender.com`

Replace every example URL above with your actual profile and deployment URLs.
