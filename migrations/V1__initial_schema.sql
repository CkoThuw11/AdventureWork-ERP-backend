-- Initial Schema Migration
-- This migration creates the users table

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Insert sample data for testing
INSERT INTO users (email, username, full_name, is_active) VALUES
    ('john.doe@example.com', 'johndoe', 'John Doe', TRUE),
    ('jane.smith@example.com', 'janesmith', 'Jane Smith', TRUE),
    ('bob.wilson@example.com', 'bobwilson', 'Bob Wilson', FALSE);
