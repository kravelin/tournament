# tournament
final project for Intro to Programming Udacity course

file structure:
* tournament.sql contains the DATABASE schema and commands to create the database
* tournament.py contains the functions for managing tournaments
* tournament_test.py contains test cases for testing a tournament

To verify the test cases use `python tournament_test.py`

To run the program normally use `python tournament.py`

- NOTE: All Yes / No prompts should use a lowercase 'Y' or 'N'
- You will first be prompted to register a player
-- Enter the user's name
-- You will then be asked if this is a new player in your system
- You will be prompted to register another player. Keep doing this until you have all players.
- NOTE: The system only supports even numbers of players from 2 to 16, please keep this in mind
- You will then be prompted to hit 'Enter' when all players have been registered.
- The system will then run through matches declaring the winner of each round, using swiss pairing.
- At the end of the tournament the winner and final counts will be displayed.
- The tournament winner will be recorded and you will be given the tournament ID.
- You will then be asked if you wish to run another tournament or not.
- All players who take part in a tournament will be saved and considered existing players for later tournaments.
