-- ZT-MCP Protocol Audit Logger (PAL) Schema

CREATE TABLE IF NOT EXISTS audit_events (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_id VARCHAR(255) NOT NULL,
    tool_name VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    decision VARCHAR(50) NOT NULL, -- 'ALLOW' or 'DENY'
    denial_reason TEXT,
    payload_hash VARCHAR(64) NOT NULL,
    prev_hash VARCHAR(64) NOT NULL, -- Cryptographic linkage
    signature VARCHAR(255) NOT NULL -- HMAC-SHA256 of current row
);

CREATE INDEX idx_tool_name ON audit_events(tool_name);
CREATE INDEX idx_timestamp ON audit_events(timestamp);
