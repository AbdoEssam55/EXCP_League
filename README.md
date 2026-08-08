# EXCP League ⚽
### *Powered by EXCP Football*

A full-stack 5v5 internal football league management platform built with ASP.NET Core and vanilla JS.

![.NET](https://img.shields.io/badge/.NET-8.0-purple)
![EF Core](https://img.shields.io/badge/EF%20Core-8.0-blue)
![SQL Server](https://img.shields.io/badge/SQL%20Server-LocalDB-red)
![License](https://img.shields.io/badge/license-internal-green)

---

## Features

- **League Dashboard** — Standings, upcoming matches, top scorers, top assists, recent results
- **Team Pages** — Squad with player cards, formation view
- **Player Profiles** — Photo, stats (goals, assists, cards, appearances, minutes), OVR rating
- **Match Pages** — Interactive SVG pitch with formation view, chronological event timeline
- **Admin Portal** — Full CRUD for teams, players, matches. Manage lineups, events, and import players
- **Player Import** — CSV and Excel (.xlsx) file import for bulk player data
- **Image Management** — Upload/replace/delete player photos and team logos
- **JWT Authentication** — Role-based access (Admin/Viewer)
- **Auto-calculated Stats** — Goals, assists, standings, and scores derived from match events
- **Responsive Design** — Premium dark football-themed UI, fully mobile-friendly

---

## Architecture

```
Clean Architecture with 4 layers:

ExcpFootball.Domain           → Entities, Enums (no dependencies)
ExcpFootball.Application      → DTOs, Interfaces, Validators, Services
ExcpFootball.Infrastructure   → EF Core DbContext, Data Seeder, Service Implementations
ExcpFootball.Api              → Controllers, Middleware, JWT Config, Static Frontend (wwwroot)
ExcpFootball.Tests            → xUnit tests with EF InMemory
```

---

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- [SQL Server LocalDB](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/sql-server-express-localdb) (included with Visual Studio / SQL Server Express)

---

## Quick Start

### 1. Clone and navigate
```bash
cd ExcpFootball
```

### 2. Restore packages
```bash
dotnet restore
```

### 3. Run the application
```bash
dotnet run --project src/ExcpFootball.Api
```

The app will:
- Create the database automatically (EnsureCreated)
- Seed sample data (admin user, 2 teams, 14 players, 2 matches)
- Start the server on `http://localhost:5000` and `https://localhost:5001`

### 4. Open in browser
Navigate to **http://localhost:5000** (or https://localhost:5001)

---

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |

---

## Seeded Data

### Teams
| Team | Short | Players |
|------|-------|---------|
| Backend Development | BE | 7 players (5 starters + 2 reserves) |
| Mobile Development | MD | 7 players (5 starters + 2 reserves) |

### Sample Matches
- **Match 1** (Completed): Backend Dev 2 - 1 Mobile Dev
  - ⚽ 15' Aufinho (assist: menbo)
  - ⚽ 45' Magdy
  - ⚽ 80' Mohamed Hamed (assist: Aufinho)
- **Match 2** (Scheduled): Mobile Dev vs Backend Dev (upcoming)

---

## API Endpoints

### Public (No Auth)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | League dashboard data |
| GET | `/api/teams` | All teams |
| GET | `/api/teams/{id}` | Team detail with players |
| GET | `/api/players` | All players |
| GET | `/api/players/{id}` | Player detail with stats |
| GET | `/api/matches` | All matches |
| GET | `/api/matches/{id}` | Match detail with lineups + events |
| GET | `/api/seasons` | All seasons |
| POST | `/api/auth/login` | Login (returns JWT) |

### Admin Only (JWT + Admin Role)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/teams` | Create team |
| PUT | `/api/teams/{id}` | Update team |
| POST | `/api/teams/{id}/logo` | Upload team logo |
| POST | `/api/players` | Create player |
| PUT | `/api/players/{id}` | Update player |
| DELETE | `/api/players/{id}` | Delete player |
| POST | `/api/players/{id}/photo` | Upload player photo |
| DELETE | `/api/players/{id}/photo` | Delete player photo |
| POST | `/api/players/import` | Import from CSV/Excel |
| POST | `/api/matches` | Create match |
| PUT | `/api/matches/{id}` | Update match |
| POST | `/api/matches/{id}/lineups` | Set lineups |
| POST | `/api/matches/{id}/events` | Add match event |
| DELETE | `/api/matches/{id}/events/{eventId}` | Remove event |

### Swagger
Available at `/swagger` in development mode.

---

## CSV/Excel Import Format

The import expects these columns:

| Column | Required | Example |
|--------|----------|---------|
| PlayerName | Yes | Mohamed Hamed |
| NickName | No | الجناح الخارق |
| Number | Yes | 8 |
| Position | Yes | LW |
| Overall | No | 91 |
| Team | Yes | Backend Development |

Supported positions: `GK`, `CB`, `LW`, `RW`, `CM`, `CAM`, `ST`

---

## Running Tests

```bash
dotnet test
```

Tests cover:
- Top scorers calculation
- Top assists calculation
- Player stats aggregation (goals, assists, cards)
- Standings calculation (points, goal difference)
- Scheduled match exclusion from standings

---

## Project Structure

```
├── ExcpFootball.sln
├── README.md
├── src/
│   ├── ExcpFootball.Domain/
│   │   ├── Entities/          (Season, Team, Player, Match, MatchLineup, MatchEvent, User)
│   │   └── Enums/             (Position, MatchEventType, MatchStatus, UserRole)
│   ├── ExcpFootball.Application/
│   │   ├── DTOs/              (Auth, Teams, Players, Matches, Seasons, Dashboard)
│   │   ├── Interfaces/        (Service interfaces)
│   │   └── Validators/        (FluentValidation)
│   ├── ExcpFootball.Infrastructure/
│   │   ├── Data/              (DbContext, DataSeeder)
│   │   └── Services/          (All service implementations)
│   └── ExcpFootball.Api/
│       ├── Controllers/       (Auth, Teams, Players, Matches, Seasons, Dashboard)
│       ├── Middleware/        (ExceptionHandling)
│       └── wwwroot/           (Frontend SPA)
│           ├── index.html
│           ├── css/style.css
│           ├── js/
│           │   ├── app.js     (SPA router, API client, auth)
│           │   ├── components/ (loader, navbar, pitch, timeline, modal, toast)
│           │   └── pages/     (dashboard, teams, players, matches, login, admin/)
│           └── assets/        (default SVGs)
└── tests/
    └── ExcpFootball.Tests/    (xUnit tests)
```

---

## Configuration

Edit `src/ExcpFootball.Api/appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=ExcpFootballDb;..."
  },
  "JwtSettings": {
    "Key": "your_secret_key_at_least_32_bytes",
    "Issuer": "ExcpFootballApi",
    "Audience": "ExcpFootballUsers",
    "ExpiryInMinutes": "1440"
  },
  "FileStorage": {
    "BasePath": "wwwroot/uploads"
  }
}
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | ASP.NET Core 8.0, C# |
| ORM | Entity Framework Core 8.0 |
| Database | SQL Server (LocalDB) |
| Auth | JWT Bearer Tokens, BCrypt |
| Validation | FluentValidation |
| Import | ClosedXML (.xlsx), CSV parsing |
| Frontend | Vanilla HTML/CSS/JS (SPA) |
| Testing | xUnit, EF InMemory, Moq |

---

*Built for the EXCP 5v5 football league* ⚽🏆
