import logging
from datetime import datetime
from typing import Dict, Any
from discord.ext import commands
from bot.cogs.autocomplete import ServerAutocomplete

logger = logging.getLogger(__name__)

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="stats", description="Display player statistics")
    async def stats(self, ctx: discord.ApplicationContext, 
                   player_name: discord.Option(str, "Player name to get stats for"),
                   server: discord.Option(str, "Server to get stats from", autocomplete=ServerAutocomplete.autocomplete, required=False)):
        """Display comprehensive player statistics"""
        try:
            await ctx.defer()

            guild_id = ctx.guild_id
            server_id = server or 'default'

            # Validate database manager exists
            if not self.bot.db_manager:
                logger.error("Database manager not initialized for stats")
                error_embed = discord.Embed(
                    title="❌ Database Error",
                    description="Database connection unavailable",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
                return

            # Get player statistics with proper validation
            stats = await self.bot.db_manager.get_player_combined_stats(player_name)
            logger.info(f"Retrieved stats for {player_name}: {stats}")

            if not stats or not any([stats.get('kills', 0), stats.get('deaths', 0)]):
                embed = discord.Embed(
                    title="📊 Player Not Found",
                    description=f"No PvP data found for player **{player_name}**",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=embed)
                return

            # Ensure all numeric values are properly typed with validation
            try:
                validated_stats = {
                    'player_name': str(player_name),
                    'server_name': server_id,
                    'kills': int(stats.get('kills', 0)),
                    'deaths': int(stats.get('deaths', 0)),
                    'kdr': float(stats.get('kdr', 0.0)) if stats.get('kdr') else 0.0,
                    'personal_best_distance': float(stats.get('personal_best_distance', 0)) if stats.get('personal_best_distance') else 0.0,
                    'favorite_weapon': str(stats.get('favorite_weapon', 'Unknown')),
                    'weapon_kills': int(stats.get('weapon_kills', 0)) if stats.get('weapon_kills') else 0,
                    'active_days': int(stats.get('active_days', 0)) if stats.get('active_days') else 0,
                    'total_distance': float(stats.get('total_distance', 0)) if stats.get('total_distance') else 0.0,
                    'guild_id': guild_id
                }
                logger.info(f"Validated stats: {validated_stats}")
            except (ValueError, TypeError) as e:
                logger.error(f"Stats validation error: {e}")
                error_embed = discord.Embed(
                    title="❌ Data Error", 
                    description="Invalid statistics data format",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
                return

            # Create advanced stats embed using EmbedFactory
            from bot.utils.embed_factory import EmbedFactory
            try:
                embed, file_attachment = await EmbedFactory.build_advanced_stats_embed(validated_stats)

                if embed:
                    await ctx.followup.send(embed=embed, file=file_attachment)
                    logger.info(f"✅ Stats embed sent for {player_name}")
                else:
                    logger.error("EmbedFactory returned None embed")
                    raise Exception("Embed creation failed")

            except Exception as embed_error:
                logger.error(f"EmbedFactory error: {embed_error}")
                # Fallback embed if factory fails
                fallback_embed = discord.Embed(
                    title=f"📊 Stats for {player_name}",
                    description=f"**Kills:** {validated_stats['kills']}\n**Deaths:** {validated_stats['deaths']}\n**K/D:** {validated_stats['kdr']:.2f}",
                    color=0x00ff88
                )
                await ctx.followup.send(embed=fallback_embed)

        except Exception as e:
            logger.error(f"Stats command error: {e}")
            try:
                error_embed = discord.Embed(
                    title="❌ Error",
                    description="Failed to retrieve player statistics",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
            except:
                pass

    @discord.slash_command(name="leaderboard", description="Display server leaderboards")
    async def leaderboard(self, ctx: discord.ApplicationContext,
                         leaderboard_type: discord.Option(str, "Type of leaderboard", choices=["kills", "deaths", "kdr"]),
                         server: discord.Option(str, "Server to get leaderboard from", autocomplete=ServerAutocomplete.autocomplete, required=False)):
        """Display server leaderboards"""
        try:
            await ctx.defer()

            # Validate database manager exists
            if not self.bot.db_manager:
                logger.error("Database manager not initialized for leaderboard")
                error_embed = discord.Embed(
                    title="❌ Database Error",
                    description="Database connection unavailable",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
                return

            server_id = server or 'default'

            # Get leaderboard data with validation
            leaderboard_data = await self.bot.db_manager.get_leaderboard(leaderboard_type, guild_id=ctx.guild_id, server_id=server_id, limit=10)
            logger.info(f"Retrieved {leaderboard_type} leaderboard: {len(leaderboard_data) if leaderboard_data else 0} entries")

            if not leaderboard_data:
                embed = discord.Embed(
                    title="📊 No Data",
                    description=f"No {leaderboard_type} data available",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=embed)
                return

            # Validate and type-cast leaderboard entries
            validated_data = []
            for entry in leaderboard_data:
                try:
                    validated_entry = {
                        'name': str(entry.get('player_name', 'Unknown')),
                        'value': entry.get(leaderboard_type, 0),
                        'metric': leaderboard_type
                    }
                    validated_data.append(validated_entry)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Skipping invalid leaderboard entry: {e}")
                    continue

            if not validated_data:
                embed = discord.Embed(
                    title="📊 Data Error",
                    description="No valid leaderboard entries found", 
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=embed)
                return

            # Create leaderboard embed using EmbedFactory
            from bot.utils.embed_factory import EmbedFactory
            try:
                embed_data = {
                    'title': f"{leaderboard_type.upper()} LEADERBOARD",
                    'description': f"Top players by {leaderboard_type}",
                    'leaderboard_type': leaderboard_type,
                    'rankings_data': validated_data,
                    'server_name': server_id,
                    'guild_id': ctx.guild_id
                }

                embed, file_attachment = await EmbedFactory.build_advanced_leaderboard_embed(embed_data)

                if embed:
                    await ctx.followup.send(embed=embed, file=file_attachment)
                    logger.info(f"✅ {leaderboard_type} leaderboard sent with {len(validated_data)} entries")
                else:
                    logger.error("EmbedFactory returned None for leaderboard")
                    raise Exception("Leaderboard embed creation failed")

            except Exception as embed_error:
                logger.error(f"Leaderboard EmbedFactory error: {embed_error}")
                # Fallback embed
                fallback_embed = discord.Embed(
                    title=f"📊 {leaderboard_type.title()} Leaderboard",
                    description=f"Top {len(validated_data)} players",
                    color=0x00ff88
                )

                leaderboard_text = ""
                for i, entry in enumerate(validated_data[:10], 1):
                    leaderboard_text += f"{i}. **{entry['name']}** - {entry['value']}\n"

                fallback_embed.add_field(name="Rankings", value=leaderboard_text or "No data", inline=False)
                await ctx.followup.send(embed=fallback_embed)

        except Exception as e:
            logger.error(f"Leaderboard command error: {e}")
            try:
                error_embed = discord.Embed(
                    title="❌ Error",
                    description="Failed to retrieve leaderboard data",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
            except:
                pass

async def setup(bot):
    await bot.add_cog(Stats(bot))