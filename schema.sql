CREATE TABLE clans (
	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    name VARCHAR(255) NOT NULL,
	    region VARCHAR(10),
	    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- Index for performance
CREATE INDEX idx_clans_region ON clans(region);
CREATE INDEX idx_clans_created_at ON clans(created_at);

