"""
Kathara Circuit Plugin for Nous Hermes & Autonomous Multi-Agent Frameworks.

Decomposes monolithic LLM prompt collapse into an executable 12-Sphere
subagent circuit board with real-time visual route deliberation.
"""

__version__ = "1.0.0"
__author__ = "Beto Group // Kathara Architecture Team"

from .client import KatharaClient
from .plugin import HermesKatharaPlugin
from .circuit import KatharaCircuitRunner
from .bounty_hunter import HermesBountyHunter

__all__ = [
    "KatharaClient",
    "HermesKatharaPlugin",
    "KatharaCircuitRunner",
    "HermesBountyHunter",
]

