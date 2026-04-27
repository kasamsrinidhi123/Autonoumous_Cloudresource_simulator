# CloudScale — Dynamic Auto Scaling Simulation Platform

A full-stack web application that simulates AWS Auto Scaling behavior with real-time monitoring, load testing, and cost analysis — all running locally with zero cloud costs.

**SDG 9 — Industry, Innovation and Infrastructure**

---

## Features

- **Login / Signup** — Secure authentication with PBKDF2-SHA256 hashed passwords, SQLite database
- **Live Dashboard** — Auto-refreshes every 2 seconds with real-time CPU, memory, instance count metrics
- **Instance Fleet** — Individual instance cards showing per-instance CPU, memory, health status, and request count
- **Auto Scaling Engine** — Policy-based scaling (Scale Out at >70% CPU, Scale In at <30% CPU) with stabilization loop
- **Load Generator** — Interactive slider + quick presets (100, 300, 500, 750, 1000 users) to simulate traffic
- **System Architecture** — Visual component diagram showing how Users → Load Balancer → ASG → EC2 → CloudWatch interact
- **Live Metrics** — 4-panel Plotly charts (CPU, Memory, Instances, Users) with stats summary
- **Scaling Activity** — Timeline of all scale-out/scale-in events with timestamps and reasons
- **Cost Analysis** — Compares auto-scaled cost vs fixed provisioning with savings calculation
- **About Page** — AWS concepts explained, tech stack, usage guide

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Charts | Plotly |
| Database | SQLite |
| Backend | Python 3.12 |
| Auth | PBKDF2-SHA256 + Salt |
| Hosting | Local (no cloud required) |

---

## Project Structure

```
autoscaling_project/
├── Home.py                          # Main dashboard + auth gate
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── backend/
│   ├── __init__.py                  # Package init
│   ├── auth.py                      # Login/Signup UI + session management
│   ├── autoscaler.py                # Scaling engine (threshold-based + stabilization loop)
│   ├── db.py                        # SQLite database setup + user CRUD
│   ├── metrics.py                   # CPU & memory calculation formulas
│   └── state.py                     # SystemState + InstanceInfo (fleet tracking)
└── pages/
    ├── 1_Overview.py                # Gauges + key stats
    ├── 2_System_Architecture.py     # Interactive architecture diagram
    ├── 3_Load_Generator.py          # Slider + preset buttons to simulate load
    ├── 4_Live_Metrics.py            # 4-panel charts + stats tables
    ├── 5_Auto_Scaling_Activity.py   # Scaling event timeline + system logs
    ├── 6_Cost_Analysis.py           # Cost comparison + savings + pricing table
    └── 7_About_Project.py           # Project info + AWS concepts
```

---

## How to Run

### Prerequisites

- Python 3.9 or higher (recommended: Python 3.12)
- pip or uv package manager

### Step 1: Install Python (if not already installed)

**macOS:**
```bash
# Using uv (recommended — fast)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12

# Or using Homebrew
brew install python@3.12
```

**Windows:**
Download from https://www.python.org/downloads/ and install Python 3.12+

**Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### Step 2: Create Virtual Environment

```bash
cd autoscaling_project

# Using uv
uv venv --python 3.12 .venv

# Or using standard Python
python3.12 -m venv .venv
```

### Step 3: Activate Virtual Environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Using uv
uv pip install streamlit plotly

# Or using pip
pip install streamlit plotly
```

### Step 5: Run the Application

```bash
streamlit run Home.py --server.headless true
```

The app will open at **http://localhost:8501**

---

## How to Use (Demo Flow)

### 1. Create an Account
- Open http://localhost:8501
- Click "Create Account" tab
- Enter your name, email, and password
- Click "Create Account"

### 2. View the Dashboard
- After login, you'll see the CloudScale Dashboard
- It shows: Active Users, Instances, CPU Usage, Memory Usage
- The dashboard auto-refreshes every 2 seconds

### 3. Generate Load
- Navigate to **Load Generator** (sidebar)
- Use the slider or click quick presets:
  - **100 Users** — Low load, 1 instance handles it
  - **500 Users** — Medium load, instances scale out
  - **1000 Users** — High load, 5-6 instances spin up
- Click **Apply Load** or any preset button

### 4. Watch Auto Scaling in Action
- Go back to **Home** dashboard
- Watch in real-time:
  - CPU spikes → instances scale OUT (new instance cards appear)
  - Each instance shows its own CPU, memory, health
  - Charts update live showing the scaling timeline

### 5. Stop Load and Watch Scale Down
- Go to **Load Generator** → click **Stop Load**
- Return to **Home** — instances scale DOWN to 1
- CPU drops, excess instance cards disappear

### 6. Explore Other Pages
- **Overview** — Plotly gauges for CPU/Memory + delta indicators
- **Architecture** — Visual flow diagram (highlights active components)
- **Live Metrics** — 4-panel charts with min/max/avg stats
- **Scaling Activity** — Timeline of all scaling events with reasons
- **Cost Analysis** — See how autoscaling saves 90% vs fixed provisioning
- **About** — AWS concepts explained

---

## How Auto Scaling Works

```
┌─────────────────────────────────────────────┐
│                                             │
│   Users (0-1000)                            │
│       │                                     │
│       ▼                                     │
│   Load Balancer                             │
│       │                                     │
│       ▼                                     │
│   Auto Scaling Group                        │
│   ┌────────────────────────────────┐        │
│   │ Policy: CPU > 70% → Scale Out │        │
│   │ Policy: CPU < 30% → Scale In  │        │
│   │ Min: 1 | Max: 10 | Cooldown: 2s│       │
│   └────────────────────────────────┘        │
│       │                                     │
│       ▼                                     │
│   EC2 Instances (1 to 10)                   │
│   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐           │
│   │ 1 │ │ 2 │ │ 3 │ │ 4 │ │...│           │
│   └───┘ └───┘ └───┘ └───┘ └───┘           │
│       │                                     │
│       ▼                                     │
│   CloudWatch Monitoring                     │
│   (CPU, Memory, Requests — every 2s)        │
│       │                                     │
│       ▼                                     │
│   Dashboard (auto-refresh)                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Scaling Rules

| Condition | Action | Details |
|-----------|--------|---------|
| CPU > 70% | Scale Out | Add instances to bring CPU toward 50% |
| CPU < 30% | Scale In | Remove instances proportionally |
| CPU < 5%, 0 users | Emergency Scale In | Drop to 1 instance immediately |
| CPU < 15% | Aggressive Scale In | Halve the fleet |
| Any scaling | Cooldown | 2 second wait between scaling decisions |
| Any scaling | Stabilization | Up to 10 rounds per tick until metrics stabilize |

---

## Cost Comparison

| Scenario | Monthly Cost | Savings |
|----------|-------------|---------|
| Auto Scaled (current) | ~$8.35 | 90% |
| Fixed 2 instances | $16.70 | 80% |
| Fixed 5 instances | $41.75 | 50% |
| Fixed 10 instances | $83.50 | 0% (baseline) |

*Based on AWS t2.micro pricing: $0.0116/hour per instance*

---

## SDG Alignment

**Primary: SDG 9 — Industry, Innovation and Infrastructure**
- Promotes efficient, sustainable infrastructure management
- Demonstrates how auto scaling reduces computational waste
- Data centers consume 1-2% of global electricity — auto scaling minimizes this

**Secondary:**
- SDG 12 — Responsible Consumption (use resources only when needed)
- SDG 13 — Climate Action (less waste = less energy = lower carbon)
- SDG 4 — Quality Education (free learning tool for cloud concepts)

---

## Security

- Passwords hashed with PBKDF2-SHA256 (100,000 iterations + random salt)
- Session management via Streamlit session state
- Input validation on all forms
- No cloud credentials required — fully local

---

## Future Scope

- Integration with real AWS/Azure APIs (boto3, Azure SDK)
- Machine learning-based predictive auto scaling
- Container orchestration simulation (Kubernetes HPA)
- Multi-region deployment with latency modeling
- Custom metric support (network I/O, disk, latency)

---

## Team

- **Project:** Industry Oriented Mini Project (IOMP)
- **Institution:** Sreyas Institute of Engineering and Technology
- **Academic Year:** 2025-26
- **SDG:** 9 — Industry, Innovation and Infrastructure
