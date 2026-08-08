import os

base_dir = "c:/Users/Abdelrahman/Documents/vscode/antigrav/src"

files = {
    # DTOs - Auth
    "ExcpFootball.Application/DTOs/Auth/LoginRequest.cs": """namespace ExcpFootball.Application.DTOs.Auth;
public class LoginRequest {
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}""",
    "ExcpFootball.Application/DTOs/Auth/LoginResponse.cs": """namespace ExcpFootball.Application.DTOs.Auth;
public class LoginResponse {
    public string Token { get; set; } = string.Empty;
    public UserDto User { get; set; } = default!;
}""",
    "ExcpFootball.Application/DTOs/Auth/RegisterRequest.cs": """namespace ExcpFootball.Application.DTOs.Auth;
public class RegisterRequest {
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public string Role { get; set; } = "Viewer";
}""",
    "ExcpFootball.Application/DTOs/Auth/UserDto.cs": """namespace ExcpFootball.Application.DTOs.Auth;
public class UserDto {
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
}""",
    
    # DTOs - Teams
    "ExcpFootball.Application/DTOs/Teams/TeamDto.cs": """namespace ExcpFootball.Application.DTOs.Teams;
public class TeamDto {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string ShortName { get; set; } = string.Empty;
    public string? LogoPath { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Teams/CreateTeamRequest.cs": """namespace ExcpFootball.Application.DTOs.Teams;
public class CreateTeamRequest {
    public string Name { get; set; } = string.Empty;
    public string ShortName { get; set; } = string.Empty;
}""",
    "ExcpFootball.Application/DTOs/Teams/UpdateTeamRequest.cs": """namespace ExcpFootball.Application.DTOs.Teams;
public class UpdateTeamRequest {
    public string Name { get; set; } = string.Empty;
    public string ShortName { get; set; } = string.Empty;
}""",
    "ExcpFootball.Application/DTOs/Teams/StandingsDto.cs": """namespace ExcpFootball.Application.DTOs.Teams;
public class StandingsDto {
    public int TeamId { get; set; }
    public string TeamName { get; set; } = string.Empty;
    public string? LogoPath { get; set; }
    public int Played { get; set; }
    public int Won { get; set; }
    public int Drawn { get; set; }
    public int Lost { get; set; }
    public int GoalsFor { get; set; }
    public int GoalsAgainst { get; set; }
    public int GoalDifference { get; set; }
    public int Points { get; set; }
}""",

    # DTOs - Players
    "ExcpFootball.Application/DTOs/Players/PlayerDto.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Players;
public class PlayerDto {
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
    public string TeamName { get; set; } = string.Empty;
}""",
    "ExcpFootball.Application/DTOs/Players/CreatePlayerRequest.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Players;
public class CreatePlayerRequest {
    public string FullName { get; set; } = string.Empty;
    public string? NickName { get; set; }
    public int Number { get; set; }
    public Position Position { get; set; }
    public int OverallRating { get; set; }
    public bool IsReserve { get; set; }
    public bool IsCaptain { get; set; }
    public int TeamId { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Players/UpdatePlayerRequest.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Players;
public class UpdatePlayerRequest {
    public string FullName { get; set; } = string.Empty;
    public string? NickName { get; set; }
    public int Number { get; set; }
    public Position Position { get; set; }
    public int OverallRating { get; set; }
    public bool IsReserve { get; set; }
    public bool IsCaptain { get; set; }
    public int TeamId { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Players/PlayerStatsDto.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Players;
public class PlayerStatsDto {
    public int PlayerId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string? NickName { get; set; }
    public int Number { get; set; }
    public Position Position { get; set; }
    public string? PhotoPath { get; set; }
    public string TeamName { get; set; } = string.Empty;
    public int Goals { get; set; }
    public int Assists { get; set; }
    public int YellowCards { get; set; }
    public int RedCards { get; set; }
    public int Appearances { get; set; }
    public int MinutesPlayed { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Players/PlayerImportDto.cs": """namespace ExcpFootball.Application.DTOs.Players;
public class PlayerImportDto {
    public string PlayerName { get; set; } = string.Empty;
    public string? NickName { get; set; }
    public int Number { get; set; }
    public string Position { get; set; } = string.Empty;
    public int Overall { get; set; }
    public string Team { get; set; } = string.Empty;
}""",

    # DTOs - Matches
    "ExcpFootball.Application/DTOs/Matches/MatchDto.cs": """using System;
using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Matches;
public class MatchDto {
    public int Id { get; set; }
    public int SeasonId { get; set; }
    public int HomeTeamId { get; set; }
    public string HomeTeamName { get; set; } = string.Empty;
    public string? HomeTeamLogo { get; set; }
    public int AwayTeamId { get; set; }
    public string AwayTeamName { get; set; } = string.Empty;
    public string? AwayTeamLogo { get; set; }
    public DateTime Date { get; set; }
    public MatchStatus Status { get; set; }
    public int HomeScore { get; set; }
    public int AwayScore { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/CreateMatchRequest.cs": """using System;
namespace ExcpFootball.Application.DTOs.Matches;
public class CreateMatchRequest {
    public int SeasonId { get; set; }
    public int HomeTeamId { get; set; }
    public int AwayTeamId { get; set; }
    public DateTime Date { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/UpdateMatchRequest.cs": """using System;
using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Matches;
public class UpdateMatchRequest {
    public int SeasonId { get; set; }
    public int HomeTeamId { get; set; }
    public int AwayTeamId { get; set; }
    public DateTime Date { get; set; }
    public MatchStatus Status { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/MatchDetailDto.cs": """using System.Collections.Generic;
namespace ExcpFootball.Application.DTOs.Matches;
public class MatchDetailDto : MatchDto {
    public List<MatchLineupDto> Lineups { get; set; } = new();
    public List<MatchEventDto> Events { get; set; } = new();
}""",
    "ExcpFootball.Application/DTOs/Matches/MatchLineupDto.cs": """namespace ExcpFootball.Application.DTOs.Matches;
public class MatchLineupDto {
    public int Id { get; set; }
    public int MatchId { get; set; }
    public int PlayerId { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public int TeamId { get; set; }
    public float PositionX { get; set; }
    public float PositionY { get; set; }
    public string FormationPosition { get; set; } = string.Empty;
    public bool IsStarter { get; set; }
    public int MinutesPlayed { get; set; }
    public float Rating { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/CreateMatchLineupRequest.cs": """namespace ExcpFootball.Application.DTOs.Matches;
public class CreateMatchLineupRequest {
    public int PlayerId { get; set; }
    public int TeamId { get; set; }
    public float PositionX { get; set; }
    public float PositionY { get; set; }
    public string FormationPosition { get; set; } = string.Empty;
    public bool IsStarter { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/MatchEventDto.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Matches;
public class MatchEventDto {
    public int Id { get; set; }
    public int Minute { get; set; }
    public MatchEventType EventType { get; set; }
    public int PlayerId { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public int TeamId { get; set; }
    public int? AssistPlayerId { get; set; }
    public string? AssistPlayerName { get; set; }
}""",
    "ExcpFootball.Application/DTOs/Matches/CreateMatchEventRequest.cs": """using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Application.DTOs.Matches;
public class CreateMatchEventRequest {
    public int Minute { get; set; }
    public MatchEventType EventType { get; set; }
    public int PlayerId { get; set; }
    public int TeamId { get; set; }
    public int? AssistPlayerId { get; set; }
}""",
    
    # DTOs - Seasons
    "ExcpFootball.Application/DTOs/Seasons/SeasonDto.cs": """namespace ExcpFootball.Application.DTOs.Seasons;
public class SeasonDto {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public bool IsActive { get; set; }
}""",

    # DTOs - Dashboard
    "ExcpFootball.Application/DTOs/Dashboard/DashboardDto.cs": """using System.Collections.Generic;
using ExcpFootball.Application.DTOs.Teams;
using ExcpFootball.Application.DTOs.Players;
using ExcpFootball.Application.DTOs.Matches;
namespace ExcpFootball.Application.DTOs.Dashboard;
public class DashboardDto {
    public List<StandingsDto> Standings { get; set; } = new();
    public List<MatchDto> UpcomingMatches { get; set; } = new();
    public List<MatchDto> RecentResults { get; set; } = new();
    public List<PlayerStatsDto> TopScorers { get; set; } = new();
    public List<PlayerStatsDto> TopAssists { get; set; } = new();
}""",

    # Interfaces
    "ExcpFootball.Application/Interfaces/ITeamService.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Teams;
namespace ExcpFootball.Application.Interfaces;
public interface ITeamService {
    Task<List<TeamDto>> GetAllAsync();
    Task<TeamDto?> GetByIdAsync(int id);
    Task<TeamDto> CreateAsync(CreateTeamRequest request);
    Task UpdateAsync(int id, UpdateTeamRequest request);
    Task DeleteAsync(int id);
    Task<List<StandingsDto>> GetStandingsAsync(int seasonId);
    Task UpdateLogoAsync(int id, string logoPath);
}""",
    "ExcpFootball.Application/Interfaces/IPlayerService.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Players;
namespace ExcpFootball.Application.Interfaces;
public interface IPlayerService {
    Task<List<PlayerDto>> GetAllAsync();
    Task<PlayerDto?> GetByIdAsync(int id);
    Task<PlayerDto> CreateAsync(CreatePlayerRequest request);
    Task UpdateAsync(int id, UpdatePlayerRequest request);
    Task DeleteAsync(int id);
    Task UpdatePhotoAsync(int id, string photoPath);
}""",
    "ExcpFootball.Application/Interfaces/IMatchService.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Matches;
namespace ExcpFootball.Application.Interfaces;
public interface IMatchService {
    Task<List<MatchDto>> GetAllAsync();
    Task<MatchDetailDto?> GetByIdAsync(int id);
    Task<MatchDto> CreateAsync(CreateMatchRequest request);
    Task UpdateAsync(int id, UpdateMatchRequest request);
    Task DeleteAsync(int id);
    Task AddLineupsAsync(int matchId, List<CreateMatchLineupRequest> requests);
    Task AddEventAsync(int matchId, CreateMatchEventRequest request);
    Task RemoveEventAsync(int matchId, int eventId);
}""",
    "ExcpFootball.Application/Interfaces/ISeasonService.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Seasons;
namespace ExcpFootball.Application.Interfaces;
public interface ISeasonService {
    Task<List<SeasonDto>> GetAllAsync();
    Task<SeasonDto?> GetActiveAsync();
}""",
    "ExcpFootball.Application/Interfaces/IAuthService.cs": """using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Auth;
namespace ExcpFootball.Application.Interfaces;
public interface IAuthService {
    Task<LoginResponse> LoginAsync(LoginRequest request);
    Task<UserDto> RegisterAsync(RegisterRequest request);
    Task<UserDto?> GetCurrentUserAsync(string username);
}""",
    "ExcpFootball.Application/Interfaces/IFileStorageService.cs": """using System.IO;
using System.Threading.Tasks;
namespace ExcpFootball.Application.Interfaces;
public interface IFileStorageService {
    Task<string> SaveFileAsync(Stream fileStream, string fileName, string folderName);
    void DeleteFile(string filePath);
}""",
    "ExcpFootball.Application/Interfaces/IPlayerImportService.cs": """using System.IO;
using System.Threading.Tasks;
namespace ExcpFootball.Application.Interfaces;
public interface IPlayerImportService {
    Task ImportFromCsvAsync(Stream stream);
    Task ImportFromExcelAsync(Stream stream);
}""",
    "ExcpFootball.Application/Interfaces/IStatsService.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using ExcpFootball.Application.DTOs.Players;
namespace ExcpFootball.Application.Interfaces;
public interface IStatsService {
    Task<List<PlayerStatsDto>> GetTopScorersAsync(int seasonId, int count = 5);
    Task<List<PlayerStatsDto>> GetTopAssistsAsync(int seasonId, int count = 5);
    Task<PlayerStatsDto> GetPlayerStatsAsync(int playerId, int seasonId);
}"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Application layer DTOs and Interfaces generated.")
