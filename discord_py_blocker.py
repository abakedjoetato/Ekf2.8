
"""
Discord.py Import Blocker - Enhanced Version
Blocks discord.py while allowing py-cord 2.6.1
"""

import sys
import importlib.util
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, Loader
import logging

logger = logging.getLogger(__name__)

class DiscordPyBlocker(MetaPathFinder, Loader):
    """Meta path finder that blocks discord.py imports while allowing py-cord"""
    
    def __init__(self):
        self.blocked_modules = {
            'discord.py',
            'discord_py'
        }
        # Don't block these - they're part of py-cord
        self.allowed_modules = {
            'discord',
            'discord.ext',
            'discord.ext.commands',
            'discord.ext.bridge',  # This is py-cord functionality
            'discord.ext.pages',
            'discord.ext.menus',
            'discord.ext.tasks',
            'discord.ui',
            'discord.utils',
            'discord.voice_client',
            'discord.webhook'
        }
    
    def find_spec(self, fullname, path, target=None):
        # Allow all py-cord modules
        if any(fullname.startswith(allowed) for allowed in self.allowed_modules):
            return None  # Let normal import mechanism handle it
        
        # Block discord.py specific modules
        if any(blocked in fullname for blocked in self.blocked_modules):
            logger.warning(f"🚫 Blocked discord.py import: {fullname}")
            raise ImportError(f"discord.py import '{fullname}' blocked. Use py-cord 2.6.1 instead: pip install py-cord==2.6.1")
        
        return None  # Let normal import mechanism handle other modules
    
    def create_module(self, spec):
        return None
    
    def exec_module(self, module):
        pass

# Install the blocker only if discord.py is detected
def install_discord_py_blocker():
    """Install the discord.py blocker"""
    try:
        # Check if discord.py is installed (not py-cord)
        import discord
        
        # If we can import discord and it has __version__, check if it's discord.py
        if hasattr(discord, '__version__'):
            version = discord.__version__
            logger.info(f"Discord library version detected: {version}")
            
            # py-cord versions are typically 2.x.x, discord.py is 1.x.x or 2.x.x but different
            # For safety, only block if we detect specific discord.py patterns
            if any(pattern in str(discord.__file__) for pattern in ['discord.py', 'discord_py']):
                logger.warning("🚫 discord.py detected, installing blocker")
                blocker = DiscordPyBlocker()
                if blocker not in sys.meta_path:
                    sys.meta_path.insert(0, blocker)
                    logger.info("✅ Discord.py blocker installed")
            else:
                logger.info("✅ py-cord detected, no blocking needed")
        else:
            logger.info("✅ Discord library appears to be py-cord")
            
    except ImportError:
        logger.info("No discord library found")
    except Exception as e:
        logger.error(f"Error checking discord library: {e}")

# Only install blocker if needed
if __name__ == "__main__":
    install_discord_py_blocker()
else:
    # Don't auto-install the blocker since py-cord is working
    logger.info("✅ Discord.py blocker available but not needed (py-cord is working)")
