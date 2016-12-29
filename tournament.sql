-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create the database
CREATE DATABASE tournament;
\c tournament

-- create the the table for each unique player as they join a tournament
-- * ID is unique and primary key
-- * lastName is the player's last name, doesn't have to be unique, can't be empty
-- * firstName is the player's first name, doesn't have to be unique, can't be empty
-- * totalWins is how many tournaments they've won, defaults to 0
CREATE TABLE players(
	ID serial,
	lastName varchar(40) NOT NULL,
	firstName varchar(40) NOT NULL,
	totalWins int DEFAULT (0),
	PRIMARY KEY(ID)
);

-- create the table to store each tournament so we can track multiple tournaments
-- * TournamentID will be unique and primary key
-- * Timestamp is when the tournament was won and recorded here
-- * WinnerID is the player's ID that won the tournament and maps to players.ID
-- initial insert will just populate the tournaentID field, later updated with winnerID and timestamp
CREATE TABLE tournaments(
	tournamentID serial,
	t_timestamp timestamp,
	winnerID int references players(ID),
	PRIMARY KEY(tournamentID)
);

-- create the table of players for the current tournament and their current wins in rounds
-- * ID is the player ID and maps to players.ID
-- * wins is how many rounds they've won, defaults to 0
CREATE TABLE currentgame(
	ID int references players(ID) UNIQUE NOT NULL,
	wins int DEFAULT (0),
	PRIMARY KEY(ID)
);

-- creates table to track matches in the tournament so a player doesn't fight another player more than once
-- * player1 is the ID of one player and maps to currentgame.ID (to ensure they're enrolled in the game)
-- * player2 is the ID of one player and maps to currentgame.ID and make sure they're not playing themselves
CREATE TABLE matchups(
	player1 int references currentgame(ID) NOT NULL,
	player2 int references currentgame(ID) NOT NULL CHECK (player2 != player1),
	PRIMARY KEY(player1, player2)
);

-- create table to track the matches in the current tournament
-- * matchID is the unique ID of the match
-- * player1 is one of the players in the match, maps to currentgame.ID
-- * player2 is one of the players in the match, maps to currentgame.ID and can't be the same as player1
-- * winnerID is the ID of the winner of the round, maps to currentgame.ID and has to be either player1 or player2
-- * round is the round the match occurs in
CREATE TABLE matches(
	matchID serial,
	player1 int references currentgame(ID) NOT NULL,
	player2 int references currentgame(ID) NOT NULL CHECK (player2 != player1),
	winnerID int references currentgame(ID) CHECK (winnerID = player1 OR winnerID = player2),
	t_round int NOT NULL DEFAULT 1,
	PRIMARY KEY(matchID)
);