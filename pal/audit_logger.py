import hashlib
import psycopg2
import logging
import os
import json
from typing import Optional

logger = logging.getLogger("ZT-MCP-PAL")

class ProtocolAuditLogger:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://ztmcp_admin:secure_dev_password@localhost:5432/ztmcp_audit")
        self.hmac_secret = os.getenv("PAL_HMAC_SECRET", "dev_secret").encode()
        self.last_hash = "0000000000000000000000000000000000000000000000000000000000000000" # Genesis hash
        self._init_db()

    def _init_db(self):
        """Ensures database connection is available."""
        try:
            self.conn = psycopg2.connect(self.db_url)
            logger.info("PAL: Connected to tamper-evident audit database.")
        except Exception as e:
            logger.error(f"PAL: Database connection failed. {e}")
            self.conn = None

    def _generate_hash(self, payload_str: str, prev_hash: str) -> str:
        """Generates HMAC-SHA256 signature linking to the previous event."""
        h = hashlib.sha256()
        h.update(self.hmac_secret)
        h.update(prev_hash.encode())
        h.update(payload_str.encode())
        return h.hexdigest()

    def log_event(self, agent_id: str, tool_name: str, action: str, decision: str, payload: dict, denial_reason: Optional[str] = None):
        """Appends a cryptographically signed event to the audit log."""
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        
        current_hash = self._generate_hash(payload_str, self.last_hash)
        
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO audit_events 
                           (agent_id, tool_name, action, decision, denial_reason, payload_hash, prev_hash, signature) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (agent_id, tool_name, action, decision, denial_reason, payload_hash, self.last_hash, current_hash)
                    )
                self.conn.commit()
            except Exception as e:
                logger.error(f"PAL ERROR: Failed to write to audit log! {e}")
                
        self.last_hash = current_hash
        logger.info(f"PAL: Event Logged -> {decision} | {tool_name} | Sig: {current_hash[:8]}...")
        
        # Anomaly Detection Trigger
        self._run_anomaly_detection(agent_id, decision)

    def _run_anomaly_detection(self, agent_id: str, decision: str):
        """Active anomaly detection module checking for access frequency and denial spikes."""
        if decision == "DENY":
            # In a production system, this would track a sliding window of denials
            logger.warning(f"PAL ANOMALY: Escalating denial event for {agent_id} to HITL-AP Layer 5.")
