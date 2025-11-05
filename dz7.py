import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    curator TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    age INTEGER,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES Groups(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER CHECK(grade >= 1 AND grade <= 10),
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id)
)
""")

conn.commit()
conn.close()

class Group:
    def __init__(self, name, curator):
        self.name = name
        self.curator = curator

    def save(self):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Groups (name, curator) VALUES (?, ?)", (self.name, self.curator))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Groups")
        data = cursor.fetchall()
        conn.close()
        return data


class Student:
    def __init__(self, full_name, age, group_id):
        self.full_name = full_name
        self.age = age
        self.group_id = group_id

    def save(self):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (full_name, age, group_id) VALUES (?, ?, ?)",
                       (self.full_name, self.age, self.group_id))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")
        data = cursor.fetchall()
        conn.close()
        return data


class Subject:
    def __init__(self, title):
        self.title = title

    def save(self):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Subjects (title) VALUES (?)", (self.title,))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Subjects")
        data = cursor.fetchall()
        conn.close()
        return data


class Grade:
    def __init__(self, student_id, subject_id, grade):
        self.student_id = student_id
        self.subject_id = subject_id
        self.grade = grade

    def save(self):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
                       (self.student_id, self.subject_id, self.grade))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Grades")
        data = cursor.fetchall()
        conn.close()
        return data


conn = sqlite3.connect("university.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM Groups")
cursor.execute("DELETE FROM Students")
cursor.execute("DELETE FROM Subjects")
cursor.execute("DELETE FROM Grades")
conn.commit()
conn.close()

g1 = Group("Backend-2", "Islam")
g1.save()

st1 = Student("Islam", 20, 1)
st2 = Student("Bob", 21, 1)
st1.save()
st2.save()

subj1 = Subject("Python")
subj2 = Subject("Databases")
subj1.save()
subj2.save()

gr1 = Grade(1, 1, 5)
gr2 = Grade(1, 2, 2)
gr3 = Grade(2, 1, 3)
gr4 = Grade(2, 2, 4)
gr1.save()
gr2.save()
gr3.save()
gr4.save()

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

print("Средняя оценка каждого студента:")
cursor.execute("""
SELECT s.full_name, AVG(g.grade) as avg_grade
FROM Students s
JOIN Grades g ON s.id = g.student_id
GROUP BY s.id
""")
for row in cursor.fetchall():
    print(row)

print("Средняя оценка по каждому предмету:")
cursor.execute("""
SELECT sub.title, AVG(g.grade) as avg_grade
FROM Subjects sub
JOIN Grades g ON sub.id = g.subject_id
GROUP BY sub.id
""")
for row in cursor.fetchall():
    print(row)

print("Студенты с оценкой выше средней по группе:")
cursor.execute("""
SELECT s.full_name, AVG(g.grade) as avg_grade
FROM Students s
JOIN Grades g ON s.id = g.student_id
GROUP BY s.id
HAVING avg_grade > (
    SELECT AVG(g2.grade)
    FROM Students s2
    JOIN Grades g2 ON s2.id = g2.student_id
    WHERE s2.group_id = s.group_id
)
""")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
CREATE VIEW IF NOT EXISTS ExcellentStudents AS
SELECT s.full_name, AVG(g.grade) AS avg_grade
FROM Students s
JOIN Grades g ON s.id = g.student_id
GROUP BY s.id
HAVING avg_grade >= 8
""")

print("ExcellentStudents (средняя оценка ≥ 8):")
cursor.execute("SELECT * FROM ExcellentStudents")
for row in cursor.fetchall():
    print(row)

conn.close()
