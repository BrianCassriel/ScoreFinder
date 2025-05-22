import mysql.connector
import discord

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CPSC408",
            auth_plugin='mysql_native_password',
            database='ScoreDB'
        )
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_user(self, user_id: int) -> tuple:
        self.cursor.execute('''
            SELECT * 
            FROM user
            WHERE discordID = %s;
        ''', (user_id,))
        return self.cursor.fetchone()

    def add_user(self, member: discord.Member):
        known_id = self.get_user(member.id)
        if (known_id is not None):
            return known_id
        self.cursor.execute('''
            INSERT INTO user(discordID)
            VALUES (%s);
        ''', (member.id,))
        self.connection.commit()
        return member.id
    
    def add_users(self, members: list[discord.Member]):
        for member in members:
            self.add_user(member)

    def set_primary_instrument(self, user_id: int, instrument: str):
        pass

    def get_primary_instrument(self, user_id: int) -> str:
        return "piano"
    
    def search_scores(self, by: str, search: str, use_primary_instrument: bool = False) -> list[tuple]:
        # Search the scores in the database
        # by is the field to search by
        # search is the value to search for
        # use_primary_instrument is whether to include only results using the user's primary instrument
        return []
    
    def delete_score(self, id: int):
        pass

    def dump(self):
        # Dump the database to a csv file
        pass