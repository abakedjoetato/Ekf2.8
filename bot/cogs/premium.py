import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Premium(commands.Cog):
    """Premium features management"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="premium", description="Check premium status")
    async def premium(self, ctx: discord.ApplicationContext):
        """Check premium status"""
        try:
            await ctx.defer(ephemeral=True)

            embed = discord.Embed(
                title="💎 Premium Status",
                description="Premium features are currently in development",
                color=0xffd700
            )
            await ctx.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Premium command error: {e}")
            await ctx.followup.send("❌ Failed to check premium status", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Premium(bot))