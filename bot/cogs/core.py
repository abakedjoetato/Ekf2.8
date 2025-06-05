import discord
from discord.ext import commands
import logging
import platform
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class Core(commands.Cog):
    """Core bot commands and utilities"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, ctx: discord.ApplicationContext):
        """Check the bot's latency"""
        try:
            await ctx.defer()

            latency = round(self.bot.latency * 1000)
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Bot latency: **{latency}ms**",
                color=0x00ff88
            )
            await ctx.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Ping command error: {e}")
            await ctx.followup.send("❌ Failed to check latency", ephemeral=True)

    @discord.slash_command(name="info", description="Display bot information")
    async def info(self, ctx: discord.ApplicationContext):
        """Display bot information"""
        try:
            await ctx.defer()

            embed = discord.Embed(
                title="🤖 Bot Information",
                color=0x3498db
            )
            embed.add_field(name="Bot Version", value="2.0.0", inline=True)
            embed.add_field(name="Discord.py", value=discord.__version__, inline=True)
            embed.add_field(name="Python", value=platform.python_version(), inline=True)
            embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="Users", value=len(self.bot.users), inline=True)
            embed.timestamp = datetime.now(timezone.utc)

            await ctx.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Info command error: {e}")
            await ctx.followup.send("❌ Failed to retrieve bot information", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Core(bot))