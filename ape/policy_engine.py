import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("ZT-MCP-APE")

class AccessPolicyEngine:
    def __init__(self):
        # Maps to the OPA server running via docker-compose
        self.opa_url = os.getenv("OPA_SERVER_URL", "http://localhost:8181/v1/data/ztmcp/allow")

    def evaluate_access(self, agent_id: str, tool_name: str, action: str, capability_token: Dict[str, Any]) -> bool:
        """Evaluates tool invocation against OPA CapBAC/ABAC policies."""
        logger.info(f"APE: Evaluating access for {agent_id} -> {tool_name} ({action})")
        
        # Construct the context payload for OPA Rego evaluation
        payload = {
            "input": {
                "agent_id": agent_id,
                "tool_name": tool_name,
                "action": action,
                "capability_token": capability_token,
                "timestamp": 1712000000 # Mock current timestamp for evaluation
            }
        }

        try:
            response = requests.post(self.opa_url, json=payload, timeout=0.05) # <50ms SLA
            response.raise_for_status()
            result = response.json()
            
            is_allowed = result.get("result", False)
            if is_allowed:
                logger.info("APE ALLOW: CapBAC and ABAC policies satisfied.")
            else:
                logger.warning(f"APE DENY: Policy violation for tool '{tool_name}'.")
                
            return is_allowed
            
        except requests.exceptions.RequestException as e:
            # Deny-by-default axiom enforces denial if OPA is unreachable
            logger.error(f"APE DENY: Policy engine unreachable or timed out. {e}")
            return False
