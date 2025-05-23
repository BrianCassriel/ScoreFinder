from discord.ui import View, Button, button
from database import Database
import discord

class ConfirmDeleteView(View):
    def __init__(self, score_id: int, db: Database):
        super().__init__(timeout=60)
        self.score_id = score_id
        self.db = db
        self.finished_msg = None
        self.db.cursor.execute( # starts the transaction
            "DELETE FROM score WHERE scoreID = %s;",
            (self.score_id,)
        )

    @button(label="Yes, delete", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        self.db.connection.commit()
        await interaction.response.edit_message(
            content=f"Deleted score with ID {self.score_id}.", view=None
        )
        self.stop()

    @button(label="No, cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        self.db.connection.rollback()
        await interaction.response.edit_message(
            content="Deletion cancelled.", view=None
        )
        self.stop()