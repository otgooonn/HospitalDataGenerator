from datetime import timedelta
import random
import csv
import argparse
from faker import Faker

fake = Faker()

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

DEPARTMENTS = [
    "Internal Medicine", "General Surgery", "Emergency Medicine", 
    "Pediatrics", "Obstetrics and Gynecology", "Neurology", 
    "Cardiology", "Pulmonology", "Orthopedic Surgery", 
    "Ophthalmology", "Otolaryngology", "Dermatology",
    "Urology", "Oncology", "Intensive Care Unit", "Psychiatry",
    "Gastroenterology", "Nephrology", "Rheumatology"
]

DIAGNOSES = [
    "Pneumonia", "Heart Failure", "Diabetes Mellitus", "Hypertension",
    "Peptic Ulcer", "Hepatitis", "Kidney Failure", "Stroke",
    "Cancer", "Bronchitis", "Arthritis", "Osteoporosis",
    "Depression", "Alcohol Poisoning", "Infectious Disease",
    "Back Pain", "Migraine", "Pancreatitis", "Gallstones", "Appendicitis"
]

INSURANCES = [
    "BlueCross", "Aetna", "Cigna", "UnitedHealth", "Humana",
    "Medicare", "Medicaid", "Kaiser"
]


def generate_doctor():
    return f"Dr. {fake.last_name()}"


def generate_row(patient_id: int):
    is_male = random.choice([True, False])
    first_name = fake.first_name_male() if is_male else fake.first_name_female()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=0, maximum_age=95)
    admission = fake.date_between(start_date="-3y", end_date="today")
    stay_days = random.randint(1, 21)
    discharge = admission + timedelta(days=stay_days)
    
    age = admission.year - dob.year
    if (admission.month, admission.day) < (dob.month, dob.day):
        age -= 1
    if age < 0:
        age = 0

    return [
        patient_id,
        first_name,
        last_name,
        "Male" if is_male else "Female",
        dob.isoformat(),
        age,
        random.choice(BLOOD_GROUPS),
        fake.email(),
        fake.city(),
        admission.isoformat(),
        discharge.isoformat(),
        stay_days,
        random.choice(DEPARTMENTS),
        generate_doctor(),
        random.choice(DIAGNOSES),
        random.randint(100, 599),
        random.choice(INSURANCES),
        random.randint(500, 50000)
    ]


def generate_csv(filename="hospital_data.csv", rows=1000):
    headers = [
        "ID", "First Name", "Last Name", "Gender", "Date of Birth", "Age",
        "Blood Type", "Email", "City",
        "Admission Date", "Discharge Date", "Length of Stay",
        "Department", "Doctor", "Diagnosis",
        "Room", "Insurance", "Bill"
    ]

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(1, rows + 1):
            writer.writerow(generate_row(i))

            if i % 10000 == 0:
                print(f"{i} rows generated...")

    print(f"DONE → {filename} ({rows} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1000)
    parser.add_argument("--file", type=str, default="hospital_data.csv")
    args = parser.parse_args()
    generate_csv(filename=args.file, rows=args.rows)