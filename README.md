# FantasyMLB

This the beginning of a REST API for use on a fantasy baseball site. More to come! (Currently v1.0)

## Use

As of now, the API structure looks like this:

```url
http://host:5000/api/v{version}/players/{playerID}/{yearID}/
```
Where ```playerID``` is a string containing the unique baseball-reference playerID and ```yearID``` is a string containing the year you wish to view.

### Endpoints

```
players/
```
Gives all unique playerIDs in the database.

```
players/{playerID}/
```
Gives all stats on record by year for the player with the corresponding playerID.

```
players/{playerID}/{yearID}/
```
Gives the player's stats for the year corresponding to yearID.



As said before, much more to come. This is a work in progress.
