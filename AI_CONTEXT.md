# Project: PT-Elex-Vis (Portugal Election Visualizer)

## Tech Stack
- Backend: Flask (Python 3.11+)
- Database: PostgreSQL + PostGIS (Dockerized)
- Frontend: Vanilla JS + D3.js (SVG-based)
- Data Format: TopoJSON (for boundaries), JSON/CSV (for results)

## Directory Structure
All code lives in `src/` directories for clean organization:
```
project/
├── backend/
│   ├── srcs/           # Python source code
│   ├── docs/          # Backend documentation
│   ├── app.py         # Entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── srcs/           # Frontend source
│   │   ├── js/        # JavaScript modules
│   │   ├── css/       # Stylesheets
│   │   └── assets/    # Images, fonts, data
│   ├── docs/          # Frontend documentation
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
└── db/                # Database setup
```

## Core Logic (The DICO System)
- All geography and results MUST be linked via DICO codes:
  - Level 1: District (2 digits, e.g., "11")
  - Level 2: Concelho (4 digits, e.g., "1106")
  - Level 3: Freguesia (6 digits, e.g., "110608")
- IMPORTANT: DICO codes must be treated as STRINGS to preserve leading zeros.

## Frontend Requirements
- No heavy frameworks (No React/Vue).
- Use D3.js for SVG path rendering.
- Implement "drill-down" by swapping TopoJSON layers and updating D3 projections.

## Live Data Strategy
- Poll `eleicoes.mai.gov.pt` every 2-5 mins during election night.
- Upsert results into Postgres `results` table.