"""
📝 Enhanced Logging System
Handles separate logging for aliases and button mappings
"""

import logging
import json
from datetime import datetime
from pathlib import Path
import os

class LogManager:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamp for this session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Setup individual loggers
        self.alias_logger = self._setup_logger(
            "alias_logger",
            self.log_dir / f"alias_execution_{self.session_id}.log"
        )
        
        self.button_logger = self._setup_logger(
            "button_logger",
            self.log_dir / f"button_mapping_{self.session_id}.log"
        )
        
        # Setup JSON data stores
        self.alias_data = []
        self.button_data = []
    
    def _setup_logger(self, name: str, log_file: Path) -> logging.Logger:
        """Setup individual logger with file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def log_alias_execution(self, alias: str, success: bool, output: str = None, error: str = None):
        """Log alias execution details"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        timestamp = datetime.now().isoformat()
        
        # Log to file
        self.alias_logger.info(
            f"Alias: {alias} | Status: {status}\n"
            f"Output: {output}\n"
            f"Error: {error}\n"
            f"{'-'*50}"
        )
        
        # Store structured data
        self.alias_data.append({
            "timestamp": timestamp,
            "alias": alias,
            "success": success,
            "output": output,
            "error": error
        })
        
        # Write JSON
        self._write_json("alias_executions.json", self.alias_data)
    
    def log_button_press(self, button_info: dict):
        """Log button press details"""
        timestamp = datetime.now().isoformat()
        
        # Format button info
        info_str = (
            f"Button Press at ({button_info['x']}, {button_info['y']})\n"
            f"MIDI Note: {button_info['note']}\n"
            f"Mapped Alias: {button_info.get('alias', 'None')}\n"
            f"Quadrant: {button_info.get('quadrant', 'Unknown')}\n"
            f"Color: {button_info.get('color', 'Unknown')}\n"
            f"{'-'*50}"
        )
        
        # Log to file
        self.button_logger.info(info_str)
        
        # Store structured data
        button_info['timestamp'] = timestamp
        self.button_data.append(button_info)
        
        # Write JSON
        self._write_json("button_presses.json", self.button_data)
    
    def _write_json(self, filename: str, data: list):
        """Write data to JSON file"""
        json_path = self.log_dir / filename
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_session_summary(self) -> dict:
        """Generate session summary"""
        return {
            "session_id": self.session_id,
            "total_button_presses": len(self.button_data),
            "total_alias_executions": len(self.alias_data),
            "successful_aliases": sum(1 for a in self.alias_data if a['success']),
            "failed_aliases": sum(1 for a in self.alias_data if not a['success']),
            "most_pressed_buttons": self._get_most_pressed_buttons(),
            "most_used_aliases": self._get_most_used_aliases()
        }
    
    def _get_most_pressed_buttons(self) -> list:
        """Get statistics on most pressed buttons"""
        button_counts = {}
        for press in self.button_data:
            coord = (press['x'], press['y'])
            button_counts[coord] = button_counts.get(coord, 0) + 1
        
        # Sort by count
        return sorted(
            [{'coordinates': coord, 'count': count} 
             for coord, count in button_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )
    
    def _get_most_used_aliases(self) -> list:
        """Get statistics on most used aliases"""
        alias_counts = {}
        for execution in self.alias_data:
            alias = execution['alias']
            alias_counts[alias] = alias_counts.get(alias, 0) + 1
        
        # Sort by count
        return sorted(
            [{'alias': alias, 'count': count} 
             for alias, count in alias_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )