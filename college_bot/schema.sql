-- Users table (Students)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    college_id VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Moderators table (Admins)
CREATE TABLE moderators (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    mod_id VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Schedule table
CREATE TABLE schedule (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course VARCHAR(100) NOT NULL,
    day VARCHAR(20) NOT NULL,
    time VARCHAR(20) NOT NULL,
    room VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurants table
CREATE TABLE restaurants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(100),
    address VARCHAR(255),
    rating FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hostels table
CREATE TABLE hostels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    capacity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gyms table
CREATE TABLE gyms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat logs table
CREATE TABLE chat_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Analytics table
CREATE TABLE analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    total_chats INT DEFAULT 0,
    top_queries TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_chat_logs_user ON chat_logs(user_id);
CREATE INDEX idx_chat_logs_date ON chat_logs(created_at);
CREATE INDEX idx_schedule_day ON schedule(day);

-- Insert sample data for testing (with properly hashed passwords)
-- Note: Run the Python script below to generate real password hashes
-- Password for student: student123
-- Password for moderator: admin123

INSERT INTO users (name, college_id, password_hash) VALUES
('Aarav Verma', '21CS105', 'scrypt:32768:8:1$aBcDeFgHiJkLmNoP$abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890'),
('Priya Singh', '21CS102', 'scrypt:32768:8:1$aBcDeFgHiJkLmNoP$abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890');

INSERT INTO moderators (name, mod_id, password_hash) VALUES
('Dr. Rajesh Gupta', 'MOD001', 'scrypt:32768:8:1$aBcDeFgHiJkLmNoP$abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890');

INSERT INTO schedule (course, day, time, room) VALUES
('Computer Networks', 'Monday', '10:00 AM', 'B-204'),
('Data Structures', 'Tuesday', '11:00 AM', 'A-301'),
('Database Systems', 'Wednesday', '2:00 PM', 'C-105'),
('Web Development', 'Thursday', '9:00 AM', 'Lab-2'),
('Mathematics-III', 'Friday', '1:00 PM', 'A-101');

INSERT INTO restaurants (name, cuisine, address, rating) VALUES
('Campus Cafe', 'North Indian', 'Gate 2, Campus', 4.5),
('Pizza Paradise', 'Italian', 'Hostel Block', 4.3),
('South Spice', 'South Indian', 'Market Road', 4.7),
('Burger Junction', 'Fast Food', 'Main Gate', 4.2);

INSERT INTO hostels (name, address, capacity) VALUES
('Boys Hostel A', 'Block A, Campus', 200),
('Girls Hostel B', 'Block B, Campus', 150),
('PG Hostel C', 'Block C, Campus', 100);

INSERT INTO gyms (name, address, features) VALUES
('Campus Fitness', 'Sports Complex', 'Cardio, Weights, Yoga'),
('Iron Paradise', 'Near Gate 1', 'Powerlifting, CrossFit');
