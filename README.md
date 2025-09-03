# ⚽ WOSO API
*Comprehensive Women's Football Data Platform*

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)](https://django-rest-framework-simplejwt.readthedocs.io)

---

> **"With women's football, the data just isn't there. While men's football analytics flourished with detailed stats and insights, women's football data remained scattered and incomplete. As someone passionate about both technology and women's sports, I built this API to bridge that gap. Every goal scored, every progressive pass made, every save - they all deserve to be measured, analyzed, and celebrated. This isn't just about numbers; it's about giving women's football the analytical foundation it deserves to grow, attract investment, and inspire the next generation of female athletes."**

---

## 🌟 Overview

**WOSO API** provides comprehensive football data specifically focused on women's leagues, with rich statistical analysis capabilities. Built for analysts, developers, journalists, and anyone passionate about women's football analytics.

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
https://wosoapi.com/
```

### 1. Register & Authenticate
```bash
# 1. Register new account
curl -X POST https://wosoapi.onrender.com/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'

# 2. Check email and click verification link

# 3. Get JWT tokens
curl -X POST https://wosoapi.onrender.com//token/ \
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
  https://wosoapi.onrender.com/leagues/<int:league_id>/clubs/

# Get all players in Arsenal Women
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
   https://wosoapi.onrender.com/clubs/<int:club_id>/players/

# Get top scorers
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://wosoapi.onrender.com/leagues/<int:league_id>/players/?ordering=-goals"
```

---

## 🔐 Authentication System

> **All endpoints require JWT authentication except registration and verification**

### Registration & Verification Flow

<details>
<summary><strong>POST</strong> /register/ - Register New User</summary>

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
<summary><strong>GET</strong> /verify/{uid}/{token}/ - Verify Email</summary>

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
<summary><strong>POST</strong> /resend/verify/ - Resend Verification Email</summary>

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
<summary><strong>POST</strong> /token/ - Obtain JWT Tokens</summary>

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

> 🔑 **Token Lifespan:** Access tokens are short-lived(2hours/120minutes), refresh tokens last longer(7 days).

</details>

<details>
<summary><strong>POST</strong> /token/refresh/ - Refresh Access Token</summary>

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



## ⚽ Football Data API

> **🏅 Data Attribution:** All football statistics provided by [FBref.com](https://fbref.com) - *Sports Reference* and its partners. FBref is the leading source for advanced football analytics and historical statistics. Please respect their terms of service when using this data.

> All endpoints require authentication: `Authorization: Bearer YOUR_ACCESS_TOKEN`

### 🌍 Countries & Leagues

<details>
<summary><strong>GET</strong> /countries/ - List All Countries</summary>

Get all countries with women's football leagues in the database.

**Response:**
```json
[
  {
    "id": "1",
    "name": "England", 
    "code": "ENG",
    "leagues_count": 1
  }
]
```

</details>

<details>
<summary><strong>GET</strong> /leagues/ - List All Leagues</summary>

Get all women's football leagues with basic information.

**Response:**
```json
[
  {
    "id": "1",
    "name": "Women's Super League",
    "country": "England",
    "total_clubs": 12
  }
]
```

*Data source: [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /leagues/{league_id}/seasons/ - League Seasons</summary>

Get all available seasons for a specific league.

**Example:** `/leagues/1/seasons/`

</details>

<details>
<summary><strong>GET</strong> /leagues/{league_id}/clubs/ - Clubs in League</summary>

Get all clubs in a specific league with current season performance.

**Example:** `/wosoapi/leagues/1/clubs/`

*All team statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /wosoapi/leagues/{league_id}/players/ - All League Players</summary>

Get all players across all clubs in a league with comprehensive statistics.

**Query Parameters:**
- `id` - Filter by player id
- `full_name`- Filter by full name
- `club` - Filter by club
- `fbref_id` - filter by fbref_id
- `ordering` - Sort by `id`, `full_name`, `club`

*Player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /leagues/{league_id}/goalkeepers/ - All League Goalkeepers</summary>

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

- `search` - Search by club name

</details>

<details>
<summary><strong>GET</strong> /clubs/{club_id}/ - Club Profile & Stats</summary>

Get comprehensive club information and detailed season statistics.

**Example:** `/clubs/1/`

**Response includes:**
- Club basic information

- Historical data (if available)


*All club statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /clubstats/ - All Club Statistics</summary>

Get statistical data for all clubs across all seasons.

**Query Parameters:**
- `season` - Filter by season (e.g., `2024/25`)
- `league` - Filter by league (e.g., `wsl`)
- `ordering` - Sort by field (e.g., `points`, `-goals_for`, `xg_for`)

**Response includes:** Goals for/against, xG, possession stats, passing stats, defensive stats, and more.

*Statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /clubs/{club_id}/players/ - Club Players</summary>

Get all players in a specific club with their comprehensive season statistics.

**Example:** `/wosoapi/clubs/arsenal-women/players/`

*Player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /clubs/{club_id}/goalkeepers/ - Club Goalkeepers</summary>

Get all goalkeepers in a specific club with specialized goalkeeper statistics.

*Goalkeeper statistics sourced from [FBref.com](https://fbref.com)*

</details>

### 👩‍⚽ Players

<details>
<summary><strong>GET</strong> /players/ - All Players</summary>

Get list of all players across all clubs and leagues.



**Response:**
```json
[
  {
    "player_id": "250",
    "full_name": "Mariona Caldentey",
    "club": "Arsenal", 
    "fbref_id":"4671156"

  }
]
```

</details>

<details>
<summary><strong>GET</strong> /playerstats/ - All Player Statistics</summary>

Get comprehensive statistical data for all players with advanced analytics.

**Query Parameters:**
- `season` - Filter by season
- `position` - Filter by position
- `minutes_played` - Minutes played
- `ordering` - Sort by stat (e.g., `goals`, `-xg`, `assists`, `-progressive_passes`)

**Response includes extensive FBref statistics:**
- **Basic:** matches_played, starts, minutes, goals, assists
- **Expected:** xg, xa, npxg, 
- **Shooting:** shots, shots_target, shots_creation_action
- **Passing:** passes_to_final_3rd,passes_to_pen_area
- **Progression:** prog_carries, carries_to_final_3rd, carries_to_pen_area
- **Defending:** tackles, interceptions, tackles_won
- **Discipline:** yellow_cards, red_cards, fouls_won,fouls_commited

*All player statistics sourced from [FBref.com](https://fbref.com)*

</details>

<details>
<summary><strong>GET</strong> /players/{player_id}/ - Player Profile</summary>

Get detailed player information and complete statistical history.

**Example:** `/wosoapi/players/`

**Response includes:**
- Personal information 


*Player data sourced from [FBref.com](https://fbref.com)*

</details>

### 🥅 Goalkeepers

<details>
<summary><strong>GET</strong> /goalkeepers/ - All Goalkeepers</summary>

Get list of all goalkeepers across leagues with specialized filtering.

**Query Parameters:**
- `club` - Filter by club
- `league` - Filter by league  
- `minutes` - Minutes played
- `ordering` - Sort by goalkeeper stats (e.g., `-save_percentage`, `goals_conceded`)

</details>

<details>
<summary><strong>GET</strong> /goalkeepers/{goalkeeper_id}/ - Goalkeeper Profile</summary>

Get detailed goalkeeper profile with specialized statistics and career history.

**Response includes:**
- **Shot Stopping:** saves, save_percentage, goals_against
- **Advanced Metrics:** post_shot_xg, 


*All goalkeeper statistics sourced from [FBref.com](https://fbref.com)*

</details>

---

## 📊 Complete API Reference

### 🌍 **Countries**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/countries/` | GET | Get all countries with women's football data |

### 🏆 **Leagues**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/leagues/` | GET | Get all leagues |
| `/leagues/{league_id}/seasons/` | GET | Get all seasons for a specific league |
| `/leagues/{league_id}/clubs/` | GET | Get all clubs in a specific league |
| `/leagues/{league_id}/players/` | GET | Get all players in clubs of a specific league |
| `/leagues/{league_id}/goalkeepers/` | GET | Get all goalkeepers in clubs of a specific league |

### 📅 **Seasons**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/seasons/` | GET | Get all seasons across all leagues |

### 🏟️ **Clubs**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/club/` | GET | Get all clubs |
| `/clubs/{club_id}/` | GET | Get details + stats of a specific club |
| `/clubstats/` | GET | Get all club stats (across seasons) |
| `/clubs/{club_id}/players/` | GET | Get all players (with stats) in a specific club |
| `/clubs/{club_id}/goalkeepers/` | GET | Get all goalkeepers (with stats) in a specific club |

### 👩‍⚽ **Players**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/players/` | GET | Get all players |
| `/players/stats/` | GET | Get all player stats (across seasons) |
| `/players/{player_id}/` | GET | Get details + stats of a specific player |

### 🧤 **Goalkeepers**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/goalkeepers/` | GET | Get all goalkeepers |
| `/goalkeepers/{goalkeeper_id}/` | GET | Get details + stats of a specific goalkeeper |

---

## 📈 Advanced Query Examples

### 🎯 Top Performers
```bash
# Top 10 goal scorers in WSL (2023/24, league filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&ordering=-goals&minutes_played__gte=500&limit=10

# Top 5 goal scorers in Arsenal Women (2023/24, league + club filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&player__club__name=Arsenal&ordering=-goals&limit=10

# Best passers by completion (all leagues, 2023/24)
GET /playerstats/?season=2023/24&position=MF&ordering=-passes_comp&minutes_played__gte=300

# Most progressive players in UWCL (2023/24, league filter)
GET /playerstats/?season=2023/24&player__club__league__code=UWCL&ordering=-prog_carries&minutes_played__gte=400

# Top 10 assist providers in Chelsea Women (2023/24, club filter)
GET /playerstats/?season=2023/24&player__club__name=Chelsea&ordering=-assists&limit=10

# Most minutes played in Arsenal Women (2023/24, league + club filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&player__club__name=Arsenal&ordering=-minutes_played&limit=10



```

### ⚡ Advanced Analytics
```bash
# Highest xG performers, forwards in WSL (2023/24, league filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&position=FW&ordering=-xg

# Underperforming strikers in UWCL (high xG but ≤2 goals, 2023/24, league filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&position=FW&ordering=-xg&goals__lte=2

# Best defensive midfielders in Arsenal Women (2023/24, league + club filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&player__club__name=Arsenal&position=MF&ordering=-tackles&minutes_played__gte=500

# Most ball-winning midfielders (global, tackles + interceptions, 2023/24)
GET /playerstats/?season=2023/24&position=MF&ordering=-tackles&ordering=-interceptions

# Best young forwards in WSL (under 23, 2023/24, league filter)
GET /playerstats/?season=2023/24&player__club__league__code=WSL&player__age__lte=23&position=FW&minutes_played__gte=300&ordering=-goals

# Ball-playing defenders in Barcelona Femení (2023/24, league + club filter)
GET /playerstats/?season=2023/24&player__club__league__code=UWCL&player__club__name=Barcelona&position=DF&ordering=-prog_carries&minutes_played__gte=700
```

### 🥅 Goalkeeper Analytics
```bash
# Best shot stoppers in WSL (2023/24, league filter)
GET /goalkeepers/?season=2023/24&player__club__league__code=WSL&ordering=-save_percentage&minutes_played__gte=450

# Goalkeepers with most clean sheets in Chelsea Women (2023/24, club filter)
GET /goalkeepers/?season=2023/24&player__club__name=Chelsea&ordering=-clean_sheets

# Goalkeepers preventing most goals vs xG in UWCL (2023/24, league filter)
GET /goalkeepers/?season=2023/24&player__club__league__code=UWCL&ordering=-psxg
# Best shot stoppers (2023/24)
GET /goalkeepers/?season=2023/24&ordering=-save_percentage&minutes_played__gte=450

# Most saves (2023/24)
GET /goalkeepers/?season=2023/24&ordering=-saves&limit=5

# Most clean sheets (2023/24)
GET /goalkeepers/?season=2023/24&ordering=-clean_sheets

# Preventing most goals vs xG (2023/24)
GET /goalkeepers/?season=2023/24&ordering=-psxg

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
- **Shooting:** shots, shots on target
- **Passing:**  progressive passes,   passes_to_pen_area, 
- **Ball Progression:** dribbles, carries_to_final_3rd, carries_to_pen_area, passes_to_final_3rd, prog_carries
- **Defending:** tackles, interceptions
- **Discipline:** yellow cards, red cards, fouls committed/won


**Goalkeeper-Specific Stats:**
- **Shot Stopping:** saves, save percentage, goals conceded
- **Advanced Metrics:** post-shot xG


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
response = requests.post('https://wosoapi.onrender.com/register/', json={
    'email': 'dev@example.com',
    'password': 'DevPass123!',
    'password_confirm': 'DevPass123!'
})

# 2. Verify email (check inbox)

# 3. Get tokens
response = requests.post('https://wosoapi.onrender.com//token/', json={
    'email': 'dev@example.com',
    'password': 'DevPass123!'
})

tokens = response.json()
access_token = tokens['access']

# 4. Make authenticated requests
headers = {'Authorization': f'Bearer {access_token}'}
players = requests.get('https://wosoapi.onrender.com/players/', headers=headers)
```

### 3. Common Patterns
```python
# Get top scorers
top_scorers = requests.get(
    'https://wosoapi.onrender.com/players/stats/?ordering=-goals&min_minutes=500',
    headers=headers
).json()

# Get Arsenal squad
arsenal_players = requests.get(
    'https://wosoapi.onrender.com//clubs/arsenal-women/players/',
    headers=headers  
).json()

# Get WSL goalkeepers by save percentage
best_keepers = requests.get(
    'https://wosoapi.onrender.com/leagues/wsl/goalkeepers/?ordering=-save_percentage',
    headers=headers
).json()
```

---

## 💡 Support & Contributing

**Questions or Issues?**
- 📧 Email: fasolamiracle001@gmail.com
- 🐦 Twitter: [@Justmimi___]
<!-- - 📚 Full Documentation: -->

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