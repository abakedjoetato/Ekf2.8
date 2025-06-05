import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Linking(commands.Cog):
    """Player linking system"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="link", description="Link your Discord account to a player name")
    async def link(self, ctx: discord.ApplicationContext, 
                  player_name: discord.Option(str, "Player name to link")):
        """Link Discord account to player name"""
        try:
            await ctx.defer(ephemeral=True)

            if not self.bot.db_manager:
                await ctx.followup.send("❌ Database unavailable", ephemeral=True)
                return

            # Validate player name
            if not player_name or len(player_name.strip()) < 3:
                await ctx.followup.send("❌ Player name must be at least 3 characters", ephemeral=True)
                return

            guild_id = ctx.guild_id
            user_id = ctx.user.id

            # Check if already linked
            existing_link = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if existing_link:
                await ctx.followup.send("❌ You already have a linked player. Use `/unlink` first.", ephemeral=True)
                return

            # Create link
            await self.bot.db_manager.create_linked_player(guild_id, user_id, player_name.strip())
            await ctx.followup.send(f"✅ Linked to player: **{player_name.strip()}**", ephemeral=True)

        except Exception as e:
            logger.error(f"Link command error: {e}")
            await ctx.followup.send("❌ Failed to link player", ephemeral=True)

    @discord.slash_command(name="unlink", description="Unlink your Discord account")
    async def unlink(self, ctx: discord.ApplicationContext):
        """Unlink Discord account"""
        try:
            await ctx.defer(ephemeral=True)

            if not self.bot.db_manager:
                await ctx.followup.send("❌ Database unavailable", ephemeral=True)
                return

            guild_id = ctx.guild_id
            user_id = ctx.user.id

            # Check if linked
            existing_link = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if not existing_link:
                await ctx.followup.send("❌ No linked player found", ephemeral=True)
                return

            # Remove link
            await self.bot.db_manager.remove_linked_player(guild_id, user_id)
            await ctx.followup.send("✅ Player unlinked successfully", ephemeral=True)

        except Exception as e:
            logger.error(f"Unlink command error: {e}")
            await ctx.followup.send("❌ Failed to unlink player", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Linking(bot))