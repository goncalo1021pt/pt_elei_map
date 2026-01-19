-- Initialize PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create DICO codes table
CREATE TABLE IF NOT EXISTS dico_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(6) NOT NULL UNIQUE,
    level INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    parent_code VARCHAR(6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create elections table
CREATE TABLE IF NOT EXISTS elections (
    id SERIAL PRIMARY KEY,
    election_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create results table
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    election_id VARCHAR(50) NOT NULL,
    dico_code VARCHAR(6) NOT NULL,
    party_code VARCHAR(10) NOT NULL,
    votes INTEGER DEFAULT 0,
    percentage DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (election_id) REFERENCES elections(election_id),
    FOREIGN KEY (dico_code) REFERENCES dico_codes(code),
    UNIQUE(election_id, dico_code, party_code)
);

-- Create indexes
CREATE INDEX idx_dico_code ON dico_codes(code);
CREATE INDEX idx_dico_level ON dico_codes(level);
CREATE INDEX idx_results_election ON results(election_id);
CREATE INDEX idx_results_dico ON results(dico_code);
