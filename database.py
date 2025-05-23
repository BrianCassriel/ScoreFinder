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
    
    def search_scores(self, user_id: int, by: str, search: str, use_primary_instrument: bool = False) -> list[tuple]:
        # Search the scores in the database
        # by is the field to search by
        # search is the value to search for
        # use_primary_instrument is whether to include only results using the user's primary instrument
        search_field_map = {
            "Title": "score.title",
            "Composer": "CONCAT(firstName, ' ', lastName)",
            "Collection": "collection.name",
            "Publisher": "publisher.name"
        }
        query = f'''
            SELECT
                score.scoreID AS ID,
                score.title AS title,
                collection.name AS collection,
                CONCAT(firstName, ' ', lastName) AS composer,
                publisher.name AS publisher
            FROM score
            INNER JOIN collection
                ON score.collectionID = collection.collectionID
            INNER JOIN scorecomposers
                ON score.scoreID = scorecomposers.scoreID
            INNER JOIN composer
                ON scorecomposers.composerID = composer.composerID
            INNER JOIN publisher
                ON score.publisherID = publisher.publisherID
        '''

        if use_primary_instrument:
            query += '''
            INNER JOIN scoreinstruments
                ON score.scoreID = scoreinstruments.scoreID
            INNER JOIN user
                ON user.primaryInstrument = scoreinstruments.instrumentID
            '''
        query += f'''
            WHERE {search_field_map[by]} LIKE '%{search}%'
        '''
        if use_primary_instrument:
            query += f' AND user.discordID = {user_id};'
        else:
            query += ';'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def delete_score(self, id: int):
        self.cursor.execute('''
            DELETE FROM score
            WHERE id = %s;
        ''', (id,))
        self.connection.commit()

    def get_scores_dump(self):
        self.cursor.execute('''
            SELECT *
            FROM all_score_info;
        ''')
        return self.cursor.fetchall()