"""
seed.py - Idempotent sample data seeder for Student Management System.
Populates 36 realistic student records across multiple departments and semesters,
ensuring all grade tiers (A, B, C, D, F) are well represented for analytics demonstration.
Safe to rerun: Uses upsert on 'roll_no'.
"""

from datetime import datetime, timezone, timedelta
from database import get_db, init_database

SAMPLE_STUDENTS = [
    # --- Grade A Students (Avg >= 80) ---
    {
        "roll_no": "CSE2024001",
        "name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "department": "CSE",
        "semester": 6,
        "marks": {"DBMS": 92, "DSA": 96, "Python": 94},  # Avg: 94.0 -> A
    },
    {
        "roll_no": "IT2024002",
        "name": "Priya Patel",
        "email": "priya.patel@example.com",
        "department": "IT",
        "semester": 4,
        "marks": {"DBMS": 88, "DSA": 84, "Python": 90},  # Avg: 87.33 -> A
    },
    {
        "roll_no": "AIDS2024003",
        "name": "Rohan Verma",
        "email": "rohan.verma@example.com",
        "department": "AI&DS",
        "semester": 2,
        "marks": {"DBMS": 82, "DSA": 86, "Python": 87},  # Avg: 85.0 -> A
    },
    {
        "roll_no": "ECE2024004",
        "name": "Sneha Reddy",
        "email": "sneha.reddy@example.com",
        "department": "ECE",
        "semester": 5,
        "marks": {"DBMS": 80, "DSA": 85, "Python": 81},  # Avg: 82.0 -> A
    },

    # --- Grade B Students (70 <= Avg < 80) ---
    {
        "roll_no": "CSE2024005",
        "name": "Aditya Singh",
        "email": "aditya.singh@example.com",
        "department": "CSE",
        "semester": 6,
        "marks": {"DBMS": 76, "DSA": 78, "Python": 80},  # Avg: 78.0 -> B
    },
    {
        "roll_no": "MECH2024006",
        "name": "Vikram Malhotra",
        "email": "vikram.malhotra@example.com",
        "department": "MECH",
        "semester": 7,
        "marks": {"DBMS": 72, "DSA": 75, "Python": 78},  # Avg: 75.0 -> B
    },
    {
        "roll_no": "CIVIL2024007",
        "name": "Ananya Iyer",
        "email": "ananya.iyer@example.com",
        "department": "CIVIL",
        "semester": 3,
        "marks": {"DBMS": 70, "DSA": 74, "Python": 72},  # Avg: 72.0 -> B
    },

    # --- Grade C Students (60 <= Avg < 70) ---
    {
        "roll_no": "ECE2024008",
        "name": "Karan Nair",
        "email": "karan.nair@example.com",
        "department": "ECE",
        "semester": 5,
        "marks": {"DBMS": 68, "DSA": 65, "Python": 71},  # Avg: 68.0 -> C
    },
    {
        "roll_no": "IT2024009",
        "name": "Meera Joshi",
        "email": "meera.joshi@example.com",
        "department": "IT",
        "semester": 4,
        "marks": {"DBMS": 64, "DSA": 66, "Python": 62},  # Avg: 64.0 -> C
    },
    {
        "roll_no": "AIDS2024010",
        "name": "Kabir Das",
        "email": "kabir.das@example.com",
        "department": "AI&DS",
        "semester": 2,
        "marks": {"DBMS": 62, "DSA": 60, "Python": 64},  # Avg: 62.0 -> C
    },

    # --- Grade D Students (40 <= Avg < 60) ---
    {
        "roll_no": "CSE2024011",
        "name": "Tanvi Deshmukh",
        "email": "tanvi.deshmukh@example.com",
        "department": "CSE",
        "semester": 8,
        "marks": {"DBMS": 55, "DSA": 58, "Python": 61},  # Avg: 58.0 -> D
    },
    {
        "roll_no": "MECH2024012",
        "name": "Harshvardhan Rao",
        "email": "harsh.rao@example.com",
        "department": "MECH",
        "semester": 7,
        "marks": {"DBMS": 50, "DSA": 52, "Python": 48},  # Avg: 50.0 -> D
    },
    {
        "roll_no": "CIVIL2024013",
        "name": "Diya Sen",
        "email": "diya.sen@example.com",
        "department": "CIVIL",
        "semester": 3,
        "marks": {"DBMS": 44, "DSA": 46, "Python": 42},  # Avg: 44.0 -> D
    },

    # --- Grade F Students (Avg < 40) ---
    {
        "roll_no": "ECE2024014",
        "name": "Arjun Kapoor",
        "email": "arjun.kapoor@example.com",
        "department": "ECE",
        "semester": 1,
        "marks": {"DBMS": 35, "DSA": 38, "Python": 32},  # Avg: 35.0 -> F
    },
    {
        "roll_no": "IT2024015",
        "name": "Riya Choudhury",
        "email": "riya.choudhury@example.com",
        "department": "IT",
        "semester": 1,
        "marks": {"DBMS": 28, "DSA": 32, "Python": 30},  # Avg: 30.0 -> F
    },
    {
        "roll_no": "CSE2024016",
        "name": "Rahul Kumar",
        "email": "rahul.kumar@example.com",
        "department": "CSE",
        "semester": 5,
        "marks": {"DBMS": 85, "DSA": 90, "Python": 88},  # Avg: 87.67 -> A
    },

    # --- Additional sample students for a fuller directory and analytics view ---
    {
        "roll_no": "CSE2024017",
        "name": "Ishita Mehta",
        "email": "ishita.mehta@example.com",
        "department": "CSE",
        "semester": 2,
        "marks": {"DBMS": 91, "DSA": 89, "Python": 93},  # Avg: 91.0 -> A
    },
    {
        "roll_no": "IT2024018",
        "name": "Yash Agarwal",
        "email": "yash.agarwal@example.com",
        "department": "IT",
        "semester": 8,
        "marks": {"DBMS": 86, "DSA": 88, "Python": 84},  # Avg: 86.0 -> A
    },
    {
        "roll_no": "AIDS2024019",
        "name": "Nandini Rao",
        "email": "nandini.rao@example.com",
        "department": "AI&DS",
        "semester": 6,
        "marks": {"DBMS": 81, "DSA": 83, "Python": 85},  # Avg: 83.0 -> A
    },
    {
        "roll_no": "ECE2024020",
        "name": "Devansh Gupta",
        "email": "devansh.gupta@example.com",
        "department": "ECE",
        "semester": 3,
        "marks": {"DBMS": 78, "DSA": 76, "Python": 79},  # Avg: 77.67 -> B
    },
    {
        "roll_no": "MECH2024021",
        "name": "Pooja Kulkarni",
        "email": "pooja.kulkarni@example.com",
        "department": "MECH",
        "semester": 4,
        "marks": {"DBMS": 74, "DSA": 77, "Python": 73},  # Avg: 74.67 -> B
    },
    {
        "roll_no": "CIVIL2024022",
        "name": "Manav Bansal",
        "email": "manav.bansal@example.com",
        "department": "CIVIL",
        "semester": 8,
        "marks": {"DBMS": 71, "DSA": 75, "Python": 70},  # Avg: 72.0 -> B
    },
    {
        "roll_no": "CSE2024023",
        "name": "Simran Kaur",
        "email": "simran.kaur@example.com",
        "department": "CSE",
        "semester": 7,
        "marks": {"DBMS": 69, "DSA": 67, "Python": 70},  # Avg: 68.67 -> C
    },
    {
        "roll_no": "IT2024024",
        "name": "Nikhil Sethi",
        "email": "nikhil.sethi@example.com",
        "department": "IT",
        "semester": 5,
        "marks": {"DBMS": 65, "DSA": 68, "Python": 66},  # Avg: 66.33 -> C
    },
    {
        "roll_no": "AIDS2024025",
        "name": "Ayesha Khan",
        "email": "ayesha.khan@example.com",
        "department": "AI&DS",
        "semester": 4,
        "marks": {"DBMS": 61, "DSA": 64, "Python": 63},  # Avg: 62.67 -> C
    },
    {
        "roll_no": "ECE2024026",
        "name": "Varun Menon",
        "email": "varun.menon@example.com",
        "department": "ECE",
        "semester": 6,
        "marks": {"DBMS": 58, "DSA": 55, "Python": 59},  # Avg: 57.33 -> D
    },
    {
        "roll_no": "MECH2024027",
        "name": "Ritika Sharma",
        "email": "ritika.sharma@example.com",
        "department": "MECH",
        "semester": 2,
        "marks": {"DBMS": 52, "DSA": 56, "Python": 54},  # Avg: 54.0 -> D
    },
    {
        "roll_no": "CIVIL2024028",
        "name": "Saurabh Jain",
        "email": "saurabh.jain@example.com",
        "department": "CIVIL",
        "semester": 7,
        "marks": {"DBMS": 47, "DSA": 49, "Python": 45},  # Avg: 47.0 -> D
    },
    {
        "roll_no": "CSE2024029",
        "name": "Neha Kapoor",
        "email": "neha.kapoor@example.com",
        "department": "CSE",
        "semester": 1,
        "marks": {"DBMS": 39, "DSA": 36, "Python": 38},  # Avg: 37.67 -> F
    },
    {
        "roll_no": "IT2024030",
        "name": "Aman Thakur",
        "email": "aman.thakur@example.com",
        "department": "IT",
        "semester": 3,
        "marks": {"DBMS": 31, "DSA": 35, "Python": 33},  # Avg: 33.0 -> F
    },
    {
        "roll_no": "AIDS2024031",
        "name": "Kritika Saini",
        "email": "kritika.saini@example.com",
        "department": "AI&DS",
        "semester": 1,
        "marks": {"DBMS": 27, "DSA": 30, "Python": 29},  # Avg: 28.67 -> F
    },
    {
        "roll_no": "ECE2024032",
        "name": "Mohit Yadav",
        "email": "mohit.yadav@example.com",
        "department": "ECE",
        "semester": 8,
        "marks": {"DBMS": 83, "DSA": 80, "Python": 86},  # Avg: 83.0 -> A
    },
    {
        "roll_no": "MECH2024033",
        "name": "Anjali Nair",
        "email": "anjali.nair@example.com",
        "department": "MECH",
        "semester": 5,
        "marks": {"DBMS": 79, "DSA": 81, "Python": 77},  # Avg: 79.0 -> B
    },
    {
        "roll_no": "CIVIL2024034",
        "name": "Raghav Mishra",
        "email": "raghav.mishra@example.com",
        "department": "CIVIL",
        "semester": 4,
        "marks": {"DBMS": 63, "DSA": 60, "Python": 65},  # Avg: 62.67 -> C
    },
    {
        "roll_no": "CSE2024035",
        "name": "Kavya Reddy",
        "email": "kavya.reddy@example.com",
        "department": "CSE",
        "semester": 3,
        "marks": {"DBMS": 57, "DSA": 60, "Python": 58},  # Avg: 58.33 -> D
    },
    {
        "roll_no": "IT2024036",
        "name": "Siddharth Roy",
        "email": "siddharth.roy@example.com",
        "department": "IT",
        "semester": 7,
        "marks": {"DBMS": 42, "DSA": 45, "Python": 41},  # Avg: 42.67 -> D
    }
]


def seed_database(db=None):
    """
    Inserts sample students using upsert to avoid duplicate key errors.
    """
    if db is None:
        db = get_db()

    init_database(db)
    students_col = db["students"]

    base_time = datetime.now(timezone.utc)
    upserted_count = 0

    print(f"[*] Seeding {len(SAMPLE_STUDENTS)} students into database '{db.name}'...")

    for idx, student in enumerate(SAMPLE_STUDENTS):
        # Stagger created_at so sorting by creation date shows chronological variation
        student_data = dict(student)
        student_data["created_at"] = base_time - timedelta(minutes=15 * (len(SAMPLE_STUDENTS) - idx))

        result = students_col.update_one(
            {"roll_no": student_data["roll_no"]},
            {"$set": student_data},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            upserted_count += 1

    total_records = students_col.count_documents({})
    print(f"[OK] Seeding completed. Collection 'students' now contains {total_records} documents.")
    return total_records


if __name__ == "__main__":
    seed_database()
