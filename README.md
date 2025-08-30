# ⚡ WOSO API Documentation

This API provides football data (countries, leagues, clubs, players, goalkeepers) with JWT-based authentication and email verification.

---

## 🔐 Authentication API

<details>
<summary>Register New User</summary>

**POST /auth/register/**

| Field             | Type   | Required |
|------------------|--------|---------|
| email            | string | ✅      |
| password         | string | ✅      |
| password_confirm | string | ✅      |

**Success Response (201):**
```json
{
  "email": "user@example.com",
  "SUCCESS": "Now proceed to verify your email"
}
Errors (400):

json
Copy code
{"password": "Password mismatch"}
{"email": "This email is already in use."}
A verification email is sent after registration.

</details> <details> <summary>Verify Email</summary>
GET /auth/verify/{uid}/{token}/

Activates the user account if token is valid.

Renders verify_success.html or verify_failed.html.

Notes:

Links expire after 24 hours.

Accounts unverified after 7 days may be purged.

</details> <details> <summary>Resend Verification Email</summary>
POST /auth/resend/verify

Request:

json
Copy code
{
  "email": "user@example.com"
}
Success (200):

json
Copy code
{"success": "Check your email to verify your account."}
Errors (400):

json
Copy code
{"email": "This account is already verified. Please log in instead."}
{"email": "Account does not exist, sign up instead."}
</details> <details> <summary>Obtain JWT Token</summary>
POST /auth/token/

Request:

json
Copy code
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
Success:

json
Copy code
{
  "refresh": "...",
  "access": "..."
}
Failure:

json
Copy code
{"detail": "No active account found with the given credentials"}
</details> <details> <summary>Refresh JWT Token</summary>
POST /auth/token/refresh/

Request:

json
Copy code
{
  "refresh": "..."
}
Response:

json
Copy code
{
  "access": "new_access_token_here"
}
</details>
⚽ Football Data API
<details> <summary>Countries</summary>
Endpoint	Method	Description
/countries/	GET	List all countries

</details> <details> <summary>Leagues</summary>
Endpoint	Method	Description
/leagues/	GET	List all leagues
/leagues/{league_id}/seasons/	GET	List seasons in a specific league
/leagues/{league_id}/clubs/	GET	List clubs in a league
/leagues/{league_id}/players/	GET	List players in all clubs of a league
/leagues/{league_id}/goalkeepers/	GET	List goalkeepers in all clubs of a league

</details> <details> <summary>Seasons</summary>
Endpoint	Method	Description
/season/	GET	List all seasons

</details> <details> <summary>Clubs</summary>
Endpoint	Method	Description
/club/	GET	List all clubs
/clubs/{club_id}/	GET	Details + stats of a specific club
/club/stats/	GET	All club stats across seasons
/clubs/{club_id}/players/	GET	Players + stats in a club
/clubs/{club_id}/goalkeepers/	GET	Goalkeepers + stats in a club

</details> <details> <summary>Players</summary>
Endpoint	Method	Description
/players/	GET	List all players
/players/stats/	GET	All player stats
/players/{player_id}/	GET	Details + stats of a player

</details> <details> <summary>Goalkeepers</summary>
Endpoint	Method	Description
/goalkeepers/	GET	List all goalkeepers
/goalkeepers/{goalkeeper_id}/	GET	Details + stats of a goalkeeper

</details> ```