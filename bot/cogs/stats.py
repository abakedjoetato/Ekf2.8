import discord
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
```

```python
import logging

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

logger = logging.getLogger(__name__)

class AutomatedLeaderboard(commands.Cog):
    """Automated Leaderboard System"""

    def __init__(self, bot):
        self.bot = bot
        self.leaderboard_tasks = {}  # Store tasks to avoid duplicates
        self.running_tasks = set()
        self.autocompleter = ServerAutocomplete(bot)

    async def cog_load(self):
        """Load existing automated leaderboards from the database"""
        try:
            if not hasattr(self.bot, 'db_manager') or self.bot.db_manager is None:
                logger.warning("Database manager not initialized. Automated leaderboards will not be loaded.")
                return

            guilds = self.bot.db_manager.get_guilds()
            async for guild in guilds:
                guild_id = guild.get('_id')
                if not guild_id:
                    logger.warning(f"Skipping invalid guild document: {guild}")
                    continue

                leaderboards = guild.get('automated_leaderboards', [])
                for config in leaderboards:
                    try:
                        channel_id = config.get('channel_id')
                        leaderboard_type = config.get('leaderboard_type')
                        server_id = config.get('server_id', 'default')  # Use 'default' as fallback
                        update_interval = config.get('update_interval', 24)  # Hours
                        message_id = config.get('message_id')

                        if not all([channel_id, leaderboard_type, server_id, update_interval]):
                            logger.warning(f"Skipping leaderboard config with missing fields: {config}")
                            continue

                        # Type validation
                        if not isinstance(guild_id, int) or not isinstance(channel_id, int):
                            logger.warning(f"Invalid ID types in config: {config}")
                            continue

                        # Start the task if not already running
                        task_id = (guild_id, channel_id, leaderboard_type, server_id)
                        if task_id not in self.running_tasks:
                            self.running_tasks.add(task_id)
                            self.bot.loop.create_task(self.run_leaderboard_task(
                                guild_id=guild_id,
                                channel_id=channel_id,
                                leaderboard_type=leaderboard_type,
                                server_id=server_id,
                                update_interval=update_interval,
                                initial_message_id=message_id
                            ))
                            logger.info(f"Loaded automated leaderboard: {task_id}")
                        else:
                            logger.info(f"Automated leaderboard already running: {task_id}")

                    except Exception as config_error:
                        logger.error(f"Error loading leaderboard config: {config_error} - Config: {config}")

            logger.info("Automated leaderboards loaded")

        except Exception as e:
            logger.error(f"Error during cog load: {e}")

    async def run_leaderboard_task(self, guild_id: int, channel_id: int, leaderboard_type: str, server_id: str, update_interval: int, initial_message_id: int = None):
        """Background task to manage and update the automated leaderboard"""
        task_id = (guild_id, channel_id, leaderboard_type, server_id)
        try:

            pass
            await self.bot.wait_until_ready()
            guild = self.bot.get_guild(guild_id)
            if not guild:
                logger.warning(f"Guild not found: {guild_id}")
                self.running_tasks.discard(task_id)
                return

            channel = guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.TextChannel):
                logger.warning(f"Channel not found or invalid: {channel_id} in guild {guild_id}")
                self.running_tasks.discard(task_id)
                return

            message = None
            if initial_message_id:
                try:
                    message = await channel.fetch_message(initial_message_id)
                except discord.NotFound:
                    logger.warning(f"Initial message not found, creating a new one")
                except Exception as fetch_error:
                    logger.error(f"Failed to fetch initial message: {fetch_error}")

            while True:
                try:
                    # Fetch leaderboard data
                    if not hasattr(self.bot, 'db_manager') or not self.bot.db_manager:
                        logger.error("Database manager not initialized")
                        self.running_tasks.discard(task_id)
                        return

                    leaderboard_data = await self.bot.db_manager.get_leaderboard(leaderboard_type, guild_id=guild_id, server_id=server_id, limit=10)
                    if not leaderboard_data:
                        embed = discord.Embed(
                            title=f"📊 {leaderboard_type.title()} Leaderboard",
                            description="No data available",
                            color=0xff6b6b
                        )
                    else:
                        # Embed construction using EmbedFactory
                        embed_data = {
                            'leaderboard_type': leaderboard_type,
                            'data': leaderboard_data,
                            'guild_id': guild_id,
                            'server_id': server_id
                        }
                        embed, file_attachment = await EmbedFactory.build('leaderboard', embed_data)  # Correct usage

                    if embed:
                        if message:
                            try:
                                await message.edit(embed=embed)
                                logger.info(f"Updated leaderboard message in {channel.name} (Guild: {guild.name})")
                            except discord.errors.NotFound:
                                logger.warning(f"Message not found, creating a new one")
                                message = None  # Reset message to allow creation
                            except Exception as edit_error:
                                logger.error(f"Failed to edit message: {edit_error}")

                        if not message:
                            try:
                                message = await channel.send(embed=embed)
                                # Save the new message ID to the database
                                await self.bot.db_manager.update_leaderboard_message_id(guild_id, channel_id, leaderboard_type, server_id, message.id)
                                logger.info(f"Created new leaderboard message in {channel.name} (Guild: {guild.name})")
                            except Exception as send_error:
                                logger.error(f"Failed to send message: {send_error}")
                                self.running_tasks.discard(task_id)
                                return
                    else:
                        logger.error("EmbedFactory failed to create embed")

                except Exception as task_error:
                    logger.error(f"Task failed: {task_error}")

                await asyncio.sleep(update_interval * 3600)  # Convert hours to seconds

        except asyncio.CancelledError:
            logger.info(f"Leaderboard task cancelled: {task_id}")
        except Exception as e:
            logger.error(f"Exception in leaderboard task: {e}")
        finally:
            self.running_tasks.discard(task_id)
            logger.info(f"Leaderboard task finished: {task_id}")

    automated = SlashCommandGroup("automated", "Commands for managing automated leaderboards")

    @automated.command(name="create", description="Create an automated leaderboard in the specified channel.")
    @commands.has_permissions(administrator=True)
    async def create_leaderboard(self, ctx: discord.ApplicationContext,
                                 channel: discord.TextChannel,
                                 leaderboard_type: discord.Option(str, "Type of leaderboard", choices=["kills", "deaths", "kdr"]),
                                 server: discord.Option(str, "Server to display leaderboard for", autocomplete=ServerAutocomplete.autocomplete, required=False),
                                 update_interval: discord.Option(int, "Update interval in hours (default 24)", default=24)):
        """Create an automated leaderboard in the specified channel."""
        try:

            pass
            await ctx.defer(ephemeral=True)  # Acknowledge the command immediately

            guild_id = ctx.guild_id
            channel_id = channel.id
            server_id = server or 'default'  # Use 'default' if server is None
            task_id = (guild_id, channel_id, leaderboard_type, server_id)

            # Validate update interval
            if not (1 <= update_interval <= 720):  # 1 hour to 30 days
                await ctx.followup.send("Update interval must be between 1 and 720 hours.", ephemeral=True)
                return

            # Check if a task is already running for this channel and leaderboard type
            if task_id in self.running_tasks:
                await ctx.followup.send("A leaderboard is already running for this channel and type.", ephemeral=True)
                return

            # Save the configuration to the database
            config = {
                'channel_id': channel_id,
                'leaderboard_type': leaderboard_type,
                'server_id': server_id,
                'update_interval': update_interval
            }

            if not hasattr(self.bot, 'db_manager') or not self.bot.db_manager:
                await ctx.followup.send("Database manager not initialized.", ephemeral=True)
                return

            await self.bot.db_manager.add_automated_leaderboard(guild_id, config)
            logger.info(f"Added automated leaderboard config to DB: {config}")

            # Start the leaderboard task
            self.running_tasks.add(task_id)
            self.bot.loop.create_task(self.run_leaderboard_task(
                guild_id=guild_id,
                channel_id=channel_id,
                leaderboard_type=leaderboard_type,
                server_id=server_id,
                update_interval=update_interval
            ))

            await ctx.followup.send(f"Automated {leaderboard_type} leaderboard created in {channel.mention} (updates every {update_interval} hours).", ephemeral=True)

        except Exception as e:
            logger.error(f"Failed to create leaderboard: {e}")
            await ctx.followup.send("Failed to create leaderboard.", ephemeral=True)

    @automated.command(name="remove", description="Remove an automated leaderboard from the specified channel.")
    @commands.has_permissions(administrator=True)
    async def remove_leaderboard(self, ctx: discord.ApplicationContext,
                                 channel: discord.TextChannel,
                                 leaderboard_type: discord.Option(str, "Type of leaderboard", choices=["kills", "deaths", "kdr"]),
                                 server: discord.Option(str, "Server to remove leaderboard for", autocomplete=ServerAutocomplete.autocomplete, required=False)):
        """Remove an automated leaderboard from the specified channel."""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild_id
            channel_id = channel.id
            server_id = server or 'default'
            task_id = (guild_id, channel_id, leaderboard_type, server_id)

            # Check if the task is running
            if task_id not in self.running_tasks:
                await ctx.followup.send("No leaderboard is running for this channel and type.", ephemeral=True)
                return

            # Cancel the task
            for task in asyncio.all_tasks():
                if task.get_coro().__name__ == 'run_leaderboard_task':
                    task_args = task.get_coro().__defaults__
                    if task_args and (guild_id, channel_id, leaderboard_type, server_id) == (task_args[0], task_args[1], task_args[2], task_args[3]):
                        task.cancel()
                        break

            self.running_tasks.discard(task_id)
            logger.info(f"Stopped leaderboard task: {task_id}")

            # Remove the configuration from the database
            if not hasattr(self.bot, 'db_manager') or not self.bot.db_manager:
                await ctx.followup.send("Database manager not initialized.", ephemeral=True)
                return
            await self.bot.db_manager.remove_automated_leaderboard(guild_id, channel_id, leaderboard_type, server_id)
            logger.info(f"Removed automated leaderboard config from DB: {task_id}")

            await ctx.followup.send("Automated leaderboard removed.", ephemeral=True)

        except Exception as e:
            logger.error(f"Failed to remove leaderboard: {e}")
            await ctx.followup.send("Failed to remove leaderboard.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutomatedLeaderboard(bot))
```

```python
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Link(commands.Cog):
    """Link Discord user to in-game character"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="link", description="Link your Discord account to a character.")
    async def link(self, ctx: discord.ApplicationContext, character_name: str):
        """Link your Discord account to a character."""
        try:

            pass
            await ctx.defer(ephemeral=True)  # Acknowledge the command immediately

            guild_id = ctx.guild.id if ctx.guild else 0
            user_id = ctx.author.id
            cleaned_character_name = character_name.strip()

            # Validate character name
            if not (3 <= len(cleaned_character_name) <= 24):
                await ctx.followup.send("Character name must be between 3 and 24 characters.", ephemeral=True)
                return

            # Check for existing link
            existing_link = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if existing_link:
                # Add the new character name to the existing list
                existing_characters = existing_link.get('linked_characters', [])
                if cleaned_character_name in existing_characters:
                    await ctx.followup.send(f"Character '{cleaned_character_name}' is already linked to your account.", ephemeral=True)
                    return

                existing_characters.append(cleaned_character_name)
                await self.bot.db_manager.update_linked_player(guild_id, user_id, existing_characters)
                await ctx.followup.send(f"Character '{cleaned_character_name}' linked to your account.", ephemeral=True)
                logger.info(f"User {user_id} linked character {cleaned_character_name} (added to existing link)")
            else:
                # Create a new link
                await self.bot.db_manager.create_linked_player(guild_id, user_id, [cleaned_character_name])
                await ctx.followup.send(f"Character '{cleaned_character_name}' linked to your account.", ephemeral=True)
                logger.info(f"User {user_id} linked character {cleaned_character_name} (new link)")

        except Exception as e:
            logger.error(f"Failed to link character: {e}")
            await ctx.followup.send("Failed to link character.", ephemeral=True)

    @discord.slash_command(name="unlink", description="Unlink a character from your Discord account.")
    async def unlink(self, ctx: discord.ApplicationContext, character_name: str):
        """Unlink a character from your Discord account."""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild.id if ctx.guild else 0
            user_id = ctx.author.id
            cleaned_character_name = character_name.strip()

            # Get existing link
            existing_link = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if not existing_link:
                await ctx.followup.send("No linked characters found for your account.", ephemeral=True)
                return

            existing_characters = existing_link.get('linked_characters', [])
            if cleaned_character_name not in existing_characters:
                await ctx.followup.send(f"Character '{cleaned_character_name}' is not linked to your account.", ephemeral=True)
                return

            # Remove character from the list
            existing_characters.remove(cleaned_character_name)

            if existing_characters:
                # Update the link
                await self.bot.db_manager.update_linked_player(guild_id, user_id, existing_characters)
            else:
                # Remove the link if no characters are left
                await self.bot.db_manager.remove_linked_player(guild_id, user_id)

            await ctx.followup.send(f"Character '{cleaned_character_name}' unlinked from your account.", ephemeral=True)
            logger.info(f"User {user_id} unlinked character {cleaned_character_name}")

        except Exception as e:
            logger.error(f"Failed to unlink character: {e}")
            await ctx.followup.send("Failed to unlink character.", ephemeral=True)

    @discord.slash_command(name="listlinks", description="List all characters linked to your Discord account.")
    async def listlinks(self, ctx: discord.ApplicationContext):
        """List all characters linked to your Discord account."""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild.id if ctx.guild else 0
            user_id = ctx.author.id

            # Get existing link
            existing_link = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if not existing_link:
                await ctx.followup.send("No linked characters found for your account.", ephemeral=True)
                return

            linked_characters = existing_link.get('linked_characters', [])
            if not linked_characters:
                await ctx.followup.send("No linked characters found for your account.", ephemeral=True)
                return

            # Format the list of characters
            character_list = "\n".join(f"- {char}" for char in linked_characters)
            embed = discord.Embed(
                title="Linked Characters",
                description=character_list,
                color=0x00ff00  # Green color
            )

            await ctx.followup.send(embed=embed, ephemeral=True)
            logger.info(f"User {user_id} listed linked characters")

        except Exception as e:
            logger.error(f"Failed to list linked characters: {e}")
            await ctx.followup.send("Failed to list linked characters.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Link(bot))
```import logging
import asyncio

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class ProfileManagement(commands.Cog):
    """Profile Management System - Link and display profile information"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="profile", description="Display your linked profile (if any)")
    async def profile(self, ctx: discord.ApplicationContext):
        """Display linked profile information"""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild.id if ctx.guild else 0
            user_id = ctx.author.id

            # Fetch linked player data
            player_data = await self.bot.db_manager.get_linked_player(guild_id, user_id)

            if not player_data:
                await ctx.followup.send("❌ No linked characters found. Use `/link <character>` to get started!", ephemeral=True)
                return

            linked_characters = player_data.get('linked_characters', [])
            if not linked_characters:
                await ctx.followup.send("❌ No linked characters found. Use `/link <character>` to get started!", ephemeral=True)
                return

            # Craft the profile embed
            embed = discord.Embed(
                title=f"🎮 {ctx.author.display_name}'s Profile",
                color=0x3498db  # Blue color
            )

            # List linked characters
            character_list = "\n".join(f"- {char}" for char in linked_characters)
            embed.add_field(name="Linked Characters", value=character_list, inline=False)

            # Optional: Display stats preview (Kills, Deaths, KDR)
            total_kills = 0
            total_deaths = 0
            for character in linked_characters:
                stats = await self.bot.db_manager.get_player_stats(guild_id, character)
                if stats:
                    total_kills += stats.get('kills', 0)
                    total_deaths += stats.get('deaths', 0)

            kdr = (total_kills / total_deaths) if total_deaths else total_kills
            embed.add_field(name="Total Kills", value=str(total_kills), inline=True)
            embed.add_field(name="Total Deaths", value=str(total_deaths), inline=True)
            embed.add_field(name="K/D Ratio", value=f"{kdr:.2f}", inline=True)

            await ctx.followup.send(embed=embed, ephemeral=True)
            logger.info(f"User {user_id} displayed their profile")

        except Exception as e:
            logger.error(f"Failed to display profile: {e}")
            await ctx.followup.send("Failed to display profile.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ProfileManagement(bot))
```

```python
import logging
import asyncio

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class StatsCommands(commands.Cog):
    """Stats Commands - Retrieve and display player statistics"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="kd", description="Check your Kill/Death ratio")
    async def kd(self, ctx: discord.ApplicationContext):
        """Check own K/D ratio (linked character required)"""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild.id if ctx.guild else 0
            user_id = ctx.author.id

            # Fetch linked player data
            player_data = await self.bot.db_manager.get_linked_player(guild_id, user_id)
            if not player_data:
                await ctx.followup.send("❌ No linked characters found. Use `/link <character>` to get started!", ephemeral=True)
                return

            linked_characters = player_data.get('linked_characters', [])
            if not linked_characters:
                await ctx.followup.send("❌ No linked characters found. Use `/link <character>` to get started!", ephemeral=True)
                return

            # Calculate combined K/D ratio across all linked characters
            total_kills = 0
            total_deaths = 0
            for character in linked_characters:
                stats = await self.bot.db_manager.get_player_stats(guild_id, character)
                if stats:
                    total_kills += stats.get('kills', 0)
                    total_deaths += stats.get('deaths', 0)

            kdr = (total_kills / total_deaths) if total_deaths else total_kills
            await ctx.followup.send(f"🔪 Your K/D Ratio: **{kdr:.2f}**", ephemeral=True)
            logger.info(f"User {user_id} checked their K/D ratio")

        except Exception as e:
            logger.error(f"Failed to check K/D ratio: {e}")
            await ctx.followup.send("Failed to check K/D ratio.", ephemeral=True)

    @discord.slash_command(name="playerstats", description="Check stats for a specific player name")
    async def playerstats(self, ctx: discord.ApplicationContext, player_name: str):
        """Check stats for a specific player name"""
        try:

            pass
            await ctx.defer(ephemeral=True)

            guild_id = ctx.guild.id if ctx.guild else 0
            # player_name = player_name.strip()  # Strip whitespace (already done in autocomplete)

            # Database interaction to fetch player data

            # Ensure database manager exists
            if not self.bot.db_manager:
                logger.error("Database manager not initialized")
                error_embed = discord.Embed(
                    title="❌ Database Error",
                    description="Database connection unavailable",
                    color=0xff6b6b
                )
                await ctx.followup.send(embed=error_embed)
                return

            # Validate player data exists
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
                    'kills': int(stats.get('kills', 0)),
                    'deaths': int(stats.get('deaths', 0)),
                    'kdr': float(stats.get('kdr', 0.0)) if stats.get('kdr') else 0.0,
                    'longest_kill_distance': int(stats.get('longest_kill_distance', 0)) if stats.get('longest_kill_distance') else 0,
                    'favorite_weapon': str(stats.get('favorite_weapon', 'Unknown')),
                    'player_name': str(player_name),
                    'guild_id': ctx.guild_id
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

            # Create advanced stats embed using correct EmbedFactory method
            from bot.utils.embed_factory import EmbedFactory
            try:
                embed, file_attachment = await EmbedFactory.build('advanced_stats', validated_stats)

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

async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
```

```python
import logging
import asyncio

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Leaderboard(commands.Cog):
    """Leaderboard Commands - View server leaderboards"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="leaderboard", description="View server leaderboards")
    async def leaderboard(self, ctx: discord.ApplicationContext, leaderboard_type: discord.Option(str, "Type of leaderboard", choices=["kills", "deaths", "kdr"])):
        """View server leaderboards"""
        try:

            pass
            await ctx.defer(ephemeral=True)

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

            # Get leaderboard data with validation
            leaderboard_data = await self.bot.db_manager.get_leaderboard(leaderboard_type, limit=10)
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
                        'player_name': str(entry.get('player_name', 'Unknown')),
                        'kills': int(entry.get('kills', 0)),
                        'deaths': int(entry.get('deaths', 0)),
                        'kdr': float(entry.get('kdr', 0.0)) if entry.get('kdr') else 0.0,
                        'rank': len(validated_data) + 1
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

            # Create leaderboard embed using correct EmbedFactory method
            from bot.utils.embed_factory import EmbedFactory
            try:
                embed_data = {
                    'leaderboard_type': leaderboard_type,
                    'data': validated_data,
                    'guild_id': ctx.guild_id
                }

                embed, file_attachment = await EmbedFactory.build('leaderboard', embed_data)

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
                    leaderboard_text += f"{i}. **{entry['player_name']}** - {entry['kills']} kills\n"

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
    await bot.add_cog(Leaderboard(bot))
```

```python
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Utilities(commands.Cog):
    """Utility commands for server management"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext):
        """Check the bot's latency"""
        try:

            pass
            await ctx.defer(ephemeral=True)
            latency = round(self.bot.latency * 1000)  # Milliseconds
            await ctx.followup.send(f"🏓 Pong! Latency: {latency}ms", ephemeral=True)
            logger.info(f"Ping command used by {ctx.author.id}, latency: {latency}ms")

        except Exception as e:
            logger.error(f"Ping command error: {e}")
            await ctx.followup.send("Failed to retrieve latency.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utilities(bot))
```

```python
import logging
import asyncio

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Help(commands.Cog):
    """Help command to list available commands"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help", description="List available commands")
    async def help(self, ctx: discord.ApplicationContext):
        """List available commands"""
        try:

            pass
            await ctx.defer(ephemeral=True)

            embed = discord.Embed(
                title="Commands",
                description="List of available commands",
                color=0x00ff00  # Green color
            )

            # Iterate through all loaded cogs and their commands
            for cog_name, cog in self.bot.cogs.items():
                commands_list = []
                for command in cog.walk_commands():  # Use walk_commands for hybrid commands
                    if isinstance(command, discord.SlashCommand):  # Check if it's a SlashCommand
                        commands_list.append(f"`/{command.qualified_name}` - {command.description}")  # Use qualified_name
                if commands_list:
                    embed.add_field(name=cog_name, value="\n".join(commands_list), inline=False)

            await ctx.followup.send(embed=embed, ephemeral=True)
            logger.info(f"Help command used by {ctx.author.id}")

        except Exception as e:
            logger.error(f"Help command error: {e}")
            await ctx.followup.send("Failed to retrieve command list.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))