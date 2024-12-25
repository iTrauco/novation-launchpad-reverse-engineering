#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎨 Constants Module
Defines MIDI and color constants for Launchpad control
"""

class Colors:
    """🎨 Standard Launchpad Mini MK3 colors"""
    OFF = 0      # ⚫ Off
    RED = 5      # 🔴 Red
    GREEN = 21   # 💚 Green
    BLUE = 45    # 💙 Blue
    YELLOW = 13  # 💛 Yellow
    PURPLE = 49  # 💜 Purple
    CYAN = 33    # 🔷 Cyan
    WHITE = 3    # ⚪ White

# 🎹 MIDI Constants
MIDI_NOTE_ON = 0x90  # Note On message
MIDI_NOTE_OFF = 0x80  # Note Off message

# 🎛️ Grid Constants
GRID_SIZE = 8  # Standard 8x8 grid

def calculate_note(x: int, y: int) -> int:
    """🧮 Calculate MIDI note number from x,y coordinates"""
    return x + (y * 10)

def calculate_xy(note: int) -> tuple[int, int]:
    """🎯 Calculate x,y coordinates from MIDI note number"""
    x = note % 10
    y = note // 10
    return x, y
