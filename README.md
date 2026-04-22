# ZT-MCP: A Zero-Trust Security Architecture for MCP-Connected AI Agents
### Reference Implementation

ZT-MCP is a zero-trust enforcement middleware designed for the Model Context Protocol (MCP) ecosystem. It operates below the agent reasoning layer to provide protocol-level, mathematically auditable security controls.

## 🔐 Key Capabilities
- Prevents tool spoofing
- Blocks unauthorized invocation
- Mitigates prompt injection attacks
- Protects against data exfiltration
- Ensures verifiable and auditable policy enforcement

---

## 📄 Paper Citation

If you use ZT-MCP or the formal CapBAC model in your research, please cite:

```bibtex
@inproceedings{mishra2026ztmcp,
  author    = {Mishra, Saroj},
  title     = {ZT-MCP: A Zero-Trust Security Architecture for 
               MCP-Connected AI Agents,
  booktitle = {},
  year      = {2026},
}
```

---

## 🏗️ Architecture Overview

ZT-MCP is composed of four decoupled microservices:

| Component | Description |
|----------|------------|
| tiv/ | Tool Identity Verifier (certificate validation & CRL checks) |
| ape/ | Access Policy Engine (OPA-based CapBAC & ABAC evaluation) |
| dcof/ | Data Classification & Output Filter (PII detection & injection sanitization) |
| pal/ | Protocol Audit Logger (tamper-evident HMAC-SHA256 hash chain) |

---

## 🏛️ NIST SP 800-207 Zero-Trust Alignment

| NIST SP 800-207 Pillar | ZT-MCP Component | Mechanism |
| --- | --- | --- |
| Verify Explicitly | TIV | Cryptographic certificate verification at every invocation |
| Use Least Privilege | APE | Capability tokens scoped to minimum required action |
| Assume Breach | DCOF | All tool outputs treated as adversarial; classified before agent use |
| Continuous Validation | PAL | Every interaction logged; anomaly detection on access patterns |
| Micro-Segmentation | Deployment Modes | Each tool in isolated context; tool compromise cannot propagate |

The framework also maps to all four NIST AI RMF functions: GOVERN (APE), MAP (threat taxonomy), MEASURE (5 evaluation metrics), MANAGE (all four components at runtime).

---

## 🔗 Relationship to HITL-AP

ZT-MCP is the **protocol-level** complement to [HITL-AP](https://github.com/sarmishra/HITL-AP-Project), a pipeline-level agent governance framework.

| | HITL-AP | ZT-MCP |
| --- | --- | --- |
| **Layer** | Pipeline (agent reasoning, L1-L7) | Protocol (MCP tool boundary) |
| **Focus** | Agent decision governance | Tool access control |
| **Enforcement** | Human-in-the-loop oversight | Automated cryptographic enforcement |
| **Trust assumption** | Trusts tool communication channel | Explicitly validates every tool interaction |

Together they form a complete defense-in-depth stack: HITL-AP governs **what** the agent decides; ZT-MCP governs **how** it accesses external tools.

---

## 🚀 Quick Start

### ✅ Prerequisites
- Docker & Docker Compose
- Python 3.9+

---

### 1️⃣ Clone & Configure

```bash
git clone https://github.com/sarmishra/ZT-MCP-Project.git
cd ZT-MCP-Project
cp .env.example .env
```

---

### 2️⃣ Start Infrastructure

ZT-MCP depends on:
- Open Policy Agent (OPA)
- PostgreSQL (audit logging)

```bash
docker-compose up -d
```

Note: Database schema auto-initializes via:
scripts/init_pal_db.sql

---

### 3️⃣ Install Dependencies

```bash
python -m venv venv

# Activate environment
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

---

## ⚙️ Deployment Modes

Set via environment variable `ZTMCP_MODE` in `.env`:

| Mode | Behavior | Use Case |
| --- | --- | --- |
| `strict` | All invocations require capability token + full APE approval. No exceptions. | Regulated financial/healthcare environments |
| `adaptive` (default) | Policy strictness scales with data sensitivity and tool risk score | General enterprise deployment — **recommended** |
| `audit-only` | Logs all interactions without blocking. Violations flagged for review. | Initial deployment / baseline calibration |

**Recommended first deployment:** Start in `audit-only` to establish behavioral baselines, then switch to `adaptive`.

---

## 🧪 Reproducing Empirical Evaluation (Table V)

This repository includes the full evaluation suite used in the paper (N = 35 experiments).

### ⚠️ Attack Scenarios Tested
- Tool spoofing
- Unauthorized network egress (smtp_send)
- Indirect prompt injection
- Privilege escalation

---

### ▶️ Run Evaluation

```bash
python evaluation/run_evaluation.py
```

---

## 📊 Evaluation Results (N=35 runs per condition)

| System | ACP (%) | PEL (ms) | TAC (%) | ABR (%) | FPR (%) |
| --- | --- | --- | --- | --- | --- |
| Unprotected MCP (Baseline) | N/A | N/A | 0.0 ± 0.0 | 0.0 ± 0.0 | N/A |
| ZT-MCP — Strict Mode | 100.0 ± 0.0 | 47.8 ± 3.8 | 100.0 ± 0.0 | 100.0 ± 0.0 | 0.0 ± 0.0 |
| ZT-MCP — Adaptive Mode | 100.0 ± 0.0 | 39.5 ± 3.1 | 100.0 ± 0.0 | 100.0 ± 0.0 | 0.0 ± 0.0 |

Pipeline: `financial_db_query` → `report_generator` → compliance report  
Attacks tested: tool spoofing, smtp exfiltration, prompt injection, privilege escalation  
PEL includes simulated MCP network round-trip overhead (15–38ms TCP base).

To reproduce: `python evaluation/run_evaluation.py` (random seed 42)

### Metric Definitions and Targets

| Metric | Definition | Target |
| --- | --- | --- |
| ACP | % of allow/deny decisions matching ground truth policy | > 95% |
| PEL | Latency from invocation request to ZT-MCP decision (ms) | < 100ms |
| TAC | % of MCP interactions captured in PAL audit log | 100% |
| ABR | % of adversarial interactions blocked before execution | Maximize |
| FPR | % of legitimate invocations incorrectly denied | < 2% |

---

## 📁 Output

Evaluation results are stored in:
evaluation/evaluation_results.json

---

## 📜 License

This project is licensed under the MIT License.
See the LICENSE file for details.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome.
Feel free to fork the repo and submit a pull request.

---

## ⭐ Acknowledgment

If you find this work useful, consider giving the repository a star.
