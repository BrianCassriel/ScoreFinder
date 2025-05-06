import mysql.connector
import discord

class Database:
    def __init__(self):
        # setup connection & cursor
        pass

    def add_users(self, members: list[discord.Member]):
        # Add to the users table
        # must check if the user is already in the database
        pass

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