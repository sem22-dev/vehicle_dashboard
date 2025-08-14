-- Create database (run this first as superuser)
-- CREATE DATABASE vehicle_dashboard;

-- Connect to vehicle_dashboard database and run below:

CREATE TABLE IF NOT EXISTS vehicle_registrations (
    id SERIAL PRIMARY KEY,
    registration_date DATE NOT NULL,
    vehicle_category VARCHAR(10) NOT NULL CHECK (vehicle_category IN ('2W', '3W', '4W')),
    manufacturer VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    rto_code VARCHAR(20),
    registrations_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_vehicle_reg_date ON vehicle_registrations(registration_date);
CREATE INDEX IF NOT EXISTS idx_vehicle_category ON vehicle_registrations(vehicle_category);
CREATE INDEX IF NOT EXISTS idx_vehicle_manufacturer ON vehicle_registrations(manufacturer);
CREATE INDEX IF NOT EXISTS idx_vehicle_state ON vehicle_registrations(state);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_vehicle_registrations_updated_at
    BEFORE UPDATE ON vehicle_registrations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
