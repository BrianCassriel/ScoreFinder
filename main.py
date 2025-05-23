from typing import Optional, Literal
import discord
from discord import app_commands
from database import Database
from discord.ui import View, Button, button

scores_db = Database()
MY_GUILD = discord.Object(id=1366586741359644873)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

class ConfirmDeleteView(View):
    def __init__(self, score_id: int, db: Database):
        super().__init__(timeout=60)
        self.score_id = score_id
        self.db = db
        self.finished_msg = None

    @button(label="Yes, delete", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        # perform deletion and commit
        self.db.connection.start_transaction()
        self.db.cursor.execute(
            "DELETE FROM score WHERE scoreID = %s;",
            (self.score_id,)
        )
        self.db.connection.commit()
        await interaction.response.edit_message(
            content=f"Deleted score with ID {self.score_id}.", view=None
        )
        self.stop()

    @button(label="No, cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        # rollback and cancel
        self.db.connection.rollback()
        await interaction.response.edit_message(
            content="Deletion cancelled.", view=None
        )
        self.stop()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    for (guild) in client.guilds:
        scores_db.add_users(guild.members)

@client.event
async def on_member_join(member: discord.Member):
    scores_db.add_user(member)

@client.tree.command()
@app_commands.describe(
    instrument='Your primary instrument.'
)
async def instrument(interaction: discord.Interaction, instrument: Optional[str] = None):
    """Sets your primary instrument. Leave blank to see your current primary instrument."""
    # Show current if no argument
    if instrument is None:
        instrument = scores_db.get_primary_instrument(interaction.user.id)
        if instrument is not None:
            message = f"Your primary instrument is {instrument}."
        else:
            message = "You don't have a primary instrument set."
    else:
        # Normalize and delegate validation + update
        instrument = instrument.lower()
        message = scores_db.set_primary_instrument(interaction.user.id, instrument)

    await interaction.response.send_message(message, ephemeral=True)

@client.tree.context_menu(name='Show Primary Instrument')
async def show_primary_instrument(interaction: discord.Interaction, member: discord.Member):
    """Shows the primary instrument of a member."""
    instrument = scores_db.get_primary_instrument(member.id)
    if instrument is None:
        message = f"{member.display_name} does not have a primary instrument set."
    else:
        message = f"{member.display_name}'s primary instrument is {instrument}."
    await interaction.response.send_message(message, ephemeral=True)

@client.tree.command()
@app_commands.describe(
    by='The field to search by',
    search='The value to search for',
    use_primary_instrument='Whether to include only results using your primary instrument'
)
async def find(interaction: discord.Interaction, by: Literal["Title", "Composer", "Publisher", "Collection"], search: Optional[str] = '', use_primary_instrument: Optional[bool] = False):
    """Search scores and collections by title, composer or publisher."""
    await interaction.response.defer(ephemeral=True)
    results = scores_db.search_scores(interaction.user.id, by, search, use_primary_instrument)
    if len(results) == 0 and use_primary_instrument:
        await interaction.followup.send(f"No results found for '{search}' in {by} for {scores_db.get_primary_instrument(interaction.user.id)}.", ephemeral=True)
        return
    elif len(results) == 0:
        await interaction.followup.send(f"No results found for '{search}' in {by}.", ephemeral=True)
        return
    
    message = f"## Found {len(results)} results for '{search}' in {by}"
    if use_primary_instrument:
        message += f" (*{scores_db.get_primary_instrument(interaction.user.id)} only*)"
    message += ":\n"
    for result in results:
        message += f'(ID: {result[0]}) **{result[1]}** by {result[3]} from *{result[2]}*. Published by {result[4]}.\n'
    await interaction.followup.send(message, ephemeral=True)

@client.tree.command()
@app_commands.describe(
    title='The title of the score',
    composer='The composer of the score',
    publisher='The publisher of the score',
    collection='The collection of the score'
)
async def add_score(interaction: discord.Interaction, title: str, composer: str, publisher: Optional[str] = None, collection: Optional[str] = None): # ADD INSTRUMENTS
    """Adds a score to the database."""
    message = f"Added {title} by {composer} to the database."
    if publisher is not None:
        message += f" Publisher: {publisher}."
    if collection is not None:
        message += f" Collection: {collection}."
    await interaction.response.send_message(message, ephemeral=True)

@client.tree.command()
@app_commands.describe(
    id='The ID of the score to delete'
)
async def delete_score(interaction: discord.Interaction, id: int):
    """Deletes a score from the database, with confirmation."""
    # Send confirmation prompt
    view = ConfirmDeleteView(id, scores_db)
    await interaction.response.send_message(
        f"Are you sure you want to delete score ID {id}?",
        view=view,
        ephemeral=True
    )


@client.tree.command()

async def get_scores_csv(interaction: discord.Interaction):
    """Gets all scores in CSV format."""
    scores = scores_db.get_scores_dump()
    with open('scores.csv', 'w') as f:
        f.write("id,title,pdfFilename,collection,composer_first_name,composer_last_name,publisher,instrument\n")
        for score in scores:
            for i in range(len(score)):
                f.write(f"{score[i]}")
                if i < len(score) - 1:
                    f.write(",")
            f.write("\n")
    with open('scores.csv', 'rb') as f:
        await interaction.response.send_message(file=discord.File(f, 'scores.csv'), ephemeral=True)

token = open('discordToken.txt').readline().strip()
client.run(token)