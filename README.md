# ⚽ WOSO API
*Comprehensive Women's Football Data Platform*

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)](https://django-rest-framework-simplejwt.readthedocs.io)

---

> **"Growing up watching women's football, I noticed something missing - the data wasn't there. While men's football analytics flourished with detailed stats and insights, women's football data remained scattered and incomplete. As someone passionate about both technology and women's sports, I built this API to bridge that gap. Every goal scored, every progressive pass made, every save - they all deserve to be measured, analyzed, and celebrated. This isn't just about numbers; it's about giving women's football the analytical foundation it deserves to grow, attract investment, and inspire the next generation of female athletes."**

---

## 🌟 Overview

The **WOSO API** (Women's Sports Obsessed) provides comprehensive football data specifically focused on women's leagues, with rich statistical analysis capabilities. Built for analysts, developers, journalists, and anyone passionate about women's football analytics.

**🔥 Data Source:** All football statistics are sourced from [FBref.com](https://fbref.com) - the premier destination for football statistics and analytics. We are grateful to FBref for providing comprehensive women's football data that makes this API possible.

### ✨ Key Features
- 🔒 **Secure JWT Authentication** with email verification
- 📊 **Comprehensive Stats** including xG, xA, progressive passes, defensive actions
- 🏆 **Multi-League Support** starting with WSL (Women's Super League)
- ⚡ **High Performance** REST API built with Django + DRF
- 📈 **Advanced Analytics** designed for serious football analysis
- 🌍 **Developer Friendly** with detailed documentation and examples

### 🎯 Use Cases
- **Sports Analytics**: Build dashboards and predictive models
- **Media & Journalism**: Data-driven storytelling and match analysis  
- **Fantasy Football**: Create women's fantasy football platforms
- **Academic Research**: Study trends in women's football development
- **Fan Applications**: Enhance supporter experience with rich data

---

## 🚀 Quick Start

### Base URL
```
http://localhost:8000/wosoapi/
```

### 1. Register & Authenticate
```bash
# 1. Register new account
curl -X POST http://localhost:8000/wosoapi/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'

# 2. Check email and click verification link

# 3. Get JWT tokens
curl -X POST http://localhost:8000/wosoapi/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@example.com", 
    "password": "SecurePass123!"
  }'
```

### 2. Make API Calls
```bash
# Get all WSL clubs
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/wosoapi/leagues/wsl/clubs/

# Get all players in Arsenal Women
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/wosoapi/clubs/arsenal-women/players/

# Get top scorers
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:8000/wosoapi/players/stats/?ordering=-goals"
```

---

## 🔐 Authentication System

> **All endpoints require JWT authentication except registration and verification**

### Registration & Verification Flow

<details>
<summary><strong>POST</strong> /wosoapi/register/ - Register New User</summary>

Create a new user account. Account starts inactive until email verification.

**Request Body:**
```json
{
  "email": "analyst@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Success Response (201):**
```json
{
  "email": "analyst@example.com",
  "SUCCESS": "Now proceed to verify your email"
}
```

**Error Responses (400):**
```json
{"password": "Password mismatch"}
{"email": "This email is already in use."}
{"email": "Email cannot be empty."}
```

> 📧 **Important:** A verification email is automatically sent to the provided email address.

</details>

<details>
<summary><strong>GET</strong> /wosoapi/verify/{uid}/{token}/ - Verify Email</summary>

Activate user account using verification link from email.

**URL Parameters:**
- `uid` - Base64 encoded user ID
- `token` - Email verification token

**Success Response:**
- Renders `verify_success.html` template
- Account is activated (`is_active = True`)

**Failure Response:**
- Renders `verify_failed.html` template
- Shows "Invalid or expired token" message

**Important Notes:**
- ⏰ Verification tokens expire after **24 hours**
- 🗑️ Unverified accounts may be automatically deleted after **7 days**
- 🔄 Users can request new verification emails if needed

</details>

<details>
<summary><strong>POST</strong> /wosoapi/resend/verify/ - Resend Verification Email</summary>

Request new verification email for unverified accounts.

**Request Body:**
```json
{
  "email": "analyst@example.com"
}
```

**Success Response (200):**
```json
{
  "success": "Check your email to verify your account."
}
```

**Error Responses (400):**
```json
{"email": "This account is already verified. Please log in instead."}
{"email": "Account does not exist, sign up instead."}
```

</details>

### JWT Token Management

<details>
<summary><strong>POST</strong> /wosoapi/token/ - Obtain JWT Tokens</summary>

Get access and refresh tokens for authenticated API requests.

**Request Body:**
```json
{
  "email": "analyst@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response (401):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

> 🔑 **Token Lifespan:** Access tokens are short-lived, refresh tokens last longer. Check your Django settings for exact durations.

</details>

<details>
<summary><strong>POST</strong> /wosoapi/token/refresh/ - Refresh Access Token</summary>

Get new access token using valid refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

</details>

### Admin Operations

<details>
<summary><strong>GET</strong> /wosoapi/admin/delete/ - Delete Unverified Users (Admin Only)</summary>

Administrative endpoint to clean up unverified user accounts.

**Headers Required:**
```
Authorization: Bearer ADMIN_ACCESS_TOKEN
```

**Success Response (200):**
```json
{
  "message": "Successfully deleted 5 unverified users."
}
```

> ⚠️ **Admin Only:** Requires superuser permissions.

</details>

---

## ⚽ Football Data API

> **🏅 Data Attribution:** All football statistics provided by [FBref.com](https://fbref.com) - *Sports Reference* and its partners. FBref is the leading source for advanced football analytics and historical statistics. Please respect their terms of service when using this data.

> All endpoints require authentication: `Authorization: Bearer YOUR_ACCESS_TOKEN`

### 🌍 Countries & Leagues

<details>
<summary><strong>GET</strong> /wosoapi/countries/ - List All Countries</summary>

Get all countries with women's football leagues in the database.

**Response:**
```json
[
  {
    "id": "ENG",
    "name": "England", 
    "code": "ENG",
    "leagues_count": 1
  }
]
```

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/ - List All Leagues</summary>

Get all women's football leagues with basic information.

**Response:**
```json
[
  {
    "league_id": "wsl",
    "name": "Women's Super League",
    "country": "England",
    "current_season": "2024/25",
    "total_clubs": 12,
    "founded": 2011
  }
]
```

*Data source: [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/{league_id}/seasons/ - League Seasons</summary>

Get all available seasons for a specific league.

**Example:** `/wosoapi/leagues/wsl/seasons/`

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/{league_id}/clubs/ - Clubs in League</summary>

Get all clubs in a specific league with current season performance.

**Example:** `/wosoapi/leagues/wsl/clubs/`

*All team statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/{league_id}/players/ - All League Players</summary>

Get all players across all clubs in a league with comprehensive statistics.

**Query Parameters:**
- `position` - Filter by position (GK, DF, MF, FW)
- `nationality` - Filter by country
- `min_goals` - Minimum goals scored
- `min_minutes` - Minimum minutes played
- `ordering` - Sort by statistic (e.g., `-goals`, `xg`, `-assists`)

*Player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/{league_id}/goalkeepers/ - All League Goalkeepers</summary>

Get all goalkeepers across all clubs in a league with specialized goalkeeper statistics.

*Goalkeeper statistics sourced from [FBref.com](https://fbref.com)*

</details>

### 📅 Seasons

<details>
<summary><strong>GET</strong> /wosoapi/season/ - List All Seasons</summary>

Get all seasons across all leagues in the database.

</details>

### 🏟️ Clubs & Teams

<details>
<summary><strong>GET</strong> /wosoapi/club/ - List All Clubs</summary>

Get all clubs across all leagues and seasons.

**Query Parameters:**
- `league` - Filter by league
- `country` - Filter by country
- `search` - Search by club name

</details>

<details>
<summary><strong>GET</strong> /wosoapi/clubs/{club_id}/ - Club Profile & Stats</summary>

Get comprehensive club information and detailed season statistics.

**Example:** `/wosoapi/clubs/arsenal-women/`

**Response includes:**
- Club basic information
- Current season performance
- Historical data (if available)
- Squad summary statistics

*All club statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/club/stats/ - All Club Statistics</summary>

Get statistical data for all clubs across all seasons.

**Query Parameters:**
- `season` - Filter by season (e.g., `2024/25`)
- `league` - Filter by league (e.g., `wsl`)
- `ordering` - Sort by field (e.g., `points`, `-goals_for`, `xg_for`)

**Response includes:** Goals for/against, xG, possession stats, passing stats, defensive stats, and more.

*Statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/clubs/{club_id}/players/ - Club Players</summary>

Get all players in a specific club with their comprehensive season statistics.

**Example:** `/wosoapi/clubs/arsenal-women/players/`

**Query Parameters:**
- `position` - Filter by position
- `min_minutes` - Minimum minutes played
- `ordering` - Sort by statistic

*Player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/clubs/{club_id}/goalkeepers/ - Club Goalkeepers</summary>

Get all goalkeepers in a specific club with specialized goalkeeper statistics.

*Goalkeeper statistics sourced from [FBref.com](https://fbref.com)*

</details>

### 👩‍⚽ Players

<details>
<summary><strong>GET</strong> /wosoapi/players/ - All Players</summary>

Get list of all players across all clubs and leagues.

**Query Parameters:**
- `club` - Filter by club ID
- `league` - Filter by league
- `position` - Filter by position (GK, DF, MF, FW)
- `nationality` - Filter by country
- `search` - Search by player name
- `age_min` / `age_max` - Age range filter

**Response:**
```json
[
  {
    "player_id": "vivianne-miedema",
    "name": "Vivianne Miedema",
    "club": "Arsenal Women", 
    "position": "FW",
    "age": 27,
    "nationality": "Netherlands"
  }
]
```

</details>

<details>
<summary><strong>GET</strong> /wosoapi/players/stats/ - All Player Statistics</summary>

Get comprehensive statistical data for all players with advanced analytics.

**Query Parameters:**
- `season` - Filter by season
- `club` - Filter by club
- `position` - Filter by position
- `min_minutes` - Minimum minutes played
- `ordering` - Sort by stat (e.g., `goals`, `-xg`, `assists`, `-progressive_passes`)

**Response includes extensive FBref statistics:**
- **Basic:** matches_played, starts, minutes, goals, assists
- **Expected:** xg, xa, npxg, npxg_xa
- **Shooting:** shots, shots_on_target, shot_conversion
- **Passing:** pass_completion, progressive_passes, key_passes
- **Progression:** progressive_carries, carries_distance
- **Defending:** tackles, interceptions, blocks, clearances
- **Discipline:** yellow_cards, red_cards, fouls
- **Per 90 Stats:** goals_per90, assists_per90, xg_per90

*All player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/players/{player_id}/ - Player Profile</summary>

Get detailed player information and complete statistical history.

**Example:** `/wosoapi/players/sam-kerr/`

**Response includes:**
- Personal information and career details
- Current season performance
- Historical statistics
- Advanced analytics and per-90 metrics

*Player data sourced from [FBref.com](https://fbref.com)*

</details>

### 🥅 Goalkeepers

<details>
<summary><strong>GET</strong> /wosoapi/goalkeepers/ - All Goalkeepers</summary>

Get list of all goalkeepers across leagues with specialized filtering.

**Query Parameters:**
- `club` - Filter by club
- `league` - Filter by league  
- `nationality` - Filter by country
- `min_minutes` - Minimum minutes played
- `ordering` - Sort by goalkeeper stats (e.g., `-save_percentage`, `goals_against`)

</details>

<details>
<summary><strong>GET</strong> /wosoapi/goalkeepers/{goalkeeper_id}/ - Goalkeeper Profile</summary>

Get detailed goalkeeper profile with specialized statistics and career history.

**Response includes:**
- **Shot Stopping:** saves, save_percentage, goals_against
- **Advanced Metrics:** post_shot_xg, goals_prevented, shot_stopping_performance
- **Distribution:** launch_completion, pass_completion, distribution_distance
- **Penalty Stats:** penalties_faced, penalties_saved, penalty_save_rate
- **Sweeping Actions:** actions_outside_penalty_area

*All goalkeeper statistics sourced from [FBref.com](https://fbref.com)*

</details>

---

## 📊 Complete API Reference

### 🌍 **Countries**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/countries/` | GET | Get all countries with women's football data |

### 🏆 **Leagues**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/leagues/` | GET | Get all leagues |
| `/wosoapi/leagues/{league_id}/seasons/` | GET | Get all seasons for a specific league |
| `/wosoapi/leagues/{league_id}/clubs/` | GET | Get all clubs in a specific league |
| `/wosoapi/leagues/{league_id}/players/` | GET | Get all players in clubs of a specific league |
| `/wosoapi/leagues/{league_id}/goalkeepers/` | GET | Get all goalkeepers in clubs of a specific league |

### 📅 **Seasons**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/season/` | GET | Get all seasons across all leagues |

### 🏟️ **Clubs**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/club/` | GET | Get all clubs |
| `/wosoapi/clubs/{club_id}/` | GET | Get details + stats of a specific club |
| `/wosoapi/club/stats/` | GET | Get all club stats (across seasons) |
| `/wosoapi/clubs/{club_id}/players/` | GET | Get all players (with stats) in a specific club |
| `/wosoapi/clubs/{club_id}/goalkeepers/` | GET | Get all goalkeepers (with stats) in a specific club |

### 👩‍⚽ **Players**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/players/` | GET | Get all players |
| `/wosoapi/players/stats/` | GET | Get all player stats (across seasons) |
| `/wosoapi/players/{player_id}/` | GET | Get details + stats of a specific player |

### 🧤 **Goalkeepers**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wosoapi/goalkeepers/` | GET | Get all goalkeepers |
| `/wosoapi/goalkeepers/{goalkeeper_id}/` | GET | Get details + stats of a specific goalkeeper |

---

## 📈 Advanced Query Examples

### 🎯 Top Performers
```bash
# Top 10 goal scorers in WSL
GET /wosoapi/players/stats/?league=wsl&ordering=-goals&min_minutes=500

# Best passers by completion rate
GET /wosoapi/players/stats/?position=MF&ordering=-pass_completion&min_minutes=300

# Most progressive players
GET /wosoapi/players/stats/?ordering=-progressive_passes&min_minutes=400
```

### ⚡ Advanced Analytics
```bash
# Highest xG performers
GET /wosoapi/players/stats/?ordering=-xg&position=FW

# Most efficient finishers (goals vs xG)
GET /wosoapi/players/stats/?ordering=-goals&min_minutes=600

# Best defensive midfielders
GET /wosoapi/players/stats/?position=MF&ordering=-tackles&min_minutes=500
```

### 🥅 Goalkeeper Analytics
```bash
# Best shot stoppers
GET /wosoapi/goalkeepers/?ordering=-save_percentage&min_minutes=450

# Goalkeepers preventing most goals vs xG
GET /wosoapi/goalkeepers/?ordering=-goals_prevented
```

---

## 📊 Data Coverage

### 🏆 **Current Leagues**
- **Women's Super League (WSL)** - England's top women's football division
- *More leagues coming soon...*

### 📈 **Statistical Categories**

**Outfield Player Stats:**
- **Basic Performance:** matches, starts, minutes, goals, assists
- **Expected Stats:** xG, xA, npxG (non-penalty expected goals)
- **Shooting:** shots, shots on target, conversion rates
- **Passing:** completion rates, progressive passes, key passes
- **Ball Progression:** progressive carries, dribbles, carry distance
- **Defending:** tackles, interceptions, blocks, clearances, aerial duels
- **Discipline:** yellow cards, red cards, fouls committed/drawn
- **Per 90 Metrics:** All major stats normalized per 90 minutes

**Goalkeeper-Specific Stats:**
- **Shot Stopping:** saves, save percentage, goals against
- **Advanced Metrics:** post-shot xG, goals prevented
- **Distribution:** launch completion, pass accuracy, distribution distance  
- **Penalty Situations:** penalties faced, saved, save rate
- **Sweeping:** actions outside penalty area, defensive actions

*All statistics collected and calculated by [FBref.com](https://fbref.com)*

---

## 🛠️ Technical Specifications

**Backend Stack:**
- **Django 4.2+** - Web framework
- **Django REST Framework** - API framework  
- **Simple JWT** - JWT authentication
- **PostgreSQL** - Primary database
- **Email Backend** - SMTP email verification

**API Standards:**
- **REST Architecture** - Resource-based URLs
- **JSON Responses** - Consistent data format
- **HTTP Status Codes** - Standard response codes
- **JWT Authentication** - Secure token-based auth
- **Email Verification** - Account security
- **Rate Limiting** - Performance protection

---

## 🚨 Error Handling

### Standard HTTP Status Codes
- **200** - Success
- **201** - Created successfully  
- **400** - Bad request (validation errors)
- **401** - Unauthorized (invalid/missing token)
- **403** - Forbidden (insufficient permissions)
- **404** - Resource not found
- **429** - Rate limit exceeded
- **500** - Internal server error

### Error Response Format
```json
{
  "error": "Resource not found",
  "code": "PLAYER_NOT_FOUND", 
  "details": "Player with ID 'invalid-id' does not exist"
}
```

---

## ⚖️ Data Attribution & Legal

**🏅 Primary Data Source:** All football statistics are provided by [**FBref.com**](https://fbref.com), operated by *Sports Reference LLC*. FBref is the premier source for football statistics and advanced analytics.

**📋 Usage Terms:**
- This API aggregates publicly available football statistics
- All original data belongs to **FBref.com** and their data providers
- Users must comply with FBref's terms of service
- Commercial usage should acknowledge FBref as the data source
- This API is for educational, analytical, and development purposes

**🔗 Data Sources:**
- [FBref.com](https://fbref.com) - Primary football statistics
- *Sports Reference* network - Historical and current data
- Official league sources - Verification and supplementary data

---

## 🚀 Getting Started for Developers

### 1. Installation & Setup
```bash
# Clone repository
git clone <your-repo-url>
cd woso-api

# Install dependencies  
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 2. Authentication Flow
```python
import requests

# 1. Register
response = requests.post('http://localhost:8000/wosoapi/register/', json={
    'email': 'dev@example.com',
    'password': 'DevPass123!',
    'password_confirm': 'DevPass123!'
})

# 2. Verify email (check inbox)

# 3. Get tokens
response = requests.post('http://localhost:8000/wosoapi/token/', json={
    'email': 'dev@example.com',
    'password': 'DevPass123!'
})

tokens = response.json()
access_token = tokens['access']

# 4. Make authenticated requests
headers = {'Authorization': f'Bearer {access_token}'}
players = requests.get('http://localhost:8000/wosoapi/players/', headers=headers)
```

### 3. Common Patterns
```python
# Get top scorers
top_scorers = requests.get(
    'http://localhost:8000/wosoapi/players/stats/?ordering=-goals&min_minutes=500',
    headers=headers
).json()

# Get Arsenal squad
arsenal_players = requests.get(
    'http://localhost:8000/wosoapi/clubs/arsenal-women/players/',
    headers=headers  
).json()

# Get WSL goalkeepers by save percentage
best_keepers = requests.get(
    'http://localhost:8000/wosoapi/leagues/wsl/goalkeepers/?ordering=-save_percentage',
    headers=headers
).json()
```

---

## 💡 Support & Contributing

**Questions or Issues?**
- 📧 Email: api@woso.dev
- 🐦 Twitter: [@your_twitter_handle]
- 📚 Full Documentation: https://docs.woso.dev

**Data Attribution:**
Please acknowledge [**FBref.com**](https://fbref.com) when using this API's data in your applications, research, or publications.

**Contributing:**
This API is part of an ongoing mission to elevate women's football through better data accessibility. Contributions, feedback, and suggestions for additional leagues or features are always welcome.

---

## ⚠️ Important Notes

- **🔒 Security:** All endpoints (except auth) require valid JWT tokens
- **📊 Data Quality:** Statistics are sourced from [FBref.com](https://fbref.com) and updated regularly
- **⚡ Performance:** Responses are typically under 200ms
- **🔄 Updates:** Data refreshed weekly during season, daily during transfer windows
- **📝 Admin Rights:** Write operations restricted to superusers only
- **📧 Email Verification:** Required for all new accounts

---

*Built with ❤️ for women's football analytics | Data powered by [FBref.com](https://fbref.com)*