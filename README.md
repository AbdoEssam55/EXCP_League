# EXCP League (Powered by EXCP Football)

A complete full-stack web application for managing a 5-a-side football league, built with ASP.NET Core 8 Clean Architecture and a vanilla HTML/CSS/JS Single Page Application (SPA).

## Features

* **League Dashboard**: View current standings, top scorers, and recent match results.
* **Teams & Players Management**: Browse teams, view detailed player profiles, and track statistics.
* **Live Match Tracking**: Interactive match timeline with events (goals, assists, cards, substitutions) that automatically calculate match scores.
* **Interactive Pitch Visualization**: View 5-a-side team lineups on a graphical pitch with player names and positions.
* **EXCP Draft (NEW)**:
  * **FUT-Style Card Creator**: Design custom player cards with live previews. Supports multiple rarities (Gold, Silver, Bronze, Team of the Week), custom attributes, and photo uploads. Easily auto-fill stats from existing league players.
  * **5v5 Squad Builder**: Build dream teams using saved cards on an interactive pitch. Choose from multiple 5-a-side formations (1-2-1, 2-1-1, 1-1-2, 2-2, 1-3, 3-1).
* **Admin Panel**: Secured behind JWT authentication.
  * Full CRUD for Teams, Players, and Matches.
  * Bulk import players via CSV or Excel (.xlsx).
  * Live match event logging and lineup management.

## Tech Stack

* **Backend**: C#, ASP.NET Core 8.0 Web API
* **Architecture**: Clean Architecture (Domain, Application, Infrastructure, API)
* **Database**: Entity Framework Core with SQL Server LocalDB
* **Authentication**: JWT (JSON Web Tokens) with BCrypt password hashing
* **Frontend**: Vanilla HTML5, CSS3 (Premium Dark Theme with Glassmorphism), and JavaScript (SPA router)

## Getting Started

### Prerequisites
* .NET 8.0 SDK
* SQL Server LocalDB (installed with Visual Studio or SQL Server Express)

### Running the Application
1. Clone the repository and navigate to the root directory.
2. Run the application using the .NET CLI:
   ```bash
   dotnet run --project src/ExcpFootball.Api
   ```
3. The app will automatically seed the database on the first run with sample teams, players, and an admin account.
4. Open your browser and navigate to `http://localhost:5000`.

### Admin Access
To access the admin panel, log in with the default credentials:
* **Username**: `admin`
* **Password**: `admin123`

## Development Notes
* **Database Reset**: If you change the domain models, you may need to recreate the LocalDB instance as the app uses `EnsureCreated()`.
* **Frontend Caching**: The application uses cache-busting (e.g., `?v=3`) in `index.html` to ensure clients receive the latest JS/CSS updates.
* **Local Storage**: EXCP Draft cards and squads are persisted in the browser's `localStorage`.
