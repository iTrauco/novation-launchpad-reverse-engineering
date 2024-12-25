# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# 🎮 Main Application Module
# Handles MIDI setup and button mapping for Launchpad.
# """

# import rtmidi
# import logging
# from typing import Dict, Optional, Callable
# import signal
# from datetime import datetime
# from .models.button import LaunchpadButton
# from .handlers.alias_handler import AliasHandler
# from .utils.constants import Colors, MIDI_NOTE_ON, calculate_xy

# # Setup detailed logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

# logger = logging.getLogger(__name__)

# class LaunchpadApp:
#     """🎹 Main Launchpad control application"""
    
#     def __init__(self, port_name: str = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI"):
#         self.midi_in = rtmidi.MidiIn()
#         self.midi_out = rtmidi.MidiOut()
#         self.port_name = port_name
#         self.buttons: Dict[tuple, LaunchpadButton] = {}
#         self.alias_handler = AliasHandler()
#         self.session_start = datetime.now()
#         self._running = False
        
#         # Set up signal handlers for clean shutdown
#         signal.signal(signal.SIGINT, self._handle_shutdown)
#         signal.signal(signal.SIGTERM, self._handle_shutdown)
        
#         logger.info("🚀 Initializing LaunchpadApp")
        
#     def connect(self) -> bool:
#         """🔌 Connect to Launchpad MIDI ports"""
#         try:
#             # List available ports
#             in_ports = self.midi_in.get_ports()
#             out_ports = self.midi_out.get_ports()
            
#             logger.debug(f"📥 Available input ports: {in_ports}")
#             logger.debug(f"📤 Available output ports: {out_ports}")
            
#             # Find port indices
#             in_port_idx = next(i for i, name in enumerate(in_ports) if self.port_name in name)
#             out_port_idx = next(i for i, name in enumerate(out_ports) if self.port_name in name)
            
#             # Open ports
#             self.midi_in.open_port(in_port_idx)
#             self.midi_out.open_port(out_port_idx)
            
#             # Set up callback
#             self.midi_in.set_callback(self._handle_midi_input)
            
#             logger.info(f"✅ Connected to Launchpad: {self.port_name}")
#             return True
            
#         except Exception as e:
#             logger.error(f"❌ Failed to connect to Launchpad: {e}")
#             return False
            
#     def add_mapping(self, x: int, y: int, color: int, alias: str):
#         """🎯 Map button to alias with color"""
#         button = LaunchpadButton(x=x, y=y, color=color, alias=alias)
#         self.buttons[(x, y)] = button
        
#         # Set initial button color
#         self.set_button_color(button)
        
#         logger.info(
#             f"✨ Mapped button:\n"
#             f"   Coordinates: ({x}, {y})\n"
#             f"   Alias: {alias}\n"
#             f"   Color: {color}\n"
#             f"   MIDI Note: {button.note}"
#         )
        
#     def set_button_color(self, button: LaunchpadButton):
#         """🎨 Set button color"""
#         try:
#             message = [MIDI_NOTE_ON, button.note, button.color]
#             self.midi_out.send_message(message)
#             logger.debug(f"🎨 Set color {button.color} for button ({button.x}, {button.y})")
#         except Exception as e:
#             logger.error(f"❌ Failed to set button color: {e}")
            
#     def _handle_midi_input(self, event, _):
#         """🎯 Process incoming MIDI messages"""
#         message, _ = event
        
#         if len(message) != 3:
#             return
            
#         status, note, velocity = message
#         x, y = calculate_xy(note)
        
#         # Get button if it exists
#         button = self.buttons.get((x, y))
        
#         if button and velocity > 0:  # Button press
#             button.record_press(velocity)
            
#             # Execute alias if defined
#             if button.alias:
#                 success = self.alias_handler.execute(button.alias)
#                 logger.info(
#                     f"{'✅' if success else '❌'} "
#                     f"Alias execution: {button.alias}"
#                 )
                
#             # Print comprehensive debug info
#             logger.info(button.get_debug_info())
            
#     def _handle_shutdown(self, *args):
#         """🔄 Clean shutdown handling"""
#         logger.info("🛑 Shutting down...")
        
#         try:
#             # Turn off all mapped buttons
#             for button in self.buttons.values():
#                 self.set_button_color(LaunchpadButton(
#                     x=button.x, 
#                     y=button.y, 
#                     color=Colors.OFF
#                 ))
                
#             # Close MIDI ports
#             self.midi_in.close_port()
#             self.midi_out.close_port()
            
#             # Print session stats
#             session_duration = datetime.now() - self.session_start
#             logger.info(f"\n📊 Session Summary:")
#             logger.info(f"   Duration: {session_duration}")
#             logger.info(f"   Mapped Buttons: {len(self.buttons)}")
            
#             # Get alias execution stats
#             stats = self.alias_handler.get_execution_stats()
#             logger.info("   Execution Stats:")
#             for key, value in stats.items():
#                 logger.info(f"      • {key}: {value}")
                
#         except Exception as e:
#             logger.error(f"❌ Error during shutdown: {e}")
            
#         finally:
#             self._running = False
            
#     def run(self):
#         """🏃 Main application loop"""
#         if not self.connect():
#             return
            
#         self._running = True
#         logger.info("✨ Application started - Press Ctrl+C to exit")
        
#         try:
#             while self._running:
#                 signal.pause()
#         except KeyboardInterrupt:
#             self._handle_shutdown()

"""
🎮 Main Application Module
Handles MIDI setup and button mapping for Launchpad with enhanced logging.
"""

import rtmidi
import logging
from typing import Dict, Optional, Callable
import signal
from datetime import datetime
from .models.button import LaunchpadButton
from .handlers.alias_handler import AliasHandler
from .utils.constants import Colors, MIDI_NOTE_ON, calculate_xy
from .utils.log_manager import LogManager

logger = logging.getLogger(__name__)

class LaunchpadApp:
    """🎹 Main Launchpad control application"""
    
    def __init__(self, port_name: str = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI", 
                 log_manager: Optional[LogManager] = None):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.port_name = port_name
        self.buttons: Dict[tuple, LaunchpadButton] = {}
        self.alias_handler = AliasHandler()
        self.session_start = datetime.now()
        self._running = False
        
        # Initialize log manager if not provided
        self.log_manager = log_manager or LogManager()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        logger.info("🚀 Initializing LaunchpadApp")
        
    def connect(self) -> bool:
        """🔌 Connect to Launchpad MIDI ports"""
        try:
            # List available ports
            in_ports = self.midi_in.get_ports()
            out_ports = self.midi_out.get_ports()
            
            logger.debug(f"📥 Available input ports: {in_ports}")
            logger.debug(f"📤 Available output ports: {out_ports}")
            
            # Find port indices
            in_port_idx = next(i for i, name in enumerate(in_ports) if self.port_name in name)
            out_port_idx = next(i for i, name in enumerate(out_ports) if self.port_name in name)
            
            # Open ports
            self.midi_in.open_port(in_port_idx)
            self.midi_out.open_port(out_port_idx)
            
            # Set up callback
            self.midi_in.set_callback(self._handle_midi_input)
            
            logger.info(f"✅ Connected to Launchpad: {self.port_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Launchpad: {e}")
            return False
            
    def add_mapping(self, x: int, y: int, color: int, alias: str):
        """🎯 Map button to alias with color"""
        button = LaunchpadButton(x=x, y=y, color=color, alias=alias)
        self.buttons[(x, y)] = button
        
        # Set initial button color
        self.set_button_color(button)
        
        # Log the mapping
        self.log_manager.log_button_press({
            'x': x,
            'y': y,
            'color': color,
            'alias': alias,
            'note': button.note,
            'quadrant': button.get_quadrant(),
            'event_type': 'mapping_created'
        })
        
        logger.info(
            f"✨ Mapped button:\n"
            f"   Coordinates: ({x}, {y})\n"
            f"   Alias: {alias}\n"
            f"   Color: {color}\n"
            f"   MIDI Note: {button.note}"
        )
        
    def set_button_color(self, button: LaunchpadButton):
        """🎨 Set button color"""
        try:
            message = [MIDI_NOTE_ON, button.note, button.color]
            self.midi_out.send_message(message)
            logger.debug(f"🎨 Set color {button.color} for button ({button.x}, {button.y})")
        except Exception as e:
            logger.error(f"❌ Failed to set button color: {e}")
            
    def _handle_midi_input(self, event, _):
        """🎯 Process incoming MIDI messages"""
        message, _ = event
        
        if len(message) != 3:
            return
            
        status, note, velocity = message
        x, y = calculate_xy(note)
        
        # Get button if it exists
        button = self.buttons.get((x, y))
        
        if button and velocity > 0:  # Button press
            button.record_press(velocity)
            
            # Log button press
            self.log_manager.log_button_press({
                'x': x,
                'y': y,
                'color': button.color,
                'alias': button.alias,
                'note': note,
                'velocity': velocity,
                'quadrant': button.get_quadrant(),
                'event_type': 'button_pressed'
            })
            
            # Execute alias if defined
            if button.alias:
                success = self.alias_handler.execute(button.alias)
                
                # Log alias execution
                self.log_manager.log_alias_execution(
                    alias=button.alias,
                    success=success,
                    output=f"Button pressed at ({x}, {y})",
                    error=None if success else "Execution failed"
                )
                
                logger.info(
                    f"{'✅' if success else '❌'} "
                    f"Alias execution: {button.alias}"
                )
                
            # Print debug info
            logger.info(button.get_debug_info())
            
    def _handle_shutdown(self, *args):
        """🔄 Clean shutdown handling"""
        logger.info("🛑 Shutting down...")
        
        try:
            # Turn off all mapped buttons
            for button in self.buttons.values():
                self.set_button_color(LaunchpadButton(
                    x=button.x, 
                    y=button.y, 
                    color=Colors.OFF
                ))
                
            # Close MIDI ports
            self.midi_in.close_port()
            self.midi_out.close_port()
            
            # Get final session summary
            summary = self.log_manager.get_session_summary()
            
            logger.info(f"\n📊 Session Summary:")
            logger.info(f"   Session ID: {summary['session_id']}")
            logger.info(f"   Button Presses: {summary['total_button_presses']}")
            logger.info(f"   Alias Executions: {summary['total_alias_executions']}")
            logger.info(f"   Successful Aliases: {summary['successful_aliases']}")
            logger.info(f"   Failed Aliases: {summary['failed_aliases']}")
                
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
            
        finally:
            self._running = False
    
    def run(self):
        """🏃 Main application loop"""
        if not self.connect():
            return
            
        self._running = True
        logger.info("✨ Application started - Press Ctrl+C to exit")
        
        try:
            while self._running:
                signal.pause()
        except KeyboardInterrupt:
            self._handle_shutdown()