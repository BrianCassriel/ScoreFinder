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
        
        ALLOWED = {"piano", "saxophone", "violin"}
        inst = instrument.lower()

        if inst not in ALLOWED:
            return "Please choose one of: piano, saxophone, or violin."

        # 1. Look up its ID
        self.cursor.execute(
            "SELECT instrumentID FROM instrument WHERE LOWER(name) = %s;",
            (inst,)
        )
        row = self.cursor.fetchone()
        if row is None:
            return f"Instrument not found in database: {inst}."

        instr_id = row[0]

        # 2. Update the user
        self.cursor.execute(
            "UPDATE user SET primaryInstrument = %s WHERE discordID = %s;",
            (instr_id, user_id)
        )
        self.connection.commit()

        return f"Your primary instrument is now {inst}."

    def get_primary_instrument(self, user_id: int) -> str:
        """
        Look up and return the name of the user’s primary instrument,
        or None if they haven’t set one.
        """
        self.cursor.execute(
            """
            SELECT i.name
            FROM user u
            JOIN instrument i
                ON u.primaryInstrument = i.instrumentID
            WHERE u.discordID = %s;
            """,
            (user_id,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None
    
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