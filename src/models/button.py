#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎛️ Button Model Module
Defines the core button mapping structure for the Launchpad controller.
"""

from dataclasses import dataclass
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

@dataclass
class LaunchpadButton:
    """📍 Represents a physical button on the Launchpad"""
    x: int
    y: int
    color: int
    note: Optional[int] = None
    press_count: int = 0
    alias: Optional[str] = None
    last_state: Dict = None
    
    def __post_init__(self):
        """🧮 Calculate MIDI note and initialize tracking"""
        self.note = self.x + (self.y * 10)
        self.last_state = {
            'velocity': 0,
            'timestamp': None
        }
        logger.debug(f"🎮 Button initialized: ({self.x}, {self.y}) - Note: {self.note}")
    
    def record_press(self, velocity: int):
        """📊 Record button press with details"""
        from datetime import datetime
        self.press_count += 1
        self.last_state = {
            'velocity': velocity,
            'timestamp': datetime.now()
        }
        logger.info(
            f"🎯 Button Press #{self.press_count}\n"
            f"   Coordinates: ({self.x}, {self.y})\n"
            f"   MIDI Note: {self.note}\n"
            f"   Velocity: {velocity}\n"
            f"   Alias: {self.alias or 'None'}\n"
            f"   Color: {self.color}"
        )
    
    def get_quadrant(self) -> str:
        """🗺️ Determine button's quadrant location"""
        quadrant = ""
        if self.y < 4:
            quadrant += "Top "
        else:
            quadrant += "Bottom "
        
        if self.x < 4:
            quadrant += "Left"
        else:
            quadrant += "Right"
            
        return quadrant
    
    def get_debug_info(self) -> str:
        """📝 Get comprehensive debug information"""
        return (
            f"\n{'='*50}\n"
            f"🔍 Button Debug Info:\n"
            f"  📍 Position: ({self.x}, {self.y})\n"
            f"  🎯 MIDI Note: {self.note}\n"
            f"  🎨 Color: {self.color}\n"
            f"  📊 Press Count: {self.press_count}\n"
            f"  🗺️ Quadrant: {self.get_quadrant()}\n"
            f"  🔤 Alias: {self.alias or 'None'}\n"
            f"  ⏱️ Last Press: {self.last_state['timestamp']}\n"
            f"  📈 Last Velocity: {self.last_state['velocity']}\n"
            f"{'='*50}\n"
        )
