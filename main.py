from typing import Optional, Literal
import discord
from discord import app_commands
from database import Database

scores_db = Database()
MY_GUILD = discord.Object(id=1366586741359644873)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

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
    message = f"You don't have a primary instrument set."
    if instrument is None:
        instrument = scores_db.get_primary_instrument(interaction.user.id)
        if instrument is not None:
            message = f"Your primary instrument is {instrument}."
    else:
        instrument = instrument.lower()
        scores_db.set_primary_instrument(interaction.user.id, instrument)
        message = f"Your primary instrument is now {instrument}."
    await interaction.response.send_message(message, ephemeral=True)

@client.tree.context_menu(name='Show Primary Instrument')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
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
async def find(interaction: discord.Interaction, by: Literal["Title", "Composer", "Publisher"], search: str, use_primary_instrument: Optional[bool] = None):
    """Search scores and collections by title, composer or publisher."""
    results = scores_db.search_scores(by, search, use_primary_instrument)
    # The results are a list of tuples, where each tuple is a score.
    # Will need to format this nicely.
    await interaction.response.send_message(f'You would like to search for {search} by {by}.', ephemeral=True)

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
    """Deletes a score from the database."""
    scores_db.delete_score(id)
    message = f"Deleted score with ID {id} from the database."
    await interaction.response.send_message(message, ephemeral=True)

token = open('discordToken.txt').readline().strip()
client.run(token)