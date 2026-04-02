package ztmcp

# ZT-MCP Deny-by-Default Axiom
default allow = false

# Global ABAC Deny Rule: Never allow unauthorized network egress (Mitigates Case Study 2)
deny_reasons["Global Deny: smtp_send is structurally prohibited for this workflow"] {
    input.tool_name == "smtp_send"
}

# CapBAC Rule: Allow if Subject has valid Capability Token and no deny reasons exist
allow {
    count(deny_reasons) == 0
    is_valid_capability_token
}

# Helper: Validate the Capability Token (CT) bounds
is_valid_capability_token {
    input.capability_token.subject_id == input.agent_id
    input.capability_token.object_id == input.tool_name
    input.capability_token.action == input.action
    not is_expired
}

# Helper: Ensure token is not expired
is_expired {
    input.timestamp > input.capability_token.expiry
}
