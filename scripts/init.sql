-- Initial database setup script for PostgreSQL
-- This script is automatically run when the PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'UTC';

-- Create indexes for better performance (will be created after tables exist)
-- These will be created by Alembic migrations instead
