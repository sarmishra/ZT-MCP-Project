# ZT-MCP: Zero-Trust Security Architecture for MCP-Connected AI Agents
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
  title={ZT-MCP: A Zero-Trust Security Architecture for MCP-Connected AI Agents with Runtime Policy Enforcement and Data Access Control},
  author={Mishra, Saroj},
  booktitle={},
  year={2026}
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

## 📊 Evaluation Metrics

| Metric | Description | Target |
|--------|------------|--------|
| ACP | Access Control Precision | > 95% |
| PEL | Policy Enforcement Latency | < 100 ms |
| TAC | Tool Audit Coverage | 100% |
| ABR | Attack Block Rate (primary safety metric) | High |
| FPR | False Positive Rate | < 2% |

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
