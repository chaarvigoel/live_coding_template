# Multi-Sport Design Considerations

Supporting teams and players across multiple sports, where player attributes vary by sport, requires careful schema and API design.

---

## 1. Variable Player Attributes by Sport

| Sport   | Shared Attributes      | Sport-Specific Attributes                          |
|---------|------------------------|----------------------------------------------------|
| Baseball| firstName, lastName, weight, height | battingAvg, ERA, position (pitcher/outfielder)     |
| Soccer  | firstName, lastName, weight, height | goals, assists, yellowCards                        |
| Basketball | firstName, lastName, weight, height | pointsPerGame, rebounds, position                  |

**Core problem:** A single fixed schema cannot represent all sports cleanly.

---

## 2. Design Options

### Option A: EAV (Entity-Attribute-Value)

```
players: id, firstName, lastName, team_id, sport_id
player_attributes: player_id, attribute_key, attribute_value
```

- **Pros:** Fully flexible, add new attributes without migrations
- **Cons:** Poor query performance, no type safety, hard to index

### Option B: JSONB / Flexible Column

```
players: id, firstName, lastName, team_id, sport_id, attributes (JSONB)
```

- **Pros:** Flexible, some DBs support indexing on JSON paths
- **Cons:** No enforced schema per sport, validation lives in app logic

### Option C: Sport-Specific Tables

```
baseball_players: id, ...common..., batting_avg, era, position
soccer_players: id, ...common..., goals, assists, yellow_cards
```

- **Pros:** Strong typing, clear schema per sport
- **Cons:** Many tables, duplication of common fields, harder to query “all players”

### Option D: Shared Base + Sport Extensions (Recommended)

```
sports: id, name (baseball, soccer, basketball)
teams: id, name, sport_id (FK)
players: id, firstName, lastName, weight, height, team_id (FK)
baseball_stats: player_id, batting_avg, era, ...
soccer_stats: player_id, goals, assists, ...
basketball_stats: player_id, points_per_game, rebounds, ...
```

- **Pros:** Common player/team model, sport-specific stats in separate tables, easy to add new sports
- **Cons:** Requires a `sport_id` on teams and routing logic to the correct stats table

---

## 3. Recommendations

1. **Add `sport` or `sport_id` to teams**  
   Each team belongs to one sport. Players inherit sport via team.

2. **Use polymorphic stats tables**  
   Keep `batting_stats`, `fielding_stats`, `pitching_stats` for baseball. Add `soccer_stats`, `basketball_stats`, etc. Query the right table based on the team’s sport.

3. **API design**  
   - `GET /v1/teams` with `?sport=baseball`  
   - `GET /v1/players/{id}` returns common fields; optionally `?include=stats` to add sport-specific stats  
   - Or: `GET /v1/players/{id}/stats` returns the appropriate stats based on the player’s team sport

4. **Validation**  
   Define per-sport Pydantic models or validators. Reject invalid combinations (e.g. `battingAvg` for a soccer player).

5. **Extensibility**  
   Use a registry: `SPORT_STATS_HANDLERS = {"baseball": BaseballStats, "soccer": SoccerStats}` so adding a sport means adding a handler, not changing core logic.

---

## 4. Summary

- Use **shared core** (players, teams, managers) with **sport-specific stats tables**
- Tie teams to a sport; players get sport context via team
- Use **polymorphic API responses** or separate stats endpoints
- Add **per-sport validation** to keep data consistent
