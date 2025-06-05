"""
Emerald's Killfeed - Advanced Embed Factory
Leveraging py-cord 2.6.1 advanced features with professional military aesthetics
"""

import discord
from datetime import datetime, timezone
from pathlib import Path
import logging
import random
import re
from typing import Dict, Any, Optional, Tuple, List

logger = logging.getLogger(__name__)

def should_use_inline(field_value: str, max_inline_chars: int = 20) -> bool:
    """Determine if field should be inline based on content length to prevent wrapping"""
    clean_text = re.sub(r'[*`_~<>:]', '', str(field_value))
    return len(clean_text) <= max_inline_chars

class EmbedFactory:
    """Advanced embed factory using py-cord 2.6.1 features with military-grade aesthetics"""

    # Enhanced color palette with gradient-style effects
    COLORS = {
        'killfeed': 0x8B0000,        # Dark red for combat
        'suicide': 0xFF4500,         # Orange red for self-elimination
        'falling': 0x4169E1,         # Royal blue for gravity events
        'connection': 0x228B22,      # Forest green for connections
        'mission': 0x1E90FF,         # Dodger blue for missions
        'airdrop': 0xFF8C00,         # Dark orange for supply drops
        'helicrash': 0xDC143C,       # Crimson for crashes
        'trader': 0x9932CC,          # Dark orchid for commerce
        'vehicle': 0x696969,         # Dim gray for vehicles
        'success': 0x32CD32,         # Lime green for success
        'error': 0xFF1493,           # Deep pink for errors
        'warning': 0xFFD700,         # Gold for warnings
        'info': 0x00CED1,            # Dark turquoise for info
        'bounty': 0xFF6347,          # Tomato for contracts
        'economy': 0x90EE90,         # Light green for economy
        'elite': 0xFFD700,           # Gold for elite status
        'legendary': 0xFF00FF,       # Magenta for legendary
        'faction': 0x8A2BE2          # Blue violet for factions
    }

    # Professional progress bar characters
    PROGRESS_CHARS = {
        'full': '█',
        'high': '▓', 
        'medium': '▒',
        'low': '░',
        'empty': '▫'
    }

    # Military rank indicators
    RANK_INDICATORS = {
        'elite': '◆',
        'veteran': '◇',
        'experienced': '△',
        'regular': '▽',
        'recruit': '○'
    }

    # Threat level indicators
    THREAT_INDICATORS = {
        'critical': '■',
        'high': '▪',
        'medium': '▫',
        'low': '▪',
        'minimal': '·'
    }

    @staticmethod
    def create_progress_bar(value: float, max_value: float, length: int = 10) -> str:
        """Create a professional progress bar using Unicode blocks"""
        if max_value == 0:
            return f"{'▫' * length} 0%"

        percentage = min(100, (value / max_value) * 100)
        filled_length = int((percentage / 100) * length)

        bar = ''
        for i in range(length):
            if i < filled_length:
                bar += EmbedFactory.PROGRESS_CHARS['full']
            else:
                bar += EmbedFactory.PROGRESS_CHARS['empty']

        return f"{bar} {percentage:.0f}%"

    @staticmethod
    def format_performance_tier(kdr: float, kills: int) -> Tuple[str, str, int]:
        """Determine performance tier with military classification"""
        if kdr >= 3.0 and kills >= 100:
            return "ELITE OPERATOR", EmbedFactory.RANK_INDICATORS['elite'], 0xFF0000
        elif kdr >= 2.0 and kills >= 50:
            return "VETERAN COMBATANT", EmbedFactory.RANK_INDICATORS['veteran'], 0xFF8C00
        elif kdr >= 1.5 and kills >= 25:
            return "EXPERIENCED SOLDIER", EmbedFactory.RANK_INDICATORS['experienced'], 0xFFD700
        elif kdr >= 1.0:
            return "TACTICAL OPERATIVE", EmbedFactory.RANK_INDICATORS['regular'], 0x32CD32
        else:
            return "FIELD RECRUIT", EmbedFactory.RANK_INDICATORS['recruit'], 0x808080

    @staticmethod
    def create_ranking_display(rank: int, name: str, value: Any, metric: str = "") -> str:
        """Create enhanced ranking display with visual indicators"""
        rank_symbols = {1: "◆", 2: "◇", 3: "△"}
        symbol = rank_symbols.get(rank, "▫")

        # Format value based on type
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
        elif isinstance(value, int) and value >= 1000:
            formatted_value = f"{value:,}"
        else:
            formatted_value = str(value)

        return f"{symbol} **{name}** • {formatted_value} {metric}"

    @staticmethod
    def format_stats_dashboard(stats: Dict[str, Any]) -> Dict[str, str]:
        """Create comprehensive stats dashboard with visual elements"""
        kills = stats.get('kills', 0)
        deaths = stats.get('deaths', 0)
        kdr = stats.get('kdr', 0.0)

        # Calculate advanced metrics
        total_engagements = kills + deaths
        survival_rate = (kills / max(total_engagements, 1)) * 100 if total_engagements > 0 else 0
        efficiency_rating = min(100, (kdr * 20) + (stats.get('best_streak', 0) * 2))

        # Create visual progress bars
        survival_bar = EmbedFactory.create_progress_bar(survival_rate, 100, 8)
        efficiency_bar = EmbedFactory.create_progress_bar(efficiency_rating, 100, 8)

        # Performance classification
        tier, indicator, color = EmbedFactory.format_performance_tier(kdr, kills)

        return {
            'primary_stats': f"**Eliminations:** {int(kills):,}\n**Casualties:** {int(deaths):,}\n**K/D Ratio:** {float(kdr):.2f}",
            'performance_analysis': f"**Survival Rate:** {survival_bar}\n**Efficiency:** {efficiency_bar}",
            'classification': f"{indicator} **{tier}**",
            'color': color
        }

    @staticmethod
    async def build_advanced_leaderboard_embed(embed_data: Dict[str, Any]) -> Tuple[discord.Embed, discord.File]:
        """Build revolutionary leaderboard with advanced visual hierarchy"""
        try:
            title = embed_data.get('title', "COMBAT SUPERIORITY RANKINGS")
            description = embed_data.get('description', 'Elite warriors ranked by battlefield dominance')

            # Dynamic color based on leaderboard type
            lb_type = embed_data.get('leaderboard_type', 'kills')
            color_map = {
                'kills': EmbedFactory.COLORS['killfeed'],
                'kdr': EmbedFactory.COLORS['elite'],
                'weapons': EmbedFactory.COLORS['info'],
                'factions': EmbedFactory.COLORS['faction']
            }
            color = color_map.get(lb_type, EmbedFactory.COLORS['info'])

            embed = discord.Embed(
                title=f"◆ {title}",
                description=f"**{description}**",
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            # Enhanced rankings with visual hierarchy
            rankings_data = embed_data.get('rankings_data', [])
            if rankings_data:
                ranking_display = []
                for i, entry in enumerate(rankings_data[:10], 1):
                    name = entry.get('name', 'Unknown')
                    value = entry.get('value', 0)
                    metric = entry.get('metric', '')

                    display_line = EmbedFactory.create_ranking_display(i, name, value, metric)
                    ranking_display.append(display_line)

                embed.add_field(
                    name="◆ TOP COMBATANTS",
                    value="\n".join(ranking_display),
                    inline=False
                )

            # Server context with enhanced formatting
            server_name = embed_data.get('server_name', 'All Theaters')
            total_players = embed_data.get('total_players', 0)

            embed.add_field(
                name="◆ OPERATIONAL THEATER",
                value=f"**{server_name}**\n{total_players} Active Combatants",
                inline=True
            )

            # Performance statistics
            if 'stats_summary' in embed_data:
                stats = embed_data['stats_summary']
                avg_kdr = stats.get('average_kdr', 0.0)
                total_kills = stats.get('total_kills', 0)

                embed.add_field(
                    name="◆ THEATER STATISTICS",
                    value=f"**Average K/D:** {avg_kdr:.2f}\n**Total Eliminations:** {total_kills:,}",
                    inline=True
                )

            # Footer with enhanced timestamp
            embed.set_footer(
                text="◆ Intelligence Report • Powered by Emerald Tactical Systems",
                icon_url="attachment://Leaderboard.png"
            )

            # Appropriate thumbnail
            thumbnail_map = {
                'weapons': 'WeaponStats.png',
                'factions': 'Faction.png'
            }
            thumbnail = thumbnail_map.get(lb_type, 'Leaderboard.png')

            asset_file = discord.File(f"./assets/{thumbnail}", filename=thumbnail)
            embed.set_thumbnail(url=f"attachment://{thumbnail}")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building advanced leaderboard embed: {e}")
            return await EmbedFactory.build_error_embed("Leaderboard system error")

    @staticmethod
    async def build_advanced_stats_profile(embed_data: Dict[str, Any]) -> Tuple[discord.Embed, discord.File]:
        """Compatibility method for stats system"""
        return await EmbedFactory.build_advanced_stats_embed(embed_data)

    @staticmethod
    async def build_advanced_stats_embed(embed_data: Dict[str, Any]) -> Tuple[discord.Embed, discord.File]:
        """Build comprehensive stats profile with military intelligence formatting"""
        try:
            player_name = embed_data.get('player_name', 'Unknown Operative')
            server_name = embed_data.get('server_name', 'Unknown Theater')

            # Generate dashboard
            dashboard = EmbedFactory.format_stats_dashboard(embed_data)

            embed = discord.Embed(
                title="◆ MILITARY INTELLIGENCE DOSSIER",
                description=f"**OPERATIVE:** {player_name}\n**THEATER:** {server_name}",
                color=dashboard['color'],
                timestamp=datetime.now(timezone.utc)
            )

            # Primary combat metrics with visual bars
            embed.add_field(
                name="◆ COMBAT PERFORMANCE",
                value=dashboard['primary_stats'],
                inline=True
            )

            # Performance analysis with progress indicators
            embed.add_field(
                name="◆ TACTICAL ANALYSIS",
                value=dashboard['performance_analysis'],
                inline=True
            )

            # Classification and rank
            embed.add_field(
                name="◆ CLASSIFICATION",
                value=dashboard['classification'],
                inline=True
            )

            # Weapon proficiency
            favorite_weapon = embed_data.get('favorite_weapon', 'Unknown')
            weapon_kills = embed_data.get('weapon_kills', 0)
            longest_shot = embed_data.get('personal_best_distance', 0)

            weapon_display = f"**Primary:** {str(favorite_weapon)}\n**Eliminations:** {str(weapon_kills)}\n**Longest Shot:** {float(longest_shot):.0f}m"

            embed.add_field(
                name="◆ WEAPON MASTERY",
                value=weapon_display,
                inline=True
            )

            # Rivalry intelligence
            rivalry_data = embed_data.get('rivalry_data', {})
            if rivalry_data:
                nemesis = rivalry_data.get('nemesis', 'None')
                target = rivalry_data.get('primary_target', 'None')

                rivalry_display = f"**Primary Target:** {target}\n**Known Threat:** {nemesis}"
                embed.add_field(
                    name="◆ RIVALRY INTEL",
                    value=rivalry_display,
                    inline=True
                )

            # Operational status
            active_days = embed_data.get('active_days', 0)
            total_distance = embed_data.get('total_distance', 0)

            operational_display = f"**Days Active:** {str(active_days)}\n**Distance Traveled:** {float(total_distance):,.0f}m"
            embed.add_field(
                name="◆ OPERATIONAL STATUS",
                value=operational_display,
                inline=True
            )

            embed.set_footer(
                text="◆ Classified Intelligence • Emerald Tactical Division",
                icon_url="attachment://WeaponStats.png"
            )

            asset_file = discord.File("./assets/WeaponStats.png", filename="WeaponStats.png")
            embed.set_thumbnail(url="attachment://WeaponStats.png")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building advanced stats embed: {e}")
            return await EmbedFactory.build_error_embed("Stats system error")

    @staticmethod
    async def build_enhanced_killfeed_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build advanced killfeed with tactical reporting format"""
        try:
            killer = embed_data.get('killer', 'Unknown')
            victim = embed_data.get('victim', 'Unknown')
            weapon = embed_data.get('weapon', 'Unknown')
            distance = embed_data.get('distance', 0)
            is_suicide = embed_data.get('is_suicide', False)

            if is_suicide:
                if weapon.lower() in ['falling', 'fall', 'gravity']:
                    embed = discord.Embed(
                        title="◆ GRAVITY ENFORCEMENT PROTOCOL",
                        description="Altitude miscalculation resulted in terminal velocity impact",
                        color=EmbedFactory.COLORS['falling'],
                        timestamp=datetime.now(timezone.utc)
                    )

                    embed.add_field(
                        name="◆ OPERATIVE DESIGNATION",
                        value=f"**{killer}**",
                        inline=True
                    )

                    embed.add_field(
                        name="◆ INCIDENT CLASSIFICATION",
                        value="**FALLING** • Physics Lesson",
                        inline=True
                    )

                    embed.add_field(
                        name="◆ TACTICAL ASSESSMENT",
                        value="Environmental hazard claimed another combatant through gravitational forces",
                        inline=False
                    )
                else:
                    embed = discord.Embed(
                        title="◆ INTERNAL SYSTEM FAILURE",
                        description="Operator initiated emergency termination protocol",
                        color=EmbedFactory.COLORS['suicide'],
                        timestamp=datetime.now(timezone.utc)
                    )

                    embed.add_field(
                        name="◆ OPERATIVE DESIGNATION",
                        value=f"**{killer}**",
                        inline=True
                    )

                    embed.add_field(
                        name="◆ INCIDENT CLASSIFICATION", 
                        value="**SELF-TERMINATION** • Non-Combat Loss",
                        inline=True
                    )

                    embed.add_field(
                        name="◆ TACTICAL ASSESSMENT",
                        value="Strategic withdrawal via emergency protocols resulted in asset loss",
                        inline=False
                    )
            else:
                embed = discord.Embed(
                    title="◆ COMBAT SUPERIORITY CONFIRMED",
                    description="Target neutralization completed through tactical superiority",
                    color=EmbedFactory.COLORS['killfeed'],
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(
                    name="◆ ELIMINATOR",
                    value=f"**{killer}**",
                    inline=True
                )

                embed.add_field(
                    name="◆ TARGET ELIMINATED", 
                    value=f"**{victim}**",
                    inline=True
                )

                embed.add_field(
                    name="◆ ENGAGEMENT DETAILS",
                    value=f"**Weapon System:** {weapon}\n**Engagement Range:** {distance}m",
                    inline=False
                )

                # Distance classification
                if distance >= 500:
                    range_class = "Long Range Precision"
                elif distance >= 200:
                    range_class = "Medium Range Engagement"
                elif distance >= 50:
                    range_class = "Close Quarters Combat"
                else:
                    range_class = "Point Blank Execution"

                embed.add_field(
                    name="◆ TACTICAL CLASSIFICATION",
                    value=f"**{range_class}** • Professional elimination through superior positioning",
                    inline=False
                )

            embed.set_footer(
                text="◆ Combat Intelligence • Emerald Tactical Systems",
                icon_url="attachment://Killfeed.png"
            )

            asset_file = discord.File("./assets/Killfeed.png", filename="Killfeed.png")
            embed.set_thumbnail(url="attachment://Killfeed.png")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building enhanced killfeed embed: {e}")
            return await EmbedFactory.build_error_embed("Combat reporting system error")

    @staticmethod
    async def build_enhanced_mission_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build advanced mission briefing with threat assessment"""
        try:
            mission_id = embed_data.get('mission_id', '')
            state = embed_data.get('state', 'UNKNOWN')
            level = embed_data.get('level', 1)

            # Threat level visualization
            threat_indicators = {
                1: f"{EmbedFactory.THREAT_INDICATORS['low']} LOW THREAT",
                2: f"{EmbedFactory.THREAT_INDICATORS['medium']} MEDIUM THREAT", 
                3: f"{EmbedFactory.THREAT_INDICATORS['high']} HIGH THREAT",
                4: f"{EmbedFactory.THREAT_INDICATORS['critical']} CRITICAL THREAT"
            }

            threat_display = threat_indicators.get(level, f"{EmbedFactory.THREAT_INDICATORS['minimal']} UNKNOWN THREAT")

            if state == 'READY':
                embed = discord.Embed(
                    title="◆ CLASSIFIED OPERATION DECLASSIFIED",
                    description="High-priority mission parameters now available for elite operatives",
                    color=EmbedFactory.COLORS['mission'],
                    timestamp=datetime.now(timezone.utc)
                )
                status_display = "**READY FOR DEPLOYMENT** • Immediate Action Required"
            else:
                embed = discord.Embed(
                    title="◆ MISSION STATUS UPDATE",
                    description="Tactical situation evolving • Standby for further intelligence",
                    color=EmbedFactory.COLORS['info'],
                    timestamp=datetime.now(timezone.utc)
                )
                status_display = f"**{state.upper()}** • Monitoring"

            # Mission identification
            mission_name = EmbedFactory.normalize_mission_name(mission_id)
            embed.add_field(
                name="◆ TARGET DESIGNATION",
                value=f"**{mission_name}**",
                inline=True
            )

            # Threat assessment
            embed.add_field(
                name="◆ THREAT ASSESSMENT",
                value=threat_display,
                inline=True
            )

            # Operational status
            embed.add_field(
                name="◆ OPERATIONAL STATUS",
                value=status_display,
                inline=False
            )

            if state == 'READY':
                # Deployment briefing
                embed.add_field(
                    name="◆ DEPLOYMENT BRIEFING",
                    value="Elite operatives required for immediate tactical deployment • High-value rewards confirmed",
                    inline=False
                )

            embed.set_footer(
                text="◆ Mission Intelligence • Emerald Command Division",
                icon_url="attachment://Mission.png"
            )

            asset_file = discord.File("./assets/Mission.png", filename="Mission.png")
            embed.set_thumbnail(url="attachment://Mission.png")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building enhanced mission embed: {e}")
            return await EmbedFactory.build_error_embed("Mission system error")

    @staticmethod
    def normalize_mission_name(mission_id: str) -> str:
        """Convert mission ID to readable designation"""
        mission_mappings = {
            'GA_Airport_mis_01_SFPSACMission': 'Airport Tactical Zone Alpha',
            'GA_Airport_mis_02_SFPSACMission': 'Airport Tactical Zone Beta',
            'GA_Military_02_Mis1': 'Military Installation Bravo-2',
            'GA_Military_03_Mis_01': 'Military Installation Charlie-3',
            'GA_Bunker_01_Mis1': 'Underground Complex Designation Omega',
            'GA_Kamensk_Mis_1': 'Kamensk Urban Combat Zone'
        }
        return mission_mappings.get(mission_id, mission_id.replace('_', ' ').title())

    # Legacy compatibility method
    @staticmethod
    async def build(embed_type: str, embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Main build method with routing to enhanced embed types"""
        try:
            if embed_type == 'killfeed':
                return await EmbedFactory.build_enhanced_killfeed_embed(embed_data)
            elif embed_type == 'leaderboard':
                return await EmbedFactory.build_advanced_leaderboard_embed(embed_data)
            elif embed_type == 'stats':
                return await EmbedFactory.build_advanced_stats_embed(embed_data)
            elif embed_type == 'mission':
                return await EmbedFactory.build_enhanced_mission_embed(embed_data)
            else:
                # Fallback to existing methods for other types
                return await EmbedFactory.build_generic_embed(embed_data)
        except Exception as e:
            logger.error(f"Error building {embed_type} embed: {e}")
            return await EmbedFactory.build_error_embed(f"System error in {embed_type} module")

    @staticmethod
    async def build_generic_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Enhanced generic embed with professional formatting"""
        try:
            embed = discord.Embed(
                title=f"◆ {embed_data.get('title', 'EMERALD TACTICAL SYSTEMS')}",
                description=f"**{embed_data.get('description', 'Elite gaming network notification')}**",
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_footer(
                text="◆ Powered by Emerald Tactical Division",
                icon_url="attachment://main.png"
            )

            asset_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building generic embed: {e}")
            return await EmbedFactory.build_error_embed("Generic system error")

    @staticmethod
    async def build_error_embed(error_message: str) -> tuple[discord.Embed, discord.File]:
        """Enhanced error reporting with professional formatting"""
        try:
            embed = discord.Embed(
                title="◆ SYSTEM DIAGNOSTIC ALERT",
                description=f"**Critical system malfunction detected:** {error_message}",
                color=EmbedFactory.COLORS['error'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(
                name="◆ STATUS CLASSIFICATION",
                value="**OPERATION FAILED** • Immediate Attention Required",
                inline=True
            )

            embed.add_field(
                name="◆ RECOMMENDED ACTION",
                value="**DIAGNOSTIC PROTOCOL** • Technical Investigation",
                inline=True
            )

            embed.set_footer(
                text="◆ System Diagnostics • Emerald Technical Division",
                icon_url="attachment://main.png"
            )

            asset_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Critical error in error embed creation: {e}")
            # Ultimate fallback
            simple_embed = discord.Embed(
                title="◆ CRITICAL SYSTEM FAILURE",
                description="Multiple system malfunctions detected",
                color=0xFF0000,
                timestamp=datetime.now(timezone.utc)
            )
            try:
                fallback_file = discord.File("./assets/main.png", filename="main.png")
                return simple_embed, fallback_file
            except:
                return simple_embed, None

    ASSETS_PATH = Path('./assets')

    CONNECTION_TITLES = [
        "🔷 **REINFORCEMENTS ARRIVE**",
        "🔷 **OPERATIVE DEPLOYED**", 
        "🔷 **COMBATANT ONLINE**",
        "🔷 **WARRIOR ACTIVE**",
        "🔷 **ASSET MOBILIZED**"
    ]

    CONNECTION_DESCRIPTIONS = [
        "New player has joined the server",
        "Elite operative enters the battlefield",
        "Combat asset successfully deployed",
        "Legendary warrior joins the fight",
        "Tactical reinforcement activated"
    ]

    DISCONNECTION_TITLES = [
        "🔻 **EXTRACTION CONFIRMED**",
        "🔻 **OPERATIVE WITHDRAWN**",
        "🔻 **COMBAT COMPLETE**", 
        "🔻 **MISSION CONCLUDED**",
        "🔻 **ASSET OFFLINE**"
    ]

    DISCONNECTION_DESCRIPTIONS = [
        "Player has left the server",
        "Operative extraction successful",
        "Combat mission concluded",
        "Tactical withdrawal completed",
        "Asset deactivated from sector"
    ]

    MISSION_READY_TITLES = [
        "**CLASSIFIED OPERATION DECLASSIFIED**",
        "**HIGH-VALUE TARGET ACQUIRED**", 
        "**ELIMINATION CONTRACT ACTIVE**",
        "**DEATH WARRANT AUTHORIZATION**",
        "**BLADE PROTOCOL ENGAGED**",
        "**ELITE MISSION PARAMETERS**",
        "**LEGENDARY OBJECTIVE AVAILABLE**",
        "**DIAMOND TIER OPERATION**",
        "**COMMANDER'S SPECIAL ASSIGNMENT**",
        "**CHAMPIONSHIP ELIMINATION ROUND**"
    ]

    MISSION_READY_DESCRIPTIONS = [
        "**CRITICAL PRIORITY** • Elite operatives required for high-stakes engagement",
        "**MAXIMUM THREAT LEVEL** • Only the deadliest warriors need apply", 
        "**EXPLOSIVE OPPORTUNITY** • Massive rewards await skilled tacticians",
        "**PRECISION STRIKE REQUIRED** • Legendary marksmen to the front lines",
        "**LIGHTNING OPERATION** • Swift execution demanded for success",
        "**INFERNO PROTOCOL** • Enter the flames and emerge victorious",
        "**DEATH'S EMBRACE** • Where angels fear to tread, legends are born",
        "**STELLAR MISSION** • Reach for the stars through fields of fire",
        "**DIAMOND STANDARD** • Only perfection survives this crucible",
        "**CHAMPIONSHIP TIER** • Prove your worth among immortals"
    ]

    KILL_TITLES = [
        "**COMBAT SUPERIORITY ACHIEVED**",
        "**TARGET NEUTRALIZATION COMPLETE**",
        "**PRECISION ELIMINATION CONFIRMED**",
        "**TACTICAL DOMINANCE DISPLAYED**",
        "**LIGHTNING STRIKE EXECUTED**",
        "**MASTERCLASS ELIMINATION**",
        "**LEGENDARY TAKEDOWN**",
        "**CHAMPIONSHIP KILL**",
        "**BLADE DANCE FINALE**",
        "**ROYAL EXECUTION**"
    ]

    KILL_MESSAGES = [
        "Another heartbeat silenced beneath the ash sky",
        "No burial, no name — just silence where a soul once stood",
        "Left no echo. Just scattered gear and cooling blood",
        "Cut from the world like thread from a fraying coat",
        "Hunger, cold, bullets — it could've been any of them. It was enough",
        "Marked, hunted, forgotten. In that order",
        "Their fire went out before they even knew they were burning",
        "A last breath swallowed by wind and war",
        "The price of survival paid in someone else's blood",
        "The map didn't change. The player did"
    ]

    SUICIDE_TITLES = [
        "**CRITICAL SYSTEM FAILURE**",
        "**TACTICAL ERROR FATAL**",
        "**OPERATION SELF-DESTRUCT**",
        "**MISSION COMPROMISED**",
        "**EMERGENCY PROTOCOL ACTIVATED**",
        "**SYSTEM OVERLOAD CRITICAL**",
        "**MELTDOWN SEQUENCE COMPLETE**",
        "**OPERATOR DOWN - INTERNAL**",
        "**CHAOS THEORY IN ACTION**",
        "**TRAGIC PERFORMANCE**"
    ]

    SUICIDE_MESSAGES = [
        "Hit relocate like it was the snooze button. Got deleted",
        "Tactical redeployment... into the abyss",
        "Rage respawned and logic respawned with it",
        "Wanted a reset. Got a reboot straight to the void",
        "Pressed something. Paid everything",
        "Who needs enemies when you've got bad decisions?",
        "Alt+F4'd themselves into Valhalla",
        "Strategic death — poorly executed",
        "Fast travel without a destination",
        "Confirmed: the dead menu is not a safe zone"
    ]

    FALLING_TITLES = [
        "**GRAVITY ENFORCEMENT PROTOCOL**",
        "**ALTITUDE ADJUSTMENT FATAL**",
        "**TERMINAL VELOCITY ACHIEVED**",
        "**GROUND IMPACT CONFIRMED**",
        "**ELEVATION ERROR CORRECTED**",
        "**PHYSICS LESSON CONCLUDED**",
        "**DESCENT PROTOCOL FAILED**",
        "**VERTICAL MISCALCULATION**",
        "**FLIGHT PLAN TERMINATED**",
        "**LANDING COORDINATES INCORRECT**"
    ]

    FALLING_MESSAGES = [
        "Thought they could make it. The ground disagreed",
        "Airborne ambition. Terminal results",
        "Tried flying. Landed poorly",
        "Gravity called. They answered — headfirst",
        "Believed in themselves. Gravity didn't",
        "From rooftops to regret in under two seconds",
        "The sky opened. The floor closed",
        "Survival instincts took a coffee break",
        "Feet first into a bad decision",
        "Their plan had one fatal step too many"
    ]

    AIRDROP_TITLES = [
        "**TACTICAL SUPPLY DEPLOYMENT**",
        "**HIGH-VALUE CARGO INBOUND**",
        "**GIFT FROM THE GODS**",
        "**TREASURE CHEST DESCENDING**",
        "**LEGENDARY LOOT PACKAGE**",
        "**CHAMPIONSHIP REWARDS**",
        "**LIGHTNING DELIVERY**",
        "**INFERNO SUPPLIES**",
        "**ROYAL CARE PACKAGE**",
        "**PRECISION DROP ZONE**"
    ]

    HELICRASH_TITLES = [
        "**BIRD OF STEEL GROUNDED**",
        "**AVIATION CATASTROPHE**",
        "**MECHANICAL PHOENIX DOWN**",
        "**SKY CHARIOT TERMINATED**",
        "**IRON ANGEL FALLEN**",
        "**STELLAR CRASH LANDING**",
        "**PRECIOUS METAL SCATTERED**",
        "**CHAMPIONSHIP WRECKAGE**",
        "**TARGET PRACTICE COMPLETE**",
        "**ROYAL AIRCRAFT DOWN**"
    ]

    TRADER_TITLES = [
        "**BLACK MARKET MAGNATE**",
        "**SHADOW MERCHANT PRINCE**",
        "**DIAMOND DEALER ACTIVE**",
        "**CHAMPIONSHIP TRADER**",
        "**LIGHTNING MERCHANT**",
        "**INFERNO BUSINESSMAN**",
        "**STELLAR SALESMAN**",
        "**ROYAL ARMS DEALER**",
        "**PRECISION SUPPLIER**",
        "**DEATH'S QUARTERMASTER**"
    ]

    MISSION_MAPPINGS = {
        'GA_Airport_mis_01_SFPSACMission': 'Airport Mission #1',
        'GA_Airport_mis_02_SFPSACMission': 'Airport Mission #2',
        'GA_Airport_mis_03_SFPSACMission': 'Airport Mission #3',
        'GA_Airport_mis_04_SFPSACMission': 'Airport Mission #4',
        'GA_Military_02_Mis1': 'Military Base Mission #2',
        'GA_Military_03_Mis_01': 'Military Base Mission #3',
        'GA_Military_04_Mis1': 'Military Base Mission #4',
        'GA