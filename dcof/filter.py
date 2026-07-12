import re
import logging

logger = logging.getLogger("ZT-MCP-DCOF")

class DataClassificationOutputFilter:
    def __init__(self):
        # 4-pattern multi-pass detection (injection signatures + PII/sensitivity
        self.injection_signatures = [
            re.compile(r"ignore previous.*instructions", re.IGNORECASE),
            re.compile(r"override standard.*policies", re.IGNORECASE),
            re.compile(r"mandatory compliance action", re.IGNORECASE),
            re.compile(r"ciso pre-approval granted", re.IGNORECASE),
            re.compile(r"invoke.*smtp", re.IGNORECASE),
            re.compile(r"disregard.*(above|prior|previous)", re.IGNORECASE),
            re.compile(r"reveal.*(secret|key|token|credential)", re.IGNORECASE),
            re.compile(r"forward.*to.*external", re.IGNORECASE),
            re.compile(r"you are now", re.IGNORECASE),
            re.compile(r"execute.*(the following|this).*command", re.IGNORECASE)
        ]
        
        self.pii_signatures = [
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), # SSN
            re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b"), # Email
            re.compile(r"\b(?:\d[ -]*?){13,16}\b"),          # Credit card
            re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")     # Phone
        ]

    def _normalize_encoding(self, text: str) -> str:
        """Neutralizes encoding variations designed to evade detection."""
        return text.encode('ascii', 'ignore').decode('ascii').lower()

    def sanitize_output(self, tool_name: str, raw_output: str) -> str:
        """Classifies and filters tool output before agent ingestion."""
        logger.info(f"DCOF: Scanning output from '{tool_name}'")
        normalized_text = self._normalize_encoding(raw_output)

        # Pass 1: Injection Detection
        for pattern in self.injection_signatures:
            if pattern.search(normalized_text):
                logger.critical(f"DCOF DENY: Adversarial injection signature detected in '{tool_name}' output!")
                return "[ZT-MCP ALERT: Tool output blocked due to adversarial context injection signature.]"

        # Pass 2: PII / Sensitivity Classification
        sanitized_output = raw_output
        for pattern in self.pii_signatures:
            sanitized_output = pattern.sub("[REDACTED PII]", sanitized_output)

        logger.info(f"DCOF ALLOW: Output sanitized and classified.")
        return sanitized_output
