
CREATE DATABASE IF NOT EXISTS student_management;

USE student_management;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    course VARCHAR(100) NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample records for testing
INSERT INTO students (name, email, phone, course, marks)
VALUES
('Aarav Sharma', 'aarav@example.com',
 '9876543210', 'Python', 86.50),
('Priya Patil', 'priya@example.com',
 '9876501234', 'Web Development', 92.00);