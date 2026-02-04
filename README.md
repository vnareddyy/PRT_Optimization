# PRT Survey Data Analysis

## Pittsburgh Regional Transit - Public Transportation Feedback Analysis

### Overview
Analysis of **1,736 survey responses** to extract actionable insights for transit planning from the PRT Network Redesign public feedback.

### Key Findings

#### Priority Routes (Top 10)
| Route | Mentions | Priority | Issue |
|-------|----------|----------|-------|
| **54** | 254 | 🔴 HIGH | Service elimination concern |
| **28X** | 222 | 🔴 HIGH | Airport/service changes |
| **P1** | 186 | 🟠 MEDIUM | Purple Line popularity |
| **61A** | 185 | 🟠 MEDIUM | South Hills corridor |
| **61C** | 185 | 🟠 MEDIUM | South Hills corridor |
| **64** | 174 | 🟠 MEDIUM | Squirrel Hill connection |
| **71C** | 158 | 🟠 MEDIUM | East End corridor |
| **87** | 158 | 🟠 MEDIUM | Friendship/East Liberty |
| **75** | 153 | 🟠 MEDIUM | South Side connection |
| **71B** | 152 | 🟠 MEDIUM | East End corridor |

#### Action Type Distribution
| Action Type | Count | Percentage |
|-------------|-------|------------|
| **INCREASE_FREQUENCY** | 501 | 51.0% |
| IMPROVE_COVERAGE | 165 | 16.8% |
| ADD_SERVICE | 137 | 13.9% |
| DIRECT_CONNECTION | 95 | 9.7% |
| IMPROVE_RELIABILITY | 46 | 4.7% |
| PREVENT_ELIMINATION | 36 | 3.7% |
| RESTORE_SERVICE | 16 | 1.6% |

#### Geographic Patterns
| Area | Mentions | Description |
|------|----------|-------------|
| **Downtown** | 317 | Primary destination |
| **Oakland** | 279 | Universities/hospitals |
| **Greenfield** | 59 | Service concern area |
| **Millvale** | 56 | Connectivity hub |
| **Airport** | 53 | Transit access |

### Identified Connectivity Gaps
1. **South Hills ↔ Oakland**: Need direct service
2. **Squirrel Hill ↔ Downtown**: Frequency improvements
3. **Bloomfield ↔ Oakland**: No direct route exists
4. **Greenfield ↔ Downtown/Oakland**: Service elimination concern

### Files
```
ds_practicum/
├── main_analysis_fixed.py   # Main analysis pipeline
├── README.md               # This file
├── data/
│   └── processed/
│       ├── routes_mentioned.csv
│       ├── action_types.csv
│       └── geographic_areas.csv
└── reports/
    └── insights.json
```

### Running the Analysis
```bash
cd /Users/vinaynareddy/Documents/ds_practicum
python3 main_analysis_fixed.py
```

### Requirements
- pandas
- Python 3.x

### Author
Data Science Practicum Project


