import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Economy(commands.Cog):
    """Economy system"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="balance", description="Check your balance")
    async def balance(self, ctx: discord.ApplicationContext):
        """Check user balance"""
        try:
            await ctx.defer(ephemeral=True)

            embed = discord.Embed(
                title="💰 Balance",
                description="Economy system is currently in development",
                color=0x00ff88
            )
            await ctx.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Balance command error: {e}")
            await ctx.followup.send("❌ Failed to check balance", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Economy(bot))