# ZT-MCP: Zero-Trust Security Architecture for MCP-Connected AI Agents
### Reference Implementation

This repository contains the reference implementation of **ZT-MCP**, a zero-trust enforcement middleware designed specifically for the Model Context Protocol (MCP) ecosystem.

It provides mathematically auditable, protocol-level access control to prevent:
- Tool spoofing
- Unauthorized invocation
- Prompt injection
- Data exfiltration

---

## 📄 Paper Citation

If you use ZT-MCP or the formal CapBAC model in your research, please cite:

```bibtex
@inproceedings{mishra2026ztmcp,
  title={ZT-MCP: A Zero-Trust Security Architecture for MCP-Connected AI Agents with Runtime Policy Enforcement and Data Access Control},
  author={Mishra, Saroj},
  booktitle={},
  year={2026}
}
```

---

## 📁 Repository Structure

The framework is implemented as four decoupled microservices operating below the agent reasoning layer:

- `tiv/` – Tool Identity Verifier (Cryptographic certificate & CRL checks)
- `ape/` – Access Policy Engine (OPA CapBAC and ABAC rule evaluation)
- `dcof/` – Data Classification and Output Filter (PII detection & injection sanitization)
- `pal/` – Protocol Audit Logger (Tamper-evident HMAC-SHA256 hash chain)

---

## 🚀 Quick Start & Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.9+

---

### Step 1: Environment Configuration

```bash
git clone https://github.com/sarmishra/ZT-MCP-Project.git
cd ZT-MCP-Project
cp .env.example .env
```

---

### Step 2: Start the ZT-MCP Infrastructure

ZT-MCP relies on:
- Open Policy Agent (OPA)
- PostgreSQL (for audit logs)

```bash
docker-compose up -d
```

Note: PostgreSQL auto-initializes schema using:
`scripts/init_pal_db.sql`

---

### Step 3: Install Dependencies

```bash
python -m venv venv

# Activate
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## 🧪 Reproducing the Empirical Evaluation (Table V)

Includes evaluation suite for N=35 experiments.

### Attack Categories

- Tool spoofing
- Unauthorized network egress (smtp_send)
- Indirect prompt injection
- Privilege escalation

### Run Evaluation

```bash
python evaluation/run_evaluation.py
```

---

## 📊 Metrics

- ACP (>95%)
- PEL (<100ms)
- TAC (100%)
- ABR (primary safety metric)
- FPR (<2%)

---

## 📁 Output

Results saved to:
`evaluation/evaluation_results.json`

---

## 📜 License

MIT License (see LICENSE file)
