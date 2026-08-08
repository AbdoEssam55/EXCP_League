import os

base_dir = "c:/Users/Abdelrahman/Documents/vscode/antigrav/src"

files = {
    # Data Layer
    "ExcpFootball.Infrastructure/Data/ExcpFootballDbContext.cs": """using Microsoft.EntityFrameworkCore;
using ExcpFootball.Domain.Entities;
namespace ExcpFootball.Infrastructure.Data;
public class ExcpFootballDbContext : DbContext {
    public ExcpFootballDbContext(DbContextOptions<ExcpFootballDbContext> options) : base(options) { }
    public DbSet<Season> Seasons { get; set; } = null!;
    public DbSet<Team> Teams { get; set; } = null!;
    public DbSet<Player> Players { get; set; } = null!;
    public DbSet<Match> Matches { get; set; } = null!;
    public DbSet<MatchLineup> MatchLineups { get; set; } = null!;
    public DbSet<MatchEvent> MatchEvents { get; set; } = null!;
    public DbSet<User> Users { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder builder) {
        base.OnModelCreating(builder);
        
        builder.Entity<Match>()
            .HasOne(m => m.HomeTeam)
            .WithMany()
            .HasForeignKey(m => m.HomeTeamId)
            .OnDelete(DeleteBehavior.Restrict);
            
        builder.Entity<Match>()
            .HasOne(m => m.AwayTeam)
            .WithMany()
            .HasForeignKey(m => m.AwayTeamId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<MatchLineup>()
            .HasOne(ml => ml.Match)
            .WithMany(m => m.Lineups)
            .HasForeignKey(ml => ml.MatchId)
            .OnDelete(DeleteBehavior.Cascade);
            
        builder.Entity<MatchLineup>()
            .HasOne(ml => ml.Player)
            .WithMany()
            .HasForeignKey(ml => ml.PlayerId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<MatchEvent>()
            .HasOne(me => me.Match)
            .WithMany(m => m.Events)
            .HasForeignKey(me => me.MatchId)
            .OnDelete(DeleteBehavior.Cascade);
            
        builder.Entity<MatchEvent>()
            .HasOne(me => me.Player)
            .WithMany()
            .HasForeignKey(me => me.PlayerId)
            .OnDelete(DeleteBehavior.Restrict);
            
        builder.Entity<MatchEvent>()
            .HasOne(me => me.AssistPlayer)
            .WithMany()
            .HasForeignKey(me => me.AssistPlayerId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}""",
    "ExcpFootball.Infrastructure/Data/DataSeeder.cs": """using System;
using System.Linq;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using ExcpFootball.Domain.Entities;
using ExcpFootball.Domain.Enums;
namespace ExcpFootball.Infrastructure.Data;
public static class DataSeeder {
    public static void SeedData(this IApplicationBuilder app) {
        using var scope = app.ApplicationServices.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ExcpFootballDbContext>();
        context.Database.EnsureCreated();

        if (!context.Users.Any()) {
            context.Users.Add(new User { Username = "admin", PasswordHash = BCrypt.Net.BCrypt.HashPassword("admin123"), Role = UserRole.Admin });
            context.SaveChanges();
        }

        if (!context.Seasons.Any()) {
            var season = new Season { Name = "Season 1 2026/2027", IsActive = true };
            context.Seasons.Add(season);
            context.SaveChanges();
            
            var t1 = new Team { Name = "Backend Development", ShortName = "BE" };
            var t2 = new Team { Name = "Mobile Development", ShortName = "MD" };
            context.Teams.AddRange(t1, t2);
            context.SaveChanges();
            
            var p1 = new Player { FullName = "Mohamed Hamed", NickName = "الجناح الخارق", Number = 8, Position = Position.LW, OverallRating = 91, TeamId = t1.Id };
            var p2 = new Player { FullName = "Abdelrahman Abo Auf", NickName = "Aufinho", Number = 7, Position = Position.CAM, OverallRating = 93, IsCaptain = true, TeamId = t1.Id };
            var p3 = new Player { FullName = "Mostafa", Number = 10, Position = Position.RW, OverallRating = 90, TeamId = t1.Id };
            var p4 = new Player { FullName = "Ibrahim Salama", NickName = "ibrahimavic", Number = 1, Position = Position.GK, OverallRating = 85, TeamId = t1.Id };
            var p5 = new Player { FullName = "Amr Elmenbawy", NickName = "menbo", Number = 6, Position = Position.CM, OverallRating = 92, TeamId = t1.Id };
            var p6 = new Player { FullName = "Abdelrahman Essam", Number = 9, Position = Position.ST, OverallRating = 80, IsReserve = true, TeamId = t1.Id };
            var p7 = new Player { FullName = "Hisham", NickName = "H", Number = 4, Position = Position.RW, OverallRating = 95, TeamId = t1.Id };
            
            var p8 = new Player { FullName = "Magdy", Number = 8, Position = Position.RW, OverallRating = 90, IsCaptain = true, TeamId = t2.Id };
            var p9 = new Player { FullName = "Mostfa Zain", Number = 7, Position = Position.CAM, OverallRating = 87, TeamId = t2.Id };
            var p10 = new Player { FullName = "Amr Elhafy", Number = 10, Position = Position.LW, OverallRating = 89, TeamId = t2.Id };
            var p11 = new Player { FullName = "Anas Taha", Number = 2, Position = Position.CB, OverallRating = 50, TeamId = t2.Id };
            var p12 = new Player { FullName = "Mamoud Reda", Number = 1, Position = Position.GK, OverallRating = 71, TeamId = t2.Id };
            var p13 = new Player { FullName = "Sanad", Number = 12, Position = Position.GK, OverallRating = 70, IsReserve = true, TeamId = t2.Id };
            var p14 = new Player { FullName = "Nour", Number = 5, Position = Position.ST, OverallRating = 70, IsReserve = true, TeamId = t2.Id };
            
            context.Players.AddRange(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14);
            context.SaveChanges();
            
            var match1 = new Match { SeasonId = season.Id, HomeTeamId = t1.Id, AwayTeamId = t2.Id, Date = DateTime.Now.AddDays(-2), Status = MatchStatus.Completed, HomeScore = 2, AwayScore = 1 };
            var match2 = new Match { SeasonId = season.Id, HomeTeamId = t2.Id, AwayTeamId = t1.Id, Date = DateTime.Now.AddDays(5), Status = MatchStatus.Scheduled, HomeScore = 0, AwayScore = 0 };
            context.Matches.AddRange(match1, match2);
            context.SaveChanges();
            
            var e1 = new MatchEvent { MatchId = match1.Id, Minute = 15, EventType = MatchEventType.Goal, PlayerId = p2.Id, AssistPlayerId = p5.Id, TeamId = t1.Id };
            var e2 = new MatchEvent { MatchId = match1.Id, Minute = 45, EventType = MatchEventType.Goal, PlayerId = p8.Id, TeamId = t2.Id };
            var e3 = new MatchEvent { MatchId = match1.Id, Minute = 80, EventType = MatchEventType.Goal, PlayerId = p1.Id, AssistPlayerId = p2.Id, TeamId = t1.Id };
            context.MatchEvents.AddRange(e1, e2, e3);
            context.SaveChanges();
        }
    }
}"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Infrastructure layer DataSeeder and DbContext generated.")
