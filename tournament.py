#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random

MAXROUNDS = [(2,1),(4,2),(6,3),(8,3),(10,4),(12,4),(14,4),(16,4)]

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname='tournament'")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM matches"
    cursor.execute(query)
    query = "UPDATE currentgame SET matches = 0, wins = 0"
    cursor.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM currentgame"
    cursor.execute(query)
    db.commit()
    db.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM currentgame"
    cursor.execute(query)
    result = cursor.fetchone()
    players = result[0]
    print(players)
    db.close()
    return players
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's first name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    answer = raw_input("Is this an existing player? [yN]")
    if answer.lower() != "y":
    	query = "INSERT INTO players(name) VALUES (%s)"
    	cursor.execute(query,(name,))
    	db.commit()
    query = "SELECT ID FROM players WHERE name = %s"
    cursor.execute(query,(name,))
    result = cursor.fetchone()
    player_id = result[0]
    query = "INSERT INTO currentgame(ID) VALUES (%s)"
    cursor.execute(query,(player_id,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    standings = []
    
    query = "SELECT cg.ID, p.name, cg.wins, cg.matches FROM currentgame AS cg, players AS p WHERE cg.ID = p.ID ORDER BY cg.wins DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
    	standings.append((row[0],row[1],row[2],row[3]))
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
		    
    query = "INSERT INTO matches(player1,player2,winnerID) VALUES (%s, %s, %s)"
    cursor.execute(query,(winner,loser,winner))
    
    query = "SELECT wins, matches FROM currentgame WHERE ID = (%s)"
    cursor.execute(query,(winner,))
    result = cursor.fetchone()
    winnerwins = result[0] + 1
    winnermatches = result[1] + 1
    
    query = "UPDATE currentgame SET wins = %s, matches = %s WHERE ID = (%s)"
    cursor.execute(query,(winnerwins, winnermatches, winner))
    
    query = "SELECT matches FROM currentgame WHERE ID = (%s)"
    cursor.execute(query,(loser,))
    result = cursor.fetchone()
    losermatches = result[0] + 1
    
    query = "UPDATE currentgame SET matches = %s WHERE ID = (%s)"
    cursor.execute(query,(losermatches,loser))
    
    db.commit()
    db.close() 
 	
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairings = []
    matched = []
    counter = 1
    
    for row in standings:
    	if row[0] not in matched:
    		competitor = standings[counter][0]
    		pairings.append((row[0],row[1],competitor,standings[counter][1]))
    		matched.append(row[0])
    		matched.append(competitor)
    	counter += 1
    
    return pairings
    
def runTournament():
	"""Handles the rounds of a tournament, returns the winner
	
	Returns:
		id: An integer which contains the ID of the winner
		name: name of the winner
		wins: number of wins
		matches: number of matches
	"""
	rounds = 1
	db = connect()
	cursor = db.cursor()
	playercount = countPlayers()
	match = 1
	
	for row in MAXROUNDS:
		if playercount == row[0]:
			rounds = row[1]
			break
	
	counter = 0
	while counter < rounds:
		pairings = swissPairings()
		for row in pairings:
			winner = random.randint(1, 2)
			if winner == 1:
				loser = 2
				winner = 0
			else:
				loser = 0
				winner = 2
			reportMatch(row[winner],row[loser])
			print("Match " + str(match) + " winner: " + row[winner + 1] + ". Loser: " + row[loser + 1])
			match += 1
		counter += 1
	
	finalresults = playerStandings()
	winner = finalresults[0]
	return winner
	
def setupTournament():
	"""Handles setting up a new tournament and registering the players for it
	
	Assumes an even number of players will be entered but doesn't check for it.
	"""
	db = connect()
	cursor = db.cursor()
	
	while raw_input("Do you want to register a player in the tournament? (type a lowercase 'y' to do so) ") == "y":
		name = raw_input("What is the player's name? ")
		registerPlayer(name)
	
	raw_input("\nGetting ready to start the tournament. Press 'Enter' to begin.")
	winner = runTournament()
	
	print("\nThe winner is " + winner[1] + " with an ID of " + str(winner[0]) + " who won " + str(winner[2]) + " out of " + str(winner[2]) + " matches.")
	standings = playerStandings()
	counter = 0
	print("\nFinal Results:")
	print("------------------------------------------")
	for row in standings:
		print(row[1] + ", ID: " + str(row[0]) + ", won " + str(row[2]) + " of " + str(row[3]) + " matches")
	
	query = "INSERT INTO tournaments(winnerID) VALUES (%s) RETURNING tournamentID"
	cursor.execute(query,(winner[0],))
	result = cursor.fetchall()
	tournamentID = result[0][0]
	db.commit()
	print("\nResults of tournament with ID " + str(tournamentID) + " have been recorded.")
	
	deleteMatches()
	deletePlayers()
	db.close()

setupTournament()
while raw_input("\nWould you like to run another tournament?(enter a lowercase 'y' to do so) ") == "y":
	setupTournament()
	
print("\nThank you for using the Tournament software, have a good day.")