DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    option_1 VARCHAR(500) NOT NULL,
    option_2 VARCHAR(500) NOT NULL,
    option_3 VARCHAR(500) NOT NULL,
    option_4 VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option INT NOT NULL CHECK (selected_option BETWEEN 1 AND 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_question (user_id, question_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Sample poll questions
INSERT INTO questions (title, option_1, option_2, option_3, option_4)
VALUES
    ('Between the following, what do you most love to do?', 'Watch TV', 'Play the computer', 'Hanging out with friends', 'Travel the world'),
    ('Where is your preferred place to travel?', 'USA', 'France', 'South America', 'Thailand'),
    ('What is your favorite type of movie?', 'Action', 'Comedy', 'Drama', 'Sci-Fi');

-- Sample answers (assuming user IDs 1 and 2 exist in User Service)
INSERT INTO answers (user_id, question_id, selected_option)
VALUES
    (1, 1, 4),
    (1, 2, 2),
    (2, 1, 3),
    (2, 2, 1);

