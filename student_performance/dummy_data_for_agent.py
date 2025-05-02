import pandas as pd
import scipy

# Load Dummy Data
df = pd.read_csv("data3.csv")

streams = list(df["Stream"].unique())
student_names = list(df["Student Name"].unique())
subject_categories = list(df["Subject Category"].unique())
subjects = list(df["Subject"].unique())
subject_strands = list(df["Subject Strand"].unique())
terms = list(df["Term"].unique())
grades = list(df["Grade"].unique())


subject_strand_to_subject = {
    "English Reading": "English",
    "English Writing": "English",
    "Vocabulary": "Spanish",
    "Spanish Grammar": "Spanish",
    "Algebra": "Math",
    "Geometry": "Math",
    "Mechanics": "Physics",
    "Thermodynamics": "Physics",
    "Physical Geography": "Geography",
    "Human Geography": "Geography",
    "Ancient History": "History",
    "Medieval History": "History",
}


all_grades = sorted(df["Grade"].unique())

student_subject_dfs = []

for student_name in df["Student Name"].unique():
    student_df = df[df["Student Name"] == student_name]

    for subject in df["Subject"].unique():
        subject_df = student_df[student_df["Subject"] == subject]
        if subject_df.empty:
            continue

        grade_counts = subject_df["Grade"].value_counts(normalize=True).round(2)

        row = {
            grade: f"{grade_counts[grade]:.2f}" if grade in grade_counts else "-"
            for grade in all_grades
        }
        row["Student Name"] = student_name
        row["Subject"] = subject

        student_subject_dfs.append(row)


subject_grade_prob_df = pd.DataFrame(student_subject_dfs)
subject_grade_prob_df = subject_grade_prob_df[["Student Name", "Subject"] + all_grades]
subject_grade_prob_df_for_specific_student = subject_grade_prob_df[
    subject_grade_prob_df["Student Name"] == student_names[0]
]
subject_grade_prob_df_for_specific_student


all_grades = sorted(df["Grade"].unique())


student_strand_dfs = []


for student_name in df["Student Name"].unique():
    student_df = df[df["Student Name"] == student_name]

    for strand in df["Subject Strand"].unique():
        strand_df = student_df[student_df["Subject Strand"] == strand]
        if strand_df.empty:
            continue

        grade_counts = strand_df["Grade"].value_counts(normalize=True).round(2)

        row = {
            grade: f"{grade_counts[grade]:.2f}" if grade in grade_counts else "-"
            for grade in all_grades
        }
        row["Student Name"] = student_name
        row["Subject Strand"] = strand

        student_strand_dfs.append(row)


strand_grade_prob_df = pd.DataFrame(student_strand_dfs)
strand_grade_prob_df = strand_grade_prob_df[
    ["Student Name", "Subject Strand"] + all_grades
]
strand_grade_prob_df_for_specific_student = strand_grade_prob_df[
    strand_grade_prob_df["Student Name"] == student_names[0]
]
strand_grade_prob_df_for_specific_student


# ## Percentile Data
#


data = []

for stream in streams:
    # Get specific stream
    stream_df = df[df["Stream"] == stream]

    # Get details of this stream
    student_names = list(stream_df["Student Name"].unique())
    subject_strands = list(stream_df["Subject Strand"].unique())

    # For each student look at how well they did in each subject
    for student_name in student_names:
        student_df = stream_df[stream_df["Student Name"] == student_name]

        for subject_strand in subject_strands:
            subject = subject_strand_to_subject[subject_strand]
            # Get Mean and Median for strean in specific strand

            stream_subject_strand_df = stream_df[
                stream_df["Subject Strand"] == subject_strand
            ]

            stream_subject_strand_mean = (
                stream_subject_strand_df["Grade Numeric"].mean().round(1)
            )

            # stream_subject_strand_median = stream_subject_strand_df[
            #     "Grade Numeric"
            # ].median()

            stream_subject_strand_std = stream_subject_strand_df["Grade Numeric"].std()

            # Get stream mean in a particular strand
            student_subject_strand_df = student_df[
                student_df["Subject Strand"] == subject_strand
            ]

            student_subject_strand_mean = (
                student_subject_strand_df["Grade Numeric"].mean().round(1)
            )

            # student_z_score = (
            #     (student_subject_strand_mean - stream_subject_strand_mean)
            #     / stream_subject_strand_std
            #     # if stream_subject_strand_std != 0
            #     # else 0
            # )

            student_percentile = scipy.stats.percentileofscore(
                stream_subject_strand_df["Grade Numeric"],
                student_subject_strand_mean,
            ).round(1)

            data.append(
                [
                    stream,
                    student_name,
                    subject,
                    subject_strand,
                    student_subject_strand_mean,
                    student_percentile,
                ]
            )


subject_strand_percentile_df = pd.DataFrame(
    data,
    columns=[
        "Stream",
        "Student Name",
        "Subject",
        "Subject Strand",
        "Grade Numeric",
        "Percentile",
    ],
)


subject_strand_percentile_for_specific_student_df = subject_strand_percentile_df[
    subject_strand_percentile_df["Student Name"] == student_names[0]
]
subject_strand_percentile_for_specific_student_df
