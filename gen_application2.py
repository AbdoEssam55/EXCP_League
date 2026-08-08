import os

base_dir = "c:/Users/Abdelrahman/Documents/vscode/antigrav/src"

files = {
    # Services
    "ExcpFootball.Application/Services/TeamService.cs": """using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Teams;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class TeamService : ITeamService {
    private readonly ExcpFootballDbContext _context;
    public TeamService(ExcpFootballDbContext context) { _context = context; }
    public async Task<List<TeamDto>> GetAllAsync() => await _context.Teams.Select(t => new TeamDto { Id = t.Id, Name = t.Name, ShortName = t.ShortName, LogoPath = t.LogoPath }).ToListAsync();
    public async Task<TeamDto?> GetByIdAsync(int id) {
        var t = await _context.Teams.FindAsync(id);
        if (t == null) return null;
        return new TeamDto { Id = t.Id, Name = t.Name, ShortName = t.ShortName, LogoPath = t.LogoPath };
    }
    public async Task<TeamDto> CreateAsync(CreateTeamRequest request) {
        var team = new Team { Name = request.Name, ShortName = request.ShortName };
        _context.Teams.Add(team);
        await _context.SaveChangesAsync();
        return new TeamDto { Id = team.Id, Name = team.Name, ShortName = team.ShortName };
    }
    public async Task UpdateAsync(int id, UpdateTeamRequest request) {
        var team = await _context.Teams.FindAsync(id);
        if (team == null) throw new Exception("Not found");
        team.Name = request.Name;
        team.ShortName = request.ShortName;
        await _context.SaveChangesAsync();
    }
    public async Task DeleteAsync(int id) {
        var team = await _context.Teams.FindAsync(id);
        if (team != null) { _context.Teams.Remove(team); await _context.SaveChangesAsync(); }
    }
    public async Task<List<StandingsDto>> GetStandingsAsync(int seasonId) {
        var teams = await _context.Teams.ToListAsync();
        var matches = await _context.Matches.Where(m => m.SeasonId == seasonId && m.Status == ExcpFootball.Domain.Enums.MatchStatus.Completed).ToListAsync();
        var standings = teams.Select(t => new StandingsDto {
            TeamId = t.Id, TeamName = t.Name, LogoPath = t.LogoPath, Played = matches.Count(m => m.HomeTeamId == t.Id || m.AwayTeamId == t.Id),
            Won = matches.Count(m => (m.HomeTeamId == t.Id && m.HomeScore > m.AwayScore) || (m.AwayTeamId == t.Id && m.AwayScore > m.HomeScore)),
            Drawn = matches.Count(m => (m.HomeTeamId == t.Id || m.AwayTeamId == t.Id) && m.HomeScore == m.AwayScore),
            Lost = matches.Count(m => (m.HomeTeamId == t.Id && m.HomeScore < m.AwayScore) || (m.AwayTeamId == t.Id && m.AwayScore < m.HomeScore)),
            GoalsFor = matches.Where(m => m.HomeTeamId == t.Id).Sum(m => m.HomeScore) + matches.Where(m => m.AwayTeamId == t.Id).Sum(m => m.AwayScore),
            GoalsAgainst = matches.Where(m => m.HomeTeamId == t.Id).Sum(m => m.AwayScore) + matches.Where(m => m.AwayTeamId == t.Id).Sum(m => m.HomeScore)
        }).ToList();
        foreach (var s in standings) { s.GoalDifference = s.GoalsFor - s.GoalsAgainst; s.Points = s.Won * 3 + s.Drawn; }
        return standings.OrderByDescending(s => s.Points).ThenByDescending(s => s.GoalDifference).ThenByDescending(s => s.GoalsFor).ToList();
    }
    public async Task UpdateLogoAsync(int id, string logoPath) {
        var team = await _context.Teams.FindAsync(id);
        if (team != null) { team.LogoPath = logoPath; await _context.SaveChangesAsync(); }
    }
}""",
    "ExcpFootball.Application/Services/PlayerService.cs": """using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Players;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class PlayerService : IPlayerService {
    private readonly ExcpFootballDbContext _context;
    public PlayerService(ExcpFootballDbContext context) { _context = context; }
    public async Task<List<PlayerDto>> GetAllAsync() => await _context.Players.Include(p => p.Team).Select(p => new PlayerDto { Id = p.Id, FullName = p.FullName, NickName = p.NickName, Number = p.Number, Position = p.Position, OverallRating = p.OverallRating, PhotoPath = p.PhotoPath, IsReserve = p.IsReserve, IsCaptain = p.IsCaptain, TeamId = p.TeamId, TeamName = p.Team.Name }).ToListAsync();
    public async Task<PlayerDto?> GetByIdAsync(int id) {
        var p = await _context.Players.Include(x => x.Team).FirstOrDefaultAsync(x => x.Id == id);
        if (p == null) return null;
        return new PlayerDto { Id = p.Id, FullName = p.FullName, NickName = p.NickName, Number = p.Number, Position = p.Position, OverallRating = p.OverallRating, PhotoPath = p.PhotoPath, IsReserve = p.IsReserve, IsCaptain = p.IsCaptain, TeamId = p.TeamId, TeamName = p.Team!.Name };
    }
    public async Task<PlayerDto> CreateAsync(CreatePlayerRequest request) {
        var p = new Player { FullName = request.FullName, NickName = request.NickName, Number = request.Number, Position = request.Position, OverallRating = request.OverallRating, IsReserve = request.IsReserve, IsCaptain = request.IsCaptain, TeamId = request.TeamId };
        _context.Players.Add(p); await _context.SaveChangesAsync();
        return await GetByIdAsync(p.Id) ?? throw new Exception("Error");
    }
    public async Task UpdateAsync(int id, UpdatePlayerRequest request) {
        var p = await _context.Players.FindAsync(id);
        if (p == null) throw new Exception("Not found");
        p.FullName = request.FullName; p.NickName = request.NickName; p.Number = request.Number; p.Position = request.Position; p.OverallRating = request.OverallRating; p.IsReserve = request.IsReserve; p.IsCaptain = request.IsCaptain; p.TeamId = request.TeamId;
        await _context.SaveChangesAsync();
    }
    public async Task DeleteAsync(int id) {
        var p = await _context.Players.FindAsync(id);
        if (p != null) { _context.Players.Remove(p); await _context.SaveChangesAsync(); }
    }
    public async Task UpdatePhotoAsync(int id, string photoPath) {
        var p = await _context.Players.FindAsync(id);
        if (p != null) { p.PhotoPath = photoPath; await _context.SaveChangesAsync(); }
    }
}""",
    "ExcpFootball.Application/Services/MatchService.cs": """using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Domain.Enums;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Matches;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class MatchService : IMatchService {
    private readonly ExcpFootballDbContext _context;
    public MatchService(ExcpFootballDbContext context) { _context = context; }
    public async Task<List<MatchDto>> GetAllAsync() => await _context.Matches.Include(m => m.HomeTeam).Include(m => m.AwayTeam).Select(m => new MatchDto { Id = m.Id, SeasonId = m.SeasonId, HomeTeamId = m.HomeTeamId, HomeTeamName = m.HomeTeam.Name, HomeTeamLogo = m.HomeTeam.LogoPath, AwayTeamId = m.AwayTeamId, AwayTeamName = m.AwayTeam.Name, AwayTeamLogo = m.AwayTeam.LogoPath, Date = m.Date, Status = m.Status, HomeScore = m.HomeScore, AwayScore = m.AwayScore }).ToListAsync();
    public async Task<MatchDetailDto?> GetByIdAsync(int id) {
        var m = await _context.Matches.Include(x => x.HomeTeam).Include(x => x.AwayTeam).Include(x => x.Lineups).ThenInclude(l => l.Player).Include(x => x.Events).ThenInclude(e => e.Player).Include(x => x.Events).ThenInclude(e => e.AssistPlayer).FirstOrDefaultAsync(x => x.Id == id);
        if (m == null) return null;
        return new MatchDetailDto { Id = m.Id, SeasonId = m.SeasonId, HomeTeamId = m.HomeTeamId, HomeTeamName = m.HomeTeam!.Name, HomeTeamLogo = m.HomeTeam.LogoPath, AwayTeamId = m.AwayTeamId, AwayTeamName = m.AwayTeam!.Name, AwayTeamLogo = m.AwayTeam.LogoPath, Date = m.Date, Status = m.Status, HomeScore = m.HomeScore, AwayScore = m.AwayScore, Lineups = m.Lineups.Select(l => new MatchLineupDto { Id = l.Id, MatchId = l.MatchId, PlayerId = l.PlayerId, PlayerName = l.Player!.FullName, TeamId = l.TeamId, PositionX = l.PositionX, PositionY = l.PositionY, FormationPosition = l.FormationPosition, IsStarter = l.IsStarter, MinutesPlayed = l.MinutesPlayed, Rating = l.Rating }).ToList(), Events = m.Events.Select(e => new MatchEventDto { Id = e.Id, Minute = e.Minute, EventType = e.EventType, PlayerId = e.PlayerId, PlayerName = e.Player!.FullName, TeamId = e.TeamId, AssistPlayerId = e.AssistPlayerId, AssistPlayerName = e.AssistPlayer?.FullName }).ToList() };
    }
    public async Task<MatchDto> CreateAsync(CreateMatchRequest request) {
        var m = new Match { SeasonId = request.SeasonId, HomeTeamId = request.HomeTeamId, AwayTeamId = request.AwayTeamId, Date = request.Date, Status = MatchStatus.Scheduled };
        _context.Matches.Add(m); await _context.SaveChangesAsync();
        return new MatchDto { Id = m.Id, SeasonId = m.SeasonId, HomeTeamId = m.HomeTeamId, AwayTeamId = m.AwayTeamId, Date = m.Date, Status = m.Status };
    }
    public async Task UpdateAsync(int id, UpdateMatchRequest request) {
        var m = await _context.Matches.FindAsync(id);
        if (m == null) throw new Exception("Not found");
        m.SeasonId = request.SeasonId; m.HomeTeamId = request.HomeTeamId; m.AwayTeamId = request.AwayTeamId; m.Date = request.Date; m.Status = request.Status;
        await _context.SaveChangesAsync();
    }
    public async Task DeleteAsync(int id) {
        var m = await _context.Matches.FindAsync(id);
        if (m != null) { _context.Matches.Remove(m); await _context.SaveChangesAsync(); }
    }
    public async Task AddLineupsAsync(int matchId, List<CreateMatchLineupRequest> requests) {
        var m = await _context.Matches.Include(x => x.Lineups).FirstOrDefaultAsync(x => x.Id == matchId);
        if (m == null) throw new Exception("Not found");
        foreach(var req in requests) { m.Lineups.Add(new MatchLineup { MatchId = matchId, PlayerId = req.PlayerId, TeamId = req.TeamId, PositionX = req.PositionX, PositionY = req.PositionY, FormationPosition = req.FormationPosition, IsStarter = req.IsStarter }); }
        await _context.SaveChangesAsync();
    }
    public async Task AddEventAsync(int matchId, CreateMatchEventRequest request) {
        var m = await _context.Matches.Include(x => x.Events).FirstOrDefaultAsync(x => x.Id == matchId);
        if (m == null) throw new Exception("Not found");
        m.Events.Add(new MatchEvent { MatchId = matchId, Minute = request.Minute, EventType = request.EventType, PlayerId = request.PlayerId, TeamId = request.TeamId, AssistPlayerId = request.AssistPlayerId });
        if (request.EventType == MatchEventType.Goal) { if (request.TeamId == m.HomeTeamId) m.HomeScore++; else m.AwayScore++; }
        await _context.SaveChangesAsync();
    }
    public async Task RemoveEventAsync(int matchId, int eventId) {
        var m = await _context.Matches.Include(x => x.Events).FirstOrDefaultAsync(x => x.Id == matchId);
        if (m == null) throw new Exception("Not found");
        var ev = m.Events.FirstOrDefault(e => e.Id == eventId);
        if (ev != null) {
            if (ev.EventType == MatchEventType.Goal) { if (ev.TeamId == m.HomeTeamId) m.HomeScore--; else m.AwayScore--; }
            m.Events.Remove(ev); await _context.SaveChangesAsync();
        }
    }
}""",
    "ExcpFootball.Application/Services/SeasonService.cs": """using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Seasons;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class SeasonService : ISeasonService {
    private readonly ExcpFootballDbContext _context;
    public SeasonService(ExcpFootballDbContext context) { _context = context; }
    public async Task<List<SeasonDto>> GetAllAsync() => await _context.Seasons.Select(s => new SeasonDto { Id = s.Id, Name = s.Name, IsActive = s.IsActive }).ToListAsync();
    public async Task<SeasonDto?> GetActiveAsync() {
        var s = await _context.Seasons.FirstOrDefaultAsync(x => x.IsActive);
        return s == null ? null : new SeasonDto { Id = s.Id, Name = s.Name, IsActive = s.IsActive };
    }
}""",
    "ExcpFootball.Application/Services/StatsService.cs": """using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ExcpFootball.Domain.Enums;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Players;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class StatsService : IStatsService {
    private readonly ExcpFootballDbContext _context;
    public StatsService(ExcpFootballDbContext context) { _context = context; }
    public async Task<List<PlayerStatsDto>> GetTopScorersAsync(int seasonId, int count = 5) {
        var goals = await _context.MatchEvents.Include(e => e.Match).Include(e => e.Player).ThenInclude(p => p.Team)
            .Where(e => e.Match!.SeasonId == seasonId && e.EventType == MatchEventType.Goal)
            .GroupBy(e => e.PlayerId)
            .Select(g => new { PlayerId = g.Key, Goals = g.Count() })
            .OrderByDescending(g => g.Goals).Take(count).ToListAsync();
        var result = new List<PlayerStatsDto>();
        foreach (var g in goals) {
            var stats = await GetPlayerStatsAsync(g.PlayerId, seasonId);
            result.Add(stats);
        }
        return result.OrderByDescending(r => r.Goals).ToList();
    }
    public async Task<List<PlayerStatsDto>> GetTopAssistsAsync(int seasonId, int count = 5) {
        var assists = await _context.MatchEvents.Include(e => e.Match).Include(e => e.AssistPlayer).ThenInclude(p => p.Team)
            .Where(e => e.Match!.SeasonId == seasonId && e.EventType == MatchEventType.Goal && e.AssistPlayerId != null)
            .GroupBy(e => e.AssistPlayerId)
            .Select(g => new { PlayerId = g.Key.Value, Assists = g.Count() })
            .OrderByDescending(g => g.Assists).Take(count).ToListAsync();
        var result = new List<PlayerStatsDto>();
        foreach (var a in assists) {
            var stats = await GetPlayerStatsAsync(a.PlayerId, seasonId);
            result.Add(stats);
        }
        return result.OrderByDescending(r => r.Assists).ToList();
    }
    public async Task<PlayerStatsDto> GetPlayerStatsAsync(int playerId, int seasonId) {
        var p = await _context.Players.Include(x => x.Team).FirstOrDefaultAsync(x => x.Id == playerId);
        if (p == null) return new PlayerStatsDto();
        var events = await _context.MatchEvents.Include(e => e.Match).Where(e => e.Match!.SeasonId == seasonId && (e.PlayerId == playerId || e.AssistPlayerId == playerId)).ToListAsync();
        var appearances = await _context.MatchLineups.Include(l => l.Match).Where(l => l.Match!.SeasonId == seasonId && l.PlayerId == playerId).ToListAsync();
        return new PlayerStatsDto {
            PlayerId = p.Id, FullName = p.FullName, NickName = p.NickName, Number = p.Number, Position = p.Position, PhotoPath = p.PhotoPath, TeamName = p.Team!.Name,
            Goals = events.Count(e => e.PlayerId == playerId && e.EventType == MatchEventType.Goal),
            Assists = events.Count(e => e.AssistPlayerId == playerId && e.EventType == MatchEventType.Goal),
            YellowCards = events.Count(e => e.PlayerId == playerId && e.EventType == MatchEventType.YellowCard),
            RedCards = events.Count(e => e.PlayerId == playerId && e.EventType == MatchEventType.RedCard),
            Appearances = appearances.Count,
            MinutesPlayed = appearances.Sum(a => a.MinutesPlayed)
        };
    }
}""",
    "ExcpFootball.Application/Services/AuthService.cs": """using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using BCrypt.Net;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Domain.Enums;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Auth;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class AuthService : IAuthService {
    private readonly ExcpFootballDbContext _context;
    private readonly IConfiguration _config;
    public AuthService(ExcpFootballDbContext context, IConfiguration config) { _context = context; _config = config; }
    public async Task<LoginResponse> LoginAsync(LoginRequest request) {
        var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == request.Username);
        if (user == null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash)) throw new Exception("Invalid credentials");
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.ASCII.GetBytes(_config["JwtSettings:Key"]!);
        var tokenDescriptor = new SecurityTokenDescriptor {
            Subject = new ClaimsIdentity(new[] { new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()), new Claim(ClaimTypes.Name, user.Username), new Claim(ClaimTypes.Role, user.Role.ToString()) }),
            Expires = DateTime.UtcNow.AddMinutes(double.Parse(_config["JwtSettings:ExpiryInMinutes"] ?? "60")),
            Issuer = _config["JwtSettings:Issuer"], Audience = _config["JwtSettings:Audience"],
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
        };
        var token = tokenHandler.CreateToken(tokenDescriptor);
        return new LoginResponse { Token = tokenHandler.WriteToken(token), User = new UserDto { Id = user.Id, Username = user.Username, Role = user.Role.ToString() } };
    }
    public async Task<UserDto> RegisterAsync(RegisterRequest request) {
        if (await _context.Users.AnyAsync(u => u.Username == request.Username)) throw new Exception("Username exists");
        var role = Enum.Parse<UserRole>(request.Role);
        var user = new User { Username = request.Username, PasswordHash = BCrypt.Net.BCrypt.HashPassword(request.Password), Role = role };
        _context.Users.Add(user); await _context.SaveChangesAsync();
        return new UserDto { Id = user.Id, Username = user.Username, Role = user.Role.ToString() };
    }
    public async Task<UserDto?> GetCurrentUserAsync(string username) {
        var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
        if (user == null) return null;
        return new UserDto { Id = user.Id, Username = user.Username, Role = user.Role.ToString() };
    }
}""",
    "ExcpFootball.Application/Services/FileStorageService.cs": """using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using ExcpFootball.Application.Interfaces;
namespace ExcpFootball.Application.Services;
public class FileStorageService : IFileStorageService {
    private readonly string _basePath;
    public FileStorageService(IConfiguration config) { _basePath = config["FileStorage:BasePath"] ?? "wwwroot/uploads"; }
    public async Task<string> SaveFileAsync(Stream fileStream, string fileName, string folderName) {
        var folderPath = Path.Combine(_basePath, folderName);
        if (!Directory.Exists(folderPath)) Directory.CreateDirectory(folderPath);
        var uniqueName = $"{Guid.NewGuid()}_{fileName}";
        var filePath = Path.Combine(folderPath, uniqueName);
        using var stream = new FileStream(filePath, FileMode.Create);
        await fileStream.CopyToAsync(stream);
        return Path.Combine(folderName, uniqueName).Replace("\\", "/");
    }
    public void DeleteFile(string filePath) {
        var fullPath = Path.Combine(_basePath, filePath);
        if (File.Exists(fullPath)) File.Delete(fullPath);
    }
}""",
    "ExcpFootball.Application/Services/PlayerImportService.cs": """using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using ClosedXML.Excel;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Domain.Enums;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Infrastructure.Data;
namespace ExcpFootball.Application.Services;
public class PlayerImportService : IPlayerImportService {
    private readonly ExcpFootballDbContext _context;
    public PlayerImportService(ExcpFootballDbContext context) { _context = context; }
    public async Task ImportFromCsvAsync(Stream stream) {
        using var reader = new StreamReader(stream);
        var header = await reader.ReadLineAsync();
        var teams = await _context.Teams.ToListAsync();
        while (!reader.EndOfStream) {
            var line = await reader.ReadLineAsync();
            var values = line!.Split(',');
            await ProcessRow(values[0], values[1], int.Parse(values[2]), values[3], int.Parse(values[4]), values[5], teams);
        }
        await _context.SaveChangesAsync();
    }
    public async Task ImportFromExcelAsync(Stream stream) {
        using var workbook = new XLWorkbook(stream);
        var worksheet = workbook.Worksheet(1);
        var rows = worksheet.RangeUsed().RowsUsed().Skip(1);
        var teams = await _context.Teams.ToListAsync();
        foreach (var row in rows) {
            await ProcessRow(row.Cell(1).Value.ToString(), row.Cell(2).Value.ToString(), int.Parse(row.Cell(3).Value.ToString()), row.Cell(4).Value.ToString(), int.Parse(row.Cell(5).Value.ToString()), row.Cell(6).Value.ToString(), teams);
        }
        await _context.SaveChangesAsync();
    }
    private async Task ProcessRow(string name, string nickName, int number, string positionStr, int overall, string teamName, System.Collections.Generic.List<Team> teams) {
        var team = teams.FirstOrDefault(t => t.Name == teamName || t.ShortName == teamName);
        if (team == null) { team = new Team { Name = teamName, ShortName = teamName }; _context.Teams.Add(team); teams.Add(team); await _context.SaveChangesAsync(); }
        var position = Enum.Parse<Position>(positionStr);
        var player = await _context.Players.FirstOrDefaultAsync(p => p.FullName == name && p.TeamId == team.Id);
        if (player == null) { player = new Player { FullName = name, NickName = nickName, Number = number, Position = position, OverallRating = overall, TeamId = team.Id }; _context.Players.Add(player); }
        else { player.NickName = nickName; player.Number = number; player.Position = position; player.OverallRating = overall; }
    }
}""",
    
    # Validators
    "ExcpFootball.Application/Validators/CreatePlayerValidator.cs": """using FluentValidation;
using ExcpFootball.Application.DTOs.Players;
namespace ExcpFootball.Application.Validators;
public class CreatePlayerValidator : AbstractValidator<CreatePlayerRequest> {
    public CreatePlayerValidator() {
        RuleFor(x => x.FullName).NotEmpty();
        RuleFor(x => x.Number).GreaterThan(0);
        RuleFor(x => x.OverallRating).InclusiveBetween(1, 99);
    }
}""",
    "ExcpFootball.Application/Validators/CreateMatchValidator.cs": """using FluentValidation;
using ExcpFootball.Application.DTOs.Matches;
namespace ExcpFootball.Application.Validators;
public class CreateMatchValidator : AbstractValidator<CreateMatchRequest> {
    public CreateMatchValidator() {
        RuleFor(x => x.HomeTeamId).NotEmpty().NotEqual(x => x.AwayTeamId).WithMessage("Home and Away teams must be different");
        RuleFor(x => x.AwayTeamId).NotEmpty();
    }
}""",
    "ExcpFootball.Application/Validators/CreateMatchEventValidator.cs": """using FluentValidation;
using ExcpFootball.Application.DTOs.Matches;
namespace ExcpFootball.Application.Validators;
public class CreateMatchEventValidator : AbstractValidator<CreateMatchEventRequest> {
    public CreateMatchEventValidator() {
        RuleFor(x => x.Minute).GreaterThanOrEqualTo(0);
        RuleFor(x => x.PlayerId).NotEmpty();
    }
}""",
    "ExcpFootball.Application/Validators/LoginRequestValidator.cs": """using FluentValidation;
using ExcpFootball.Application.DTOs.Auth;
namespace ExcpFootball.Application.Validators;
public class LoginRequestValidator : AbstractValidator<LoginRequest> {
    public LoginRequestValidator() {
        RuleFor(x => x.Username).NotEmpty();
        RuleFor(x => x.Password).NotEmpty();
    }
}"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Application layer Services and Validators generated.")
