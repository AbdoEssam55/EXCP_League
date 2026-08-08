import os

base_dir = "c:/Users/Abdelrahman/Documents/vscode/antigrav/src"

files = {
    # Controllers
    "ExcpFootball.Api/Controllers/AuthController.cs": """using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Auth;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase {
    private readonly IAuthService _authService;
    public AuthController(IAuthService authService) { _authService = authService; }
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request) => Ok(await _authService.LoginAsync(request));
    [HttpPost("register")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Register([FromBody] RegisterRequest request) => Ok(await _authService.RegisterAsync(request));
    [HttpGet("me")]
    [Authorize]
    public async Task<IActionResult> GetCurrentUser() {
        var user = await _authService.GetCurrentUserAsync(User.Identity!.Name!);
        if (user == null) return NotFound();
        return Ok(user);
    }
}""",
    "ExcpFootball.Api/Controllers/TeamsController.cs": """using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Teams;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class TeamsController : ControllerBase {
    private readonly ITeamService _teamService;
    private readonly IFileStorageService _fileStorage;
    public TeamsController(ITeamService teamService, IFileStorageService fileStorage) { _teamService = teamService; _fileStorage = fileStorage; }
    [HttpGet] public async Task<IActionResult> GetAll() => Ok(await _teamService.GetAllAsync());
    [HttpGet("{id}")] public async Task<IActionResult> GetById(int id) { var t = await _teamService.GetByIdAsync(id); return t == null ? NotFound() : Ok(t); }
    [HttpPost] [Authorize(Roles = "Admin")] public async Task<IActionResult> Create([FromBody] CreateTeamRequest request) => Ok(await _teamService.CreateAsync(request));
    [HttpPut("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Update(int id, [FromBody] UpdateTeamRequest request) { await _teamService.UpdateAsync(id, request); return NoContent(); }
    [HttpDelete("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Delete(int id) { await _teamService.DeleteAsync(id); return NoContent(); }
    [HttpPost("{id}/logo")] [Authorize(Roles = "Admin")] public async Task<IActionResult> UploadLogo(int id, IFormFile file) {
        if (file == null || file.Length == 0) return BadRequest();
        var path = await _fileStorage.SaveFileAsync(file.OpenReadStream(), file.FileName, "teams");
        await _teamService.UpdateLogoAsync(id, path);
        return Ok(new { Path = path });
    }
}""",
    "ExcpFootball.Api/Controllers/PlayersController.cs": """using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Players;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class PlayersController : ControllerBase {
    private readonly IPlayerService _playerService;
    private readonly IPlayerImportService _importService;
    private readonly IFileStorageService _fileStorage;
    public PlayersController(IPlayerService playerService, IPlayerImportService importService, IFileStorageService fileStorage) { _playerService = playerService; _importService = importService; _fileStorage = fileStorage; }
    [HttpGet] public async Task<IActionResult> GetAll() => Ok(await _playerService.GetAllAsync());
    [HttpGet("{id}")] public async Task<IActionResult> GetById(int id) { var p = await _playerService.GetByIdAsync(id); return p == null ? NotFound() : Ok(p); }
    [HttpPost] [Authorize(Roles = "Admin")] public async Task<IActionResult> Create([FromBody] CreatePlayerRequest request) => Ok(await _playerService.CreateAsync(request));
    [HttpPut("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Update(int id, [FromBody] UpdatePlayerRequest request) { await _playerService.UpdateAsync(id, request); return NoContent(); }
    [HttpDelete("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Delete(int id) { await _playerService.DeleteAsync(id); return NoContent(); }
    [HttpPost("{id}/photo")] [Authorize(Roles = "Admin")] public async Task<IActionResult> UploadPhoto(int id, IFormFile file) {
        if (file == null || file.Length == 0) return BadRequest();
        var path = await _fileStorage.SaveFileAsync(file.OpenReadStream(), file.FileName, "players");
        await _playerService.UpdatePhotoAsync(id, path);
        return Ok(new { Path = path });
    }
    [HttpPost("import")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Import(IFormFile file) {
        if (file == null || file.Length == 0) return BadRequest();
        if (file.FileName.EndsWith(".csv")) await _importService.ImportFromCsvAsync(file.OpenReadStream());
        else if (file.FileName.EndsWith(".xlsx")) await _importService.ImportFromExcelAsync(file.OpenReadStream());
        else return BadRequest("Invalid format");
        return Ok();
    }
}""",
    "ExcpFootball.Api/Controllers/MatchesController.cs": """using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Matches;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class MatchesController : ControllerBase {
    private readonly IMatchService _matchService;
    public MatchesController(IMatchService matchService) { _matchService = matchService; }
    [HttpGet] public async Task<IActionResult> GetAll() => Ok(await _matchService.GetAllAsync());
    [HttpGet("{id}")] public async Task<IActionResult> GetById(int id) { var m = await _matchService.GetByIdAsync(id); return m == null ? NotFound() : Ok(m); }
    [HttpPost] [Authorize(Roles = "Admin")] public async Task<IActionResult> Create([FromBody] CreateMatchRequest request) => Ok(await _matchService.CreateAsync(request));
    [HttpPut("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Update(int id, [FromBody] UpdateMatchRequest request) { await _matchService.UpdateAsync(id, request); return NoContent(); }
    [HttpDelete("{id}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> Delete(int id) { await _matchService.DeleteAsync(id); return NoContent(); }
    [HttpPost("{id}/lineups")] [Authorize(Roles = "Admin")] public async Task<IActionResult> AddLineups(int id, [FromBody] List<CreateMatchLineupRequest> requests) { await _matchService.AddLineupsAsync(id, requests); return NoContent(); }
    [HttpPost("{id}/events")] [Authorize(Roles = "Admin")] public async Task<IActionResult> AddEvent(int id, [FromBody] CreateMatchEventRequest request) { await _matchService.AddEventAsync(id, request); return NoContent(); }
    [HttpDelete("{id}/events/{eventId}")] [Authorize(Roles = "Admin")] public async Task<IActionResult> RemoveEvent(int id, int eventId) { await _matchService.RemoveEventAsync(id, eventId); return NoContent(); }
}""",
    "ExcpFootball.Api/Controllers/SeasonsController.cs": """using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class SeasonsController : ControllerBase {
    private readonly ISeasonService _seasonService;
    private readonly ITeamService _teamService;
    private readonly IStatsService _statsService;
    public SeasonsController(ISeasonService seasonService, ITeamService teamService, IStatsService statsService) { _seasonService = seasonService; _teamService = teamService; _statsService = statsService; }
    [HttpGet] public async Task<IActionResult> GetAll() => Ok(await _seasonService.GetAllAsync());
    [HttpGet("{id}/standings")] public async Task<IActionResult> GetStandings(int id) => Ok(await _teamService.GetStandingsAsync(id));
    [HttpGet("{id}/top-scorers")] public async Task<IActionResult> GetTopScorers(int id) => Ok(await _statsService.GetTopScorersAsync(id));
    [HttpGet("{id}/top-assists")] public async Task<IActionResult> GetTopAssists(int id) => Ok(await _statsService.GetTopAssistsAsync(id));
}""",
    "ExcpFootball.Api/Controllers/DashboardController.cs": """using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ExcpFootball.Application.Interfaces;
using ExcpFootball.Application.DTOs.Dashboard;
namespace ExcpFootball.Api.Controllers;
[ApiController]
[Route("api/[controller]")]
public class DashboardController : ControllerBase {
    private readonly ISeasonService _seasonService;
    private readonly ITeamService _teamService;
    private readonly IMatchService _matchService;
    private readonly IStatsService _statsService;
    public DashboardController(ISeasonService seasonService, ITeamService teamService, IMatchService matchService, IStatsService statsService) {
        _seasonService = seasonService; _teamService = teamService; _matchService = matchService; _statsService = statsService;
    }
    [HttpGet] public async Task<IActionResult> GetDashboardData() {
        var season = await _seasonService.GetActiveAsync();
        if (season == null) return NotFound("No active season");
        var standings = await _teamService.GetStandingsAsync(season.Id);
        var matches = await _matchService.GetAllAsync();
        var topScorers = await _statsService.GetTopScorersAsync(season.Id);
        var topAssists = await _statsService.GetTopAssistsAsync(season.Id);
        var dashboard = new DashboardDto {
            Standings = standings,
            UpcomingMatches = matches.Where(m => m.SeasonId == season.Id && m.Status == Domain.Enums.MatchStatus.Scheduled).OrderBy(m => m.Date).ToList(),
            RecentResults = matches.Where(m => m.SeasonId == season.Id && m.Status == Domain.Enums.MatchStatus.Completed).OrderByDescending(m => m.Date).ToList(),
            TopScorers = topScorers,
            TopAssists = topAssists
        };
        return Ok(dashboard);
    }
}""",
    "ExcpFootball.Api/Middleware/ExceptionHandlingMiddleware.cs": """using System;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
namespace ExcpFootball.Api.Middleware;
public class ExceptionHandlingMiddleware {
    private readonly RequestDelegate _next;
    public ExceptionHandlingMiddleware(RequestDelegate next) { _next = next; }
    public async Task InvokeAsync(HttpContext httpContext) {
        try { await _next(httpContext); }
        catch (Exception ex) { await HandleExceptionAsync(httpContext, ex); }
    }
    private Task HandleExceptionAsync(HttpContext context, Exception exception) {
        context.Response.ContentType = "application/json";
        context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
        var result = JsonSerializer.Serialize(new { error = exception.Message });
        return context.Response.WriteAsync(result);
    }
}"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Api layer Controllers and Middleware generated.")
