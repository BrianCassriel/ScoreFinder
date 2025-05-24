# ScoreFinder

CPSC 408 Final Project - A Discord application to interface with a database of music scores.

**Landon Kauer** & **Brian Cassriel**

### Known Compile or Runtime Errors, or Code Limitations

N/A

## Installation

### 1. Open the Terminal in the Project Root

It contains `main.py`.

### 2. Install Required Python Packages

Use pip to install the necessary dependencies:

```bash
pip install discord.py mysql-connector-python
```

### 3. Start the MySQL Server

Ensure your MySQL server is running locally.

### 4. Create the Database & Import the Schema & Data

Use DataGrip to create a new database schema called "ScoreDB" and import the data using the `score_dump.sql` file.

### 5. Add Your Discord Bot Token

Create a plain-text file named `discordToken.txt` in the project folder. Paste your Discord bot token directly in this file.

### 6. Run the Bot

Start the bot by running:

```bash
python main.py
```

You should see output like:

```
Logged in as ScoreFinder (ID: ...)
```

The bot is now running, and the slash commands `/instrument piano` and `/delete_score <id>` will be available in Discord once they finish propagating!

### References

Geeks for geeks
StackOverflow
OpenAI ChatGPT for help with discord.py syntax and errors

Composer first and last name concatenation in SQL:
[SQL CONCAT()](https://learn.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver16)