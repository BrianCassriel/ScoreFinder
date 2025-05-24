# ScoreFinder
CPSC 408 Final Project - A Discord application to interface with a database of music scores.

Landon Kauer
Brian Cassriel
05/23/2025
Final Project
CPSC 408

### A description of any known compile or runtime errors, or code limitations
N/A

### A list of all references used to complete the assignment
Geeks for geeks
stackoverflow
chatgpt for help with discord.py syntax and functionality

### Instructions
Open a terminal in the project’s root folder (where you already have main.py, database.py, and score_dump_3.sql) and install the only two required packages—discord.py and mysql-connector-python—by running pip install discord.py mysql-connector-python. Next, ensure your MySQL server is running, then log in as a privileged user and create the database with CREATE DATABASE IF NOT EXISTS ScoreDB;. Import the schema and any seed data using mysql -u root -p ScoreDB < score_dump.sql (enter your password when prompted). After the database is in place, create a plain‐text file called discordToken.txt in the project folder and paste your bot token on the first line with no extra spaces or blank lines. Open main.py and confirm you’ve imported discord.ui.View, Button, and button at the top. Finally, run python main.py; you should see “Logged in as YourBotName (ID: …)” in the console, and in Discord the slash commands /instrument piano and /delete_score <id> will be available once they finish propagating.
