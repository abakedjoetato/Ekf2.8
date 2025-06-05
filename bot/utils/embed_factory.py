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
            'primary_stats': f"**Eliminations:** {kills:,}\n**Casualties:** {deaths:,}\n**K/D Ratio:** {kdr:.2f}",
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

            weapon_display = f"**Primary:** {favorite_weapon}\n**Eliminations:** {weapon_kills}\n**Longest Shot:** {longest_shot:.0f}m"

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

            operational_display = f"**Days Active:** {active_days}\n**Distance Traveled:** {total_distance:,.0f}m"
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
        'GA_Beregovoy_Mis1': 'Beregovoy Settlement Mission',
        'GA_Settle_05_ChernyLog_Mis1': 'Cherny Log Settlement Mission',
        'GA_Ind_01_m1': 'Industrial Zone Mission #1',
        'GA_Ind_02_Mis_1': 'Industrial Zone Mission #2',
        'GA_KhimMash_Mis_01': 'Chemical Plant Mission #1',
        'GA_KhimMash_Mis_02': 'Chemical Plant Mission #2',
        'GA_Bunker_01_Mis1': 'Underground Bunker Mission',
        'GA_Sawmill_01_Mis1': 'Sawmill Mission #1',
        'GA_Settle_09_Mis_1': 'Settlement Mission #9',
        'GA_Military_04_Mis_2': 'Military Base Mission #4B',
        'GA_PromZone_6_Mis_1': 'Industrial Zone Mission #6',
        'GA_PromZone_Mis_01': 'Industrial Zone Mission A',
        'GA_PromZone_Mis_02': 'Industrial Zone Mission B',
        'GA_Kamensk_Ind_3_Mis_1': 'Kamensk Industrial Mission',
        'GA_Kamensk_Mis_1': 'Kamensk City Mission #1',
        'GA_Kamensk_Mis_2': 'Kamensk City Mission #2',
        'GA_Kamensk_Mis_3': 'Kamensk City Mission #3',
        'GA_Krasnoe_Mis_1': 'Krasnoe City Mission',
        'GA_Vostok_Mis_1': 'Vostok City Mission',
        'GA_Lighthouse_02_Mis1': 'Lighthouse Mission #2',
        'GA_Elevator_Mis_1': 'Elevator Complex Mission #1',
        'GA_Elevator_Mis_2': 'Elevator Complex Mission #2',
        'GA_Sawmill_02_1_Mis1': 'Sawmill Mission #2A',
        'GA_Sawmill_03_Mis_01': 'Sawmill Mission #3',
        'GA_Bochki_Mis_1': 'Barrel Storage Mission',
        'GA_Dubovoe_0_Mis_1': 'Dubovoe Resource Mission',
    }

    @staticmethod
    def get_thumbnail_for_type(embed_type: str) -> Tuple[str, str]:
        """Get correct thumbnail file and filename for embed type"""
        
        thumbnail_mappings = {
            'killfeed': 'Killfeed.png',
            'suicide': 'Killfeed.png', 
            'falling': 'Killfeed.png',
            'connection': 'Connections.png',
            'mission': 'Mission.png',
            'airdrop': 'Airdrop.png',
            'helicrash': 'Helicrash.png',
            'trader': 'Trader.png',
            'vehicle': 'Killfeed.png',
            'leaderboard': 'Leaderboard.png',
            'stats': 'WeaponStats.png',
            'bounty': 'Bounty.png',
            'faction': 'Faction.png',
            'gambling': 'Gamble.png',
            'economy': 'main.png',
            'work': 'main.png',
            'balance': 'main.png',
            'premium': 'main.png',
            'profile': 'main.png', 
            'admin': 'main.png',
            'error': 'main.png',
            'success': 'main.png',
            'info': 'main.png'
        }
        
        thumbnail = thumbnail_mappings.get(embed_type.lower(), 'main.png')
        return f"./assets/{thumbnail}", thumbnail

    @staticmethod
    def get_mission_level(mission_id: str) -> int:
        """Determine mission difficulty level"""
        if any(x in mission_id.lower() for x in ['airport', 'military', 'bunker']):
            return 4  # High difficulty
        elif any(x in mission_id.lower() for x in ['industrial', 'chemical', 'kamensk']):
            return 3  # Medium-high difficulty
        elif any(x in mission_id.lower() for x in ['settlement', 'sawmill']):
            return 2  # Medium difficulty
        else:
            return 1  # Low difficulty

    @staticmethod
    def get_threat_level_display(level: int) -> str:
        """Get enhanced threat level display"""
        threat_displays = {
            1: "**LOW THREAT** - Rookie Operations",
            2: "**MEDIUM THREAT** - Veteran Required", 
            3: "**HIGH THREAT** - Elite Operatives Only",
            4: "**CRITICAL THREAT** - Legendary Masters"
        }
        return threat_displays.get(level, "**UNKNOWN THREAT** - Proceed with Caution")

    @staticmethod
    async def build_connection_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build minimalistic connection embed - 2 FIELDS ONLY"""
        try:
            title = embed_data.get('title', random.choice(EmbedFactory.CONNECTION_TITLES))
            description = embed_data.get('description', random.choice(EmbedFactory.CONNECTION_DESCRIPTIONS))

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['connection'],
                timestamp=datetime.now(timezone.utc)
            )

            player_name = embed_data.get('player_name', 'Unknown Player')
            platform = embed_data.get('platform', 'Unknown')
            server_name = embed_data.get('server_name', 'Unknown Server')

            embed.add_field(name="**OPERATIVE**", value=f"**{player_name}**\n**{platform}** • **{server_name}**", inline=True)
            embed.add_field(name="**STATUS**", value="**ACTIVE** • Ready for Combat", inline=True)

            embed.set_footer(text="Powered by Emerald")

            connections_file = discord.File("./assets/Connections.png", filename="Connections.png")
            embed.set_thumbnail(url="attachment://Connections.png")

            return embed, connections_file

        except Exception as e:
            logger.error(f"Error building connection embed: {e}")
            return await EmbedFactory.build_error_embed("Connection embed error")

    @staticmethod
    async def build_disconnection_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build minimalistic disconnection embed - 2 FIELDS ONLY"""
        try:
            title = embed_data.get('title', random.choice(EmbedFactory.DISCONNECTION_TITLES))
            description = embed_data.get('description', random.choice(EmbedFactory.DISCONNECTION_DESCRIPTIONS))

            embed = discord.Embed(
                title=title,
                description=description,
                color=0xDC143C,  # Crimson red for disconnections
                timestamp=datetime.now(timezone.utc)
            )

            player_name = embed_data.get('player_name', 'Unknown Player')
            platform = embed_data.get('platform', 'Unknown')
            server_name = embed_data.get('server_name', 'Unknown Server')

            embed.add_field(name="**OPERATIVE**", value=f"**{player_name}**\n**{platform}** • **{server_name}**", inline=True)
            embed.add_field(name="**STATUS**", value="**OFFLINE** • Mission Complete", inline=True)

            embed.set_footer(text="Powered by Emerald")

            connections_file = discord.File("./assets/Connections.png", filename="Connections.png")
            embed.set_thumbnail(url="attachment://Connections.png")

            return embed, connections_file

        except Exception as e:
            logger.error(f"Error building disconnection embed: {e}")
            return await EmbedFactory.build_error_embed("Disconnection embed error")

    @staticmethod
    async def build_mission_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build elite mission embed - MINIMALISTIC 3 FIELDS"""
        try:
            mission_id = embed_data.get('mission_id', '')
            state = embed_data.get('state', 'UNKNOWN')
            level = embed_data.get('level', 1)

            if state == 'READY':
                title = random.choice(EmbedFactory.MISSION_READY_TITLES)
                description = random.choice(EmbedFactory.MISSION_READY_DESCRIPTIONS)
                color = EmbedFactory.COLORS['mission']
                status_display = "**READY** • Awaiting Deployment"
            else:
                title = "**MISSION STATUS UPDATE**"
                description = "**TACTICAL SITUATION EVOLVING** • Stand by for further orders"
                color = EmbedFactory.COLORS['info']
                status_display = f"**{state}** • Updating"

            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            mission_name = EmbedFactory.normalize_mission_name(mission_id)
            threat_display = EmbedFactory.get_threat_level_display(level)

            embed.add_field(name="**TARGET DESIGNATION**", value=f"**{mission_name}**\n{threat_display}", inline=False)
            embed.add_field(name="**STATUS**", value=status_display, inline=True)

            if state == 'READY':
                embed.add_field(name="**DEPLOYMENT ORDERS**", value="Deploy immediately • High-value rewards await brave operatives", inline=False)

            embed.set_footer(text="Powered by Emerald")

            mission_file = discord.File("./assets/Mission.png", filename="Mission.png")
            embed.set_thumbnail(url="attachment://Mission.png")

            return embed, mission_file

        except Exception as e:
            logger.error(f"Error building mission embed: {e}")
            return await EmbedFactory.build_error_embed("Mission embed error")

    @staticmethod
    async def build_airdrop_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build elite airdrop embed - MINIMALISTIC 3 FIELDS"""
        try:
            title = random.choice(EmbedFactory.AIRDROP_TITLES)
            description = "**High-value military assets incoming**"

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['airdrop'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**LEGENDARY TIER**", value="Premium equipment and tactical resources", inline=False)
            embed.add_field(name="**INBOUND** • Limited Time", value="High competition expected from hostile operatives", inline=False)

            embed.set_footer(text="Powered by Emerald")

            airdrop_file = discord.File("./assets/Airdrop.png", filename="Airdrop.png")
            embed.set_thumbnail(url="attachment://Airdrop.png")

            return embed, airdrop_file

        except Exception as e:
            logger.error(f"Error building airdrop embed: {e}")
            return await EmbedFactory.build_error_embed("Airdrop embed error")

    @staticmethod
    async def build_helicrash_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build elite helicrash embed - MINIMALISTIC 3 FIELDS"""
        try:
            title = random.choice(EmbedFactory.HELICRASH_TITLES)
            description = "**Salvage opportunity in hostile territory**"

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['helicrash'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**MILITARY GRADE**", value="High-value military equipment available", inline=False)
            embed.add_field(name="**SITE LOCATED** • Dangerous", value="Hot zone active with confirmed hostile presence", inline=False)

            embed.set_footer(text="Powered by Emerald")

            helicrash_file = discord.File("./assets/Helicrash.png", filename="Helicrash.png")
            embed.set_thumbnail(url="attachment://Helicrash.png")

            return embed, helicrash_file

        except Exception as e:
            logger.error(f"Error building helicrash embed: {e}")
            return await EmbedFactory.build_error_embed("Helicrash embed error")

    @staticmethod
    async def build_trader_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build elite trader embed - MINIMALISTIC 3 FIELDS"""
        try:
            title = random.choice(EmbedFactory.TRADER_TITLES)
            description = "**Rare commodities available for trade**"

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['trader'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**ROYAL GRADE**", value="Premium equipment and rare commodities", inline=False)
            embed.add_field(name="**ACTIVE** • Open for Business", value="Verified trader with exclusive deals on high-tier equipment", inline=False)

            embed.set_footer(text="Powered by Emerald")

            trader_file = discord.File("./assets/Trader.png", filename="Trader.png")
            embed.set_thumbnail(url="attachment://Trader.png")

            return embed, trader_file

        except Exception as e:
            logger.error(f"Error building trader embed: {e}")
            return await EmbedFactory.build_error_embed("Trader embed error")

    @staticmethod
    async def build_bounty_set_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build enhanced bounty set embed - MINIMALISTIC 3 FIELDS"""
        try:
            title = "**ELIMINATION CONTRACT ISSUED**"
            description = f"**High-value target designated**"

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['bounty'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**TARGET**", value=f"**{embed_data['target_character']}**", inline=True)
            embed.add_field(name="**REWARD**", value=f"**${embed_data['bounty_amount']:,}**", inline=True)
            embed.add_field(name="**EXPIRES** • <t:{embed_data['expires_timestamp']}:R>", value="Eliminate target to claim bounty immediately", inline=False)

            embed.set_footer(text="Powered by Emerald")

            bounty_file = discord.File("./assets/Bounty.png", filename="Bounty.png")
            embed.set_thumbnail(url="attachment://Bounty.png")

            return embed, bounty_file

        except Exception as e:
            logger.error(f"Error building bounty set embed: {e}")
            return await EmbedFactory.build_error_embed("Bounty set embed error")

    @staticmethod
    async def build_bounty_list_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build enhanced bounty list embed - MINIMALISTIC 3 FIELDS"""
        try:
            embed = discord.Embed(
                title="**ACTIVE ELIMINATION CONTRACTS**",
                description=f"**{embed_data['total_bounties']}** high-value targets identified",
                color=EmbedFactory.COLORS['bounty'],
                timestamp=datetime.now(timezone.utc)
            )

            bounty_list = []
            for i, bounty in enumerate(embed_data['bounty_list'][:5], 1):  # Show max 5
                target = bounty['target_character']
                amount = bounty['amount']
                auto_indicator = " Auto" if bounty and bounty.get('auto_generated', False) else ""
                bounty_list.append(f"**{i}. {target}** - **${amount:,}**{auto_indicator}")

            embed.add_field(name="**TOP CONTRACTS**", value="\n".join(bounty_list), inline=False)
            embed.add_field(name="**PRIORITY STATUS**", value="Showing highest value targets available", inline=False)

            embed.set_footer(text="Powered by Emerald")

            bounty_file = discord.File("./assets/Bounty.png", filename="Bounty.png")
            embed.set_thumbnail(url="attachment://Bounty.png")

            return embed, bounty_file

        except Exception as e:
            logger.error(f"Error building bounty list embed: {e}")
            return await EmbedFactory.build_error_embed("Bounty list embed error")

    @staticmethod
    async def build_faction_created_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build enhanced faction created embed - MINIMALISTIC 3 FIELDS"""
        try:
            embed = discord.Embed(
                title="**FACTION ESTABLISHED**",
                description="**New military organization formed**",
                color=EmbedFactory.COLORS['success'],
                timestamp=datetime.now(timezone.utc)
            )

            faction_tag = f"**[{embed_data['faction_tag']}]**" if embed_data and embed_data.get('faction_tag') else ""
            embed.add_field(name="**ORGANIZATION**", value=f"**{embed_data['faction_name']}**\n**{embed_data['leader']}** • {faction_tag}", inline=False)

            embed.add_field(name="**ROSTER**", value=f"**{embed_data['member_count']}/{embed_data['max_members']}** Members • Active", inline=True)
            embed.add_field(name="**RECRUITMENT**", value="Use /faction invite to recruit skilled operatives", inline=False)

            embed.set_footer(text="Powered by Emerald")

            faction_file = discord.File("./assets/Faction.png", filename="Faction.png")
            embed.set_thumbnail(url="attachment://Faction.png")

            return embed, faction_file

        except Exception as e:
            logger.error(f"Error building faction created embed: {e}")
            return await EmbedFactory.build_error_embed("Faction creation embed error")

    @staticmethod
    async def build_economy_balance_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build enhanced economy balance embed - MINIMALISTIC 3 FIELDS"""
        try:
            embed = discord.Embed(
                title="**FINANCIAL STATUS REPORT**",
                description="**Economic portfolio overview**",
                color=EmbedFactory.COLORS['economy'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**OPERATIVE**", value=f"**{embed_data['user_name']}**", inline=False)
            embed.add_field(name="**CURRENT BALANCE**", value=f"**${embed_data['balance']:,}**", inline=True)

            net_worth = embed_data['total_earned'] - embed_data['total_spent']
            embed.add_field(name="**FINANCIAL ANALYSIS**", value=f"**${embed_data['total_earned']:,}** Total Earned • **${embed_data['total_spent']:,}** Total Spent\n**${net_worth:,}** Net Worth • **Excellent** Credit Rating", inline=False)

            embed.set_footer(text="Powered by Emerald")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building economy balance embed: {e}")
            return await EmbedFactory.build_error_embed("Economy balance embed error")

    @staticmethod
    async def build_economy_work_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build enhanced economy work embed - MINIMALISTIC 3 FIELDS"""
        try:
            embed = discord.Embed(
                title="**MISSION COMPLETED**",
                description=f"**{embed_data['scenario']}**",
                color=EmbedFactory.COLORS['success'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="**COMPENSATION**", value=f"**+${embed_data['earnings']:,}**", inline=True)
            embed.add_field(name="**NEXT ASSIGNMENT**", value="**Available in 1 hour**", inline=True)
            embed.add_field(name="**PERFORMANCE**", value="**Excellent** • Above Standard • Contract Work", inline=False)

            embed.set_footer(text="Powered by Emerald")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building economy work embed: {e}")
            return await EmbedFactory.build_error_embed("Economy work embed error")

    @staticmethod
    def create_mission_embed(title: str, description: str, mission_id: str, level: int, state: str, respawn_time: Optional[int] = None) -> discord.Embed:
        """Create mission embed (legacy compatibility)"""
        try:
            if state == 'READY':
                color = EmbedFactory.COLORS['mission']
            elif state == 'IN_PROGRESS':
                color = 0xFFAA00
            elif state == 'COMPLETED':
                color = EmbedFactory.COLORS['success']
            else:
                color = EmbedFactory.COLORS['info']

            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            mission_name = EmbedFactory.normalize_mission_name(mission_id)
            embed.add_field(name="Mission", value=mission_name, inline=False)

            threat_levels = ["Low", "Medium", "High", "Critical"]
            threat_level = threat_levels[min(level-1, 3)] if level > 0 else "Unknown"
            embed.add_field(name="Threat Level", value=f"Class {level} - {threat_level}", inline=True)
            embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)

            if respawn_time:
                embed.add_field(name="Respawn", value=f"{respawn_time}s", inline=True)

            embed.set_footer(text="Powered by Emerald")
            embed.set_thumbnail(url="attachment://Mission.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating mission embed: {e}")
            return discord.Embed(title="Error", description="Failed to create mission embed", color=0xFF0000)

    @staticmethod
    def create_airdrop_embed(state: str, location: str, timestamp: datetime) -> discord.Embed:
        """Create airdrop embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="🪂 Airdrop Incoming",
                description="High-value supply drop detected inbound",
                color=EmbedFactory.COLORS['airdrop'],
                timestamp=timestamp
            )

            embed.add_field(name="Drop Zone", value=location, inline=True)
            embed.add_field(name="Status", value=state.title(), inline=True)
            embed.add_field(name="Contents", value="High-Value Loot", inline=True)

            embed.set_footer(text="Powered by Emerald")
            embed.set_thumbnail(url="attachment://Airdrop.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating airdrop embed: {e}")
            return discord.Embed(title="Error", description="Failed to create airdrop embed", color=0xFF0000)

    @staticmethod
    def create_helicrash_embed(location: str, timestamp: datetime) -> discord.Embed:
        """Create helicrash embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="🚁 Helicopter Crash",
                description="Military helicopter has crashed - salvage opportunity detected",
                color=EmbedFactory.COLORS['helicrash'],
                timestamp=timestamp
            )

            embed.add_field(name="Crash Site", value=location, inline=True)
            embed.add_field(name="Status", value="Active", inline=True)
            embed.add_field(name="Loot Type", value="Military Equipment", inline=True)

            embed.set_footer(text="Powered by Emerald")
            embed.set_thumbnail(url="attachment://Helicrash.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating helicrash embed: {e}")
            return discord.Embed(title="Error", description="Failed to create helicrash embed", color=0xFF0000)

    @staticmethod
    def create_trader_embed(location: str, timestamp: datetime) -> discord.Embed:
        """Create trader embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="Trader Arrival",
                description="Traveling merchant has arrived with rare goods",
                color=EmbedFactory.COLORS['trader'],
                timestamp=timestamp
            )

            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Status", value="Open for Business", inline=True)
            embed.add_field(name="Inventory", value="Rare Items Available", inline=True)

            embed.set_footer(text="Powered by Emerald")
            embed.set_thumbnail(url="attachment://Trader.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating trader embed: {e}")
            return discord.Embed(title="Error", description="Failed to create trader embed", color=0xFF0000)

    @staticmethod
    def create_player_connect_embed(event_data: Dict[str, Any]) -> discord.Embed:
        """Create player connection embed for unified parser"""
        try:
            embed = discord.Embed(
                title="🟢 Player Connected",
                description=f"**{event_data.get('player_name', 'Unknown')}** joined the server",
                color=0x00FF00,
                timestamp=datetime.now(timezone.utc)
            )
            
            eos_id = event_data.get('eos_id', 'Unknown')
            server_name = event_data.get('server_name', 'Unknown Server')
            
            embed.add_field(name="EOS ID", value=f"`{eos_id[:16]}...`", inline=True)
            embed.add_field(name="Server", value=server_name, inline=True)
            embed.set_footer(text="Powered by Emerald")
            
            return embed
            
        except Exception as e:
            logger.error(f"Error creating player connect embed: {e}")
            return discord.Embed(title="Error", description="Failed to create connection embed", color=0xFF0000)

    @staticmethod
    def create_player_disconnect_embed(event_data: Dict[str, Any]) -> discord.Embed:
        """Create player disconnection embed for unified parser"""
        try:
            embed = discord.Embed(
                title="🔴 Player Disconnected",
                description=f"**{event_data.get('player_name', 'Unknown')}** left the server",
                color=0xFF0000,
                timestamp=datetime.now(timezone.utc)
            )
            
            eos_id = event_data.get('eos_id', 'Unknown')
            server_name = event_data.get('server_name', 'Unknown Server')
            
            embed.add_field(name="EOS ID", value=f"`{eos_id[:16]}...`", inline=True)
            embed.add_field(name="Server", value=server_name, inline=True)
            embed.set_footer(text="Powered by Emerald")
            
            return embed
            
        except Exception as e:
            logger.error(f"Error creating player disconnect embed: {e}")
            return discord.Embed(title="Error", description="Failed to create disconnection embed", color=0xFF0000)

    @staticmethod
    def create_event_embed(event_data: Dict[str, Any]) -> discord.Embed:
        """Create game event embed for unified parser"""
        try:
            event_type = event_data.get('event')
            
            if event_type == 'mission_start':
                embed = discord.Embed(
                    title="🎯 Mission Started",
                    description=f"Mission **{event_data.get('mission_name', 'Unknown')}** is now active",
                    color=0x00FF00,
                    timestamp=datetime.now(timezone.utc)
                )
            elif event_type == 'mission_end':
                embed = discord.Embed(
                    title="🎯 Mission Ended", 
                    description=f"Mission **{event_data.get('mission_name', 'Unknown')}** has ended",
                    color=0xFF0000,
                    timestamp=datetime.now(timezone.utc)
                )
            elif event_type == 'airdrop':
                embed = discord.Embed(
                    title="📦 Airdrop Event",
                    description="Supply drop incoming with valuable loot",
                    color=0x00BFFF,
                    timestamp=datetime.now(timezone.utc)
                )
            elif event_type == 'trader':
                embed = discord.Embed(
                    title="🛒 Trader Event",
                    description="Traveling merchant has arrived",
                    color=0xFF6B35,
                    timestamp=datetime.now(timezone.utc)
                )
            else:
                embed = discord.Embed(
                    title="🎮 Server Event",
                    description=f"Event: {event_type}",
                    color=0x7289DA,
                    timestamp=datetime.now(timezone.utc)
                )
            
            embed.set_footer(text="Powered by Emerald")
            return embed
            
        except Exception as e:
            logger.error(f"Error creating event embed: {e}")
            return discord.Embed(title="Error", description="Failed to create event embed", color=0xFF0000)