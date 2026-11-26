import sqlite3
con = sqlite3.connect("school.db")
con.executescript("""
DROP TABLE IF EXISTS enrollments; DROP TABLE IF EXISTS student_profiles;
DROP TABLE IF EXISTS students; DROP TABLE IF EXISTS courses; DROP TABLE IF EXISTS departments;
PRAGMA foreign_keys = ON;
CREATE TABLE departments (
  dept_id INTEGER PRIMARY KEY,
  name    TEXT NOT NULL UNIQUE);
CREATE TABLE students (
  student_id INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  email      TEXT UNIQUE,
  city       TEXT,
  dept_id    INTEGER REFERENCES departments(dept_id));
CREATE TABLE student_profiles (
  student_id INTEGER PRIMARY KEY REFERENCES students(student_id),
  phone TEXT, date_of_birth TEXT);
CREATE TABLE courses (
  course_id INTEGER PRIMARY KEY,
  title     TEXT NOT NULL,
  credits   INTEGER,
  dept_id   INTEGER REFERENCES departments(dept_id));
CREATE TABLE enrollments (
  student_id INTEGER REFERENCES students(student_id),
  course_id  INTEGER REFERENCES courses(course_id),
  marks      INTEGER,
  PRIMARY KEY (student_id, course_id));
INSERT INTO departments VALUES (1,'Computer Science'),(2,'Mathematics'),(3,'Physics');
INSERT INTO students VALUES
 (1,'Ayesha Khan','ayesha@uni.pk','Lahore',1),
 (2,'Bilal Ahmed','bilal@uni.pk','Karachi',1),
 (3,'Fatima Noor','fatima@uni.pk','Lahore',2),
 (4,'Hamza Ali','hamza@uni.pk','Islamabad',2),
 (5,'Sana Malik','sana@uni.pk','Lahore',1),
 (6,'Usman Tariq',NULL,'Karachi',NULL);
INSERT INTO student_profiles VALUES (1,'0300-1111111','2004-03-12'),(2,'0301-2222222','2003-11-02');
INSERT INTO courses VALUES (101,'Python Programming',3,1),(102,'Databases',3,1),(201,'Statistics',4,2),(301,'Mechanics',4,3);
INSERT INTO enrollments VALUES (1,101,88),(1,102,92),(2,101,75),(2,102,NULL),(3,201,81),(3,101,67),(4,201,58),(5,101,95),(5,102,84);
""")
con.commit(); con.close()
