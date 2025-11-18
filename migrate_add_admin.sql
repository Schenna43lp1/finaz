-- Migration script to add is_admin field to existing users table
-- This should be run if you already have a users table without the is_admin field

USE finaz_db;

-- Add is_admin column if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE AFTER email;

-- Optionally, make the first user an admin (uncomment the next line)
-- UPDATE users SET is_admin = TRUE WHERE id = 1;
