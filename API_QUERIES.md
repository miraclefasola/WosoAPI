# API Query Guide

This document explains how to construct API queries for the Wosostat API and what responses to expect.

## Base URL
All API endpoints start with: `https://wosostat/api`

## Authentication
All requests (except auth endpoints) require a JWT token in the header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Query Parameters

### Filtering
Most endpoints support filtering using field lookups:
- `field__exact` - Exact match
- `field__icontains` - Case-insensitive contains
- `field__gte` - Greater than or equal
- `field__lte` - Less than or equal
- `field__range` - Range of values

### Ordering
Use `ordering` parameter to sort results:
- `ordering=field` - Ascending order
- `ordering=-field` - Descending order

### Search
Use `search` parameter for text search across multiple fields.

### Pagination
- Default page size: 10 items
- Use `limit` parameter to control page size
- Use `offset` parameter to skip items

## Endpoint Examples

### Countries
```http
GET /api/countries/
```
Returns all countries with women's football data.

**Query Parameters:**
- `name__icontains` - Filter by country name
- `code` - Filter by country code
- `ordering` - Sort by `id`, `name`, `code`

### Leagues
```http
GET /api/leagues/
```
Returns all leagues with basic information.

**Query Parameters:**
- `name__icontains` - Filter by league name
- `country__name__icontains` - Filter by country name
- `code` - Filter by league code
- `total_clubs__gte` - Minimum number of clubs
- `ordering` - Sort by `id`, `name`, `country__name`, `total_clubs`

### League Seasons
```http
GET /api/leagues/{league_id}/seasons/
```
Returns all seasons for a specific league.

### League Clubs
```http
GET /api/leagues/{league_id}/clubs/
```
Returns all clubs in a specific league with current season performance.

**Query Parameters:**
- `club__name__icontains` - Filter by club name
- `season__season` - Filter by season
- `league_position__lte` - Maximum league position
- `points_won__gte` - Minimum points won
- `ordering` - Sort by `league_position`, `points_won`, `goals_scored`, etc.

### League Players
```http
GET /api/leagues/{league_id}/players/
```
Returns all players across all clubs in a league with comprehensive statistics.

**Query Parameters:**
- `player__full_name__icontains` - Filter by player name
- `club__name` - Filter by club name
- `position` - Filter by position (`FW`, `MF`, `DF`)
- `season__season` - Filter by season
- `minutes_played__gte` - Minimum minutes played
- `age__lte` - Maximum age
- `goals__gte` - Minimum goals scored
- `ordering` - Sort by any stat field

### League Goalkeepers
```http
GET /api/leagues/{league_id}/goalkeepers/
```
Returns all goalkeepers across all clubs in a league with specialized goalkeeper statistics.

**Query Parameters:**
- `player__full_name__icontains` - Filter by goalkeeper name
- `club__name` - Filter by club name
- `season__season` - Filter by season
- `minutes_played__gte` - Minimum minutes played
- `save_percentage__gte` - Minimum save percentage
- `clean_sheets__gte` - Minimum clean sheets
- `ordering` - Sort by goalkeeper stats

### Seasons
```http
GET /api/seasons/
```
Returns all seasons across all leagues.

**Query Parameters:**
- `season` - Filter by season (e.g., `2023/24`)
- `league__name__icontains` - Filter by league name
- `ordering` - Sort by `season`, `league__name`

### All Clubs
```http
GET /api/clubs/
```
Returns list of all clubs across all leagues and seasons.

**Query Parameters:**
- `name__icontains` - Filter by club name
- `fbref_id` - Filter by FBref ID
- `stadium__icontains` - Filter by stadium name
- `search` - Search across name and stadium fields
- `ordering` - Sort by `name`, `fbref_id`

### Club Detail
```http
GET /api/clubs/{club_id}/
```
Returns comprehensive club information and detailed season statistics.

**Query Parameters:**
- `season__season` - Filter by season
- `league_position__lte` - Maximum league position
- `ordering` - Sort by season or performance metrics

### Club Statistics
```http
GET /api/clubstats/
```
Returns statistical data for all clubs across all seasons.

**Query Parameters:**
- `club__name__icontains` - Filter by club name
- `season__season` - Filter by season
- `league__name__icontains` - Filter by league name
- `points_won__gte` - Minimum points won
- `goals_scored__gte` - Minimum goals scored
- `xg_created__gte` - Minimum expected goals created
- `ordering` - Sort by any statistical field

### Club Players
```http
GET /api/clubs/{club_id}/players/
```
Returns all players in a specific club with their comprehensive season statistics.

### Club Goalkeepers
```http
GET /api/clubs/{club_id}/goalkeepers/
```
Returns all goalkeepers in a specific club with specialized goalkeeper statistics.

### All Players
```http
GET /api/players/
```
Returns list of all players across all clubs and leagues.

**Query Parameters:**
- `full_name__icontains` - Filter by player name
- `fbref_id` - Filter by FBref ID
- `nationality__icontains` - Filter by nationality
- `age__gte` - Minimum age
- `age__lte` - Maximum age
- `ordering` - Sort by `full_name`, `age`, `nationality`

### Player Statistics
```http
GET /api/playerstats/
```
Returns comprehensive statistical data for all players with advanced analytics.

**Query Parameters:**
- `player__full_name__icontains` - Filter by player name
- `club__name__icontains` - Filter by club name
- `league__code` - Filter by league code (e.g., `WSL`)
- `season__season` - Filter by season (e.g., `2023/24`)
- `position` - Filter by position (`FW`, `MF`, `DF`)
- `age__gte` / `age__lte` - Filter by age range
- `minutes_played__gte` - Minimum minutes played
- `goals__gte` - Minimum goals scored
- `assists__gte` - Minimum assists
- `xg__gte` - Minimum expected goals
- `tackles__gte` - Minimum tackles made
- `ordering` - Sort by any statistical field

### All Goalkeepers
```http
GET /api/goalkeepers/
```
Returns list of all goalkeepers across leagues with specialized filtering.

**Query Parameters:**
- `player__full_name__icontains` - Filter by goalkeeper name
- `club__name__icontains` - Filter by club name
- `league__code` - Filter by league code
- `season__season` - Filter by season
- `minutes_played__gte` - Minimum minutes played
- `save_percentage__gte` - Minimum save percentage
- `goals_conceded__lte` - Maximum goals conceded
- `clean_sheets__gte` - Minimum clean sheets
- `psxg__gte` - Minimum post-shot expected goals
- `ordering` - Sort by goalkeeper statistics

## Example Queries

### Top Scorers in WSL
```http
GET /api/playerstats/?league__code=WSL&ordering=-goals&minutes_played__gte=500
```

### Arsenal Players in 2023/24 Season
```http
GET /api/playerstats/?club__name=Arsenal&season__season=2023/24
```

### Best Passers by Progressive Passes
```http
GET /api/playerstats/?ordering=-prog_passes&minutes_played__gte=300
```

### Top Goalkeepers by Save Percentage
```http
GET /api/goalkeepers/?ordering=-save_percentage&minutes_played__gte=450
```

### Young Forwards Under 23
```http
GET /api/playerstats/?age__lte=23&position=FW&minutes_played__gte=300&ordering=-goals
```

### Defensive Midfielders with Most Tackles
```http
GET /api/playerstats/?position=MF&ordering=-tackles&minutes_played__gte=500
```

### Players with Most Progressive Carries
```http
GET /api/playerstats/?ordering=-prog_carries&minutes_played__gte=400
```

### Best Shot Creation Players
```http
GET /api/playerstats/?ordering=-shots_creation_action&minutes_played__gte=500
```

### Goalkeepers with Most Clean Sheets
```http
GET /api/goalkeepers/?ordering=-clean_sheets&season__season=2023/24
```

### Players by Expected Goals Performance
```http
GET /api/playerstats/?ordering=-xg_performance&minutes_played__gte=500
```

### Most Disciplined Players (Fewest Cards)
```http
GET /api/playerstats/?ordering=yellow_card&minutes_played__gte=800
```

### Players with Most Ball Recoveries
```http
GET /api/playerstats/?ordering=-ball_recoveries&minutes_played__gte=600
```

### Goalkeepers Preventing Most Goals vs Expected
```http
GET /api/goalkeepers/?ordering=-psxg_performance&minutes_played__gte=450
```

### Most Active Sweeper Keepers
```http
GET /api/goalkeepers/?ordering=-sweeper_action_per90&minutes_played__gte=450
```

## Response Format

All successful responses return JSON data with the following structure:

```json
{
  "count": 100,
  "next": "https://wosostat/endpoint/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "field1": "value1",
      "field2": "value2"
    }
  ]
}
```

## Field Lookup Reference

### Available Lookups
- `exact` - Exact match (default if no lookup specified)
- `icontains` - Case-insensitive substring match
- `gte` - Greater than or equal to
- `gt` - Greater than
- `lte` - Less than or equal to
- `lt` - Less than
- `range` - Between two values (comma-separated)
- `in` - Match any value in a list (comma-separated)

### Examples
```http
# Exact match
GET /api/players/?full_name=Mariona Caldentey

# Case-insensitive contains
GET /api/players/?full_name__icontains=mari

# Age range
GET /api/players/?age__range=20,25

# Goals greater than or equal to 5
GET /api/playerstats/?goals__gte=5
```

## Common Filter Combinations

### High-Performing Forwards
```http
GET /api/playerstats/?position=FW&goals__gte=5&xg__gte=4.0&minutes_played__gte=500&ordering=-goals
```

### Defensive Specialists
```http
GET /api/playerstats/?position=DF&tackles__gte=20&interceptions__gte=15&minutes_played__gte=800&ordering=-tackles
```

### Creative Midfielders
```http
GET /api/playerstats/?position=MF&assists__gte=3&shots_creation_action__gte=20&prog_passes__gte=30&ordering=-assists
```

### Reliable Goalkeepers
```http
GET /api/goalkeepers/?save_percentage__gte=70.0&clean_sheets__gte=5&minutes_played__gte=900&ordering=-save_percentage
```

## Error Responses

Common error responses include:

**400: Bad Request (validation errors)**
```json
{
  "detail": "Invalid filter field or value"
}
```

**401: Unauthorized (invalid/missing token)**
```json
{
  "detail": "Given token not valid for any token type"
}
```

**403: Forbidden (insufficient permissions)**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404: Not Found (resource doesn't exist)**
```json
{
  "detail": "Not found."
}
```


## Performance Tips

1. **Use Specific Filters**: More specific queries return faster
2. **Limit Results**: Use `limit` parameter for better performance
3. **Index-Friendly Filters**: Use exact matches when possible
4. **Minimum Thresholds**: Use `minutes_played__gte` to filter out bench players
5. **Single Sort Field**: Use one `ordering` parameter for optimal performance
