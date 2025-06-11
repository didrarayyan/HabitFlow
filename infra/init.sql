-- HabitFlow Database Initialization Script
-- This script sets up the initial database structure and data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if it doesn't exist (this is handled by docker-compose)
-- The database 'habitflow' is created automatically by the postgres container

-- Set timezone
SET timezone = 'UTC';

-- Create initial admin user (will be handled by the application)
-- This is just a placeholder for any additional database setup

-- Create indexes for better performance (these will be created by SQLAlchemy)
-- But we can add some additional ones here if needed

-- Insert initial data if needed
-- For now, we'll let the application handle all data creation

-- Log the initialization
DO $$
BEGIN
    RAISE NOTICE 'HabitFlow database initialized successfully';
END $$;

