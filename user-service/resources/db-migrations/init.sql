DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT NOT NULL,
    address VARCHAR(500) NOT NULL,
    joining_date DATE NOT NULL,
    is_registered BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO users (first_name, last_name, email, age, address, joining_date, is_registered)
VALUES
    ('John', 'Doe', 'john.doe@example.com', 28, '123 Main St, New York, NY', '2024-01-15', TRUE),
    ('Jane', 'Smith', 'jane.smith@example.com', 32, '456 Oak Ave, Los Angeles, CA', '2024-02-20', TRUE),
    ('Bob', 'Johnson', 'bob.johnson@example.com', 45, '789 Pine Rd, Chicago, IL', '2024-03-10', FALSE);

