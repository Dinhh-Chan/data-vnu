
CREATE TABLE db_connections (
    id SERIAL PRIMARY KEY,
    db_type VARCHAR(50) NOT NULL, -- mysql, postgresql, mongodb, sqlserver
    host VARCHAR(100) NOT NULL,
    port INTEGER NOT NULL,
    database_name VARCHAR(100) NOT NULL,
    username VARCHAR(100),
    password VARCHAR(200),
    extra_uri TEXT, -- cho MongoDB hoặc các loại đặc biệt
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE db_connections
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON db_connections
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
CREATE TABLE external_api_endpoints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_url VARCHAR(255) NOT NULL,
    swagger_url VARCHAR(255) NOT NULL,
    default_headers TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    path VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    summary VARCHAR(255),
    description TEXT,
    parameters JSON,
    request_body JSON,
    responses JSON
);
ALTER TABLE external_api_endpoints
ADD COLUMN created_at TIMESTAMP DEFAULT now(),
ADD COLUMN updated_at TIMESTAMP DEFAULT now();