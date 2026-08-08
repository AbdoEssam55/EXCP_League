import os

base_dir = "c:/Users/Abdelrahman/Documents/vscode/antigrav/src"

files = {
    "ExcpFootball.Domain/Enums/Position.cs": """namespace ExcpFootball.Domain.Enums;
public enum Position { GK, CB, LW, RW, CM, CAM, ST }
""",
    "ExcpFootball.Domain/Enums/MatchEventType.cs": """namespace ExcpFootball.Domain.Enums;
public enum MatchEventType { Goal, Assist, YellowCard, RedCard, Substitution }
""",
    "ExcpFootball.Domain/Enums/MatchStatus.cs": """namespace ExcpFootball.Domain.Enums;
public enum MatchStatus { Scheduled, Live, Completed, Postponed }
""",
    "ExcpFootball.Domain/Enums/UserRole.cs": """namespace ExcpFootball.Domain.Enums;
public enum UserRole { Admin, Viewer }
""",
    "ExcpFootball.Domain/Entities/Season.cs": """using System.Collections.Generic;
namespace ExcpFootball.Domain.Entities;
public class Season {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public bool IsActive { get; set; }
    public ICollection<Match> Matches { get; set; } = new List<Match>();
}
""",
    "ExcpFootball.Domain/Entities/Team.cs": """using System.Collections.Generic;
namespace ExcpFootball.Domain.Entities;
public class Team {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string ShortName { get; set; } = string.Empty;
    public string? LogoPath { get; set; }
    public ICollection<Player> Players { get; set; } = new List<Player>();
}
""",
    "ExcpFootball.Domain/Entities/Player.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Domain.Entities;
public class Player {
    public int Id { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string? NickName { get; set; }
    public int Number { get; set; }
    public Position Position { get; set; }
    public int OverallRating { get; set; }
    public string? PhotoPath { get; set; }
    public bool IsReserve { get; set; }
    public bool IsCaptain { get; set; }
    public int TeamId { get; set; }
    public Team? Team { get; set; }
}
""",
    "ExcpFootball.Domain/Entities/Match.cs": """using System;
using System.Collections.Generic;
using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Domain.Entities;
public class Match {
    public int Id { get; set; }
    public int SeasonId { get; set; }
    public Season? Season { get; set; }
    public int HomeTeamId { get; set; }
    public Team? HomeTeam { get; set; }
    public int AwayTeamId { get; set; }
    public Team? AwayTeam { get; set; }
    public DateTime Date { get; set; }
    public MatchStatus Status { get; set; } = MatchStatus.Scheduled;
    public int HomeScore { get; set; }
    public int AwayScore { get; set; }
    public ICollection<MatchLineup> Lineups { get; set; } = new List<MatchLineup>();
    public ICollection<MatchEvent> Events { get; set; } = new List<MatchEvent>();
}
""",
    "ExcpFootball.Domain/Entities/MatchLineup.cs": """namespace ExcpFootball.Domain.Entities;
public class MatchLineup {
    public int Id { get; set; }
    public int MatchId { get; set; }
    public Match? Match { get; set; }
    public int PlayerId { get; set; }
    public Player? Player { get; set; }
    public int TeamId { get; set; }
    public Team? Team { get; set; }
    public float PositionX { get; set; }
    public float PositionY { get; set; }
    public string FormationPosition { get; set; } = string.Empty;
    public bool IsStarter { get; set; }
    public int MinutesPlayed { get; set; }
    public float Rating { get; set; }
}
""",
    "ExcpFootball.Domain/Entities/MatchEvent.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Domain.Entities;
public class MatchEvent {
    public int Id { get; set; }
    public int MatchId { get; set; }
    public Match? Match { get; set; }
    public int Minute { get; set; }
    public MatchEventType EventType { get; set; }
    public int PlayerId { get; set; }
    public Player? Player { get; set; }
    public int TeamId { get; set; }
    public Team? Team { get; set; }
    public int? AssistPlayerId { get; set; }
    public Player? AssistPlayer { get; set; }
}
""",
    "ExcpFootball.Domain/Entities/User.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Domain.Entities;
public class User {
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public UserRole Role { get; set; } = UserRole.Viewer;
}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Domain layer generated.")
