import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class AdminChannels(commands.Cog):
    """Admin channel management"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="configure", description="Configure bot channels")
    @commands.has_permissions(administrator=True)
    async def configure(self, ctx: discord.ApplicationContext,
                       channel_type: discord.Option(str, "Channel type", choices=["killfeed", "leaderboard", "stats"]),
                       channel: discord.Option(discord.TextChannel, "Channel to configure")):
        """Configure bot channels"""
        try:
            await ctx.defer(ephemeral=True)

            if not self.bot.db_manager:
                await ctx.followup.send("❌ Database unavailable", ephemeral=True)
                return

            guild_id = ctx.guild_id

            # Update channel configuration
            await self.bot.db_manager.update_channel_config(guild_id, channel_type, channel.id)
            await ctx.followup.send(f"✅ {channel_type} channel set to {channel.mention}", ephemeral=True)

        except Exception as e:
            logger.error(f"Configure command error: {e}")
            await ctx.followup.send("❌ Failed to configure channel", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminChannels(bot))