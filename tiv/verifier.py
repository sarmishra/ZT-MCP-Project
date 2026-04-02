import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ZT-MCP-TIV")

class ToolIdentityVerifier:
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        # Simulated Certificate Registry and Revocation List (CRL)
        self.authorized_tools = {
            "financial_db_query": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "report_generator": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
        }
        self.revoked_tools = ["financial_db_query_v2", "smtp_send_unverified"]

    def verify_tool(self, tool_name: str, provided_manifest_hash: str) -> bool:
        """Verifies tool identity against the trusted registry and CRL."""
        logger.info(f"TIV: Verifying identity for tool '{tool_name}'")
        
        if tool_name in self.revoked_tools:
            logger.warning(f"TIV DENY: Tool '{tool_name}' is on the Certificate Revocation List (CRL).")
            return False
            
        if tool_name not in self.authorized_tools:
            logger.warning(f"TIV DENY: Tool '{tool_name}' is unregistered. Spoofing attempt detected.")
            return False

        expected_hash = self.authorized_tools[tool_name]
        if provided_manifest_hash != expected_hash:
            logger.error(f"TIV DENY: Hash mismatch for '{tool_name}'. Integrity verification failed.")
            return False

        logger.info(f"TIV ALLOW: Identity verified for '{tool_name}'.")
        return True
