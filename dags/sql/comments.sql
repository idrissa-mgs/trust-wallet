CREATE TABLE IF NOT EXISTS comments (
    postId INT NOT NULL,
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    body TEXT NOT NULL
);
