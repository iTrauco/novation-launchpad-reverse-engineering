#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 Alias Handler Module
Handles the execution of shell aliases in a controlled environment.
"""

import subprocess
import logging
from pathlib import Path
import os
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AliasHandler:
    """🎮 Handles shell alias execution with detailed logging"""
    
    def __init__(self, shell_path: str = '/bin/zsh'):
        self.home = str(Path.home())
        self.shell_path = shell_path
        self.execution_history = []
        logger.info(f"🚀 Initialized AliasHandler with shell: {shell_path}")
        
    def execute(self, alias_name: str) -> bool:
        """
        🎯 Execute a shell alias with comprehensive logging
        
        Args:
            alias_name: Name of the alias to execute
        """
        timestamp = datetime.now()
        execution_record = {
            'alias': alias_name,
            'timestamp': timestamp,
            'success': False,
            'output': None,
            'error': None
        }
        
        try:
            # Using the successful method from previous implementation
            command = f"{self.shell_path} -i -c '{alias_name}'"
            
            logger.info(f"🔄 Executing: {alias_name}")
            logger.debug(f"📝 Full command: {command}")
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable=self.shell_path,
                env=os.environ.copy(),
                start_new_session=True
            )
            
            stdout, stderr = process.communicate(timeout=5)
            
            # Record outputs
            if stdout:
                output = stdout.decode().strip()
                logger.info(f"📤 Output: {output}")
                execution_record['output'] = output
                
            if stderr:
                error = stderr.decode().strip()
                logger.warning(f"⚠️ Error: {error}")
                execution_record['error'] = error
                
            success = process.returncode == 0
            execution_record['success'] = success
            
            if success:
                logger.info(f"✅ Successfully executed: {alias_name}")
            else:
                logger.error(f"❌ Failed to execute: {alias_name}")
            
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Timeout executing: {alias_name}")
            execution_record['error'] = "Execution timeout"
            success = False
            
        except Exception as e:
            logger.error(f"💥 Error executing {alias_name}: {e}")
            execution_record['error'] = str(e)
            success = False
            
        finally:
            self.execution_history.append(execution_record)
            return success
    
    def get_execution_stats(self) -> dict:
        """📊 Get statistics about alias executions"""
        if not self.execution_history:
            return {"message": "No executions recorded"}
            
        stats = {
            "total_executions": len(self.execution_history),
            "successful_executions": sum(1 for record in self.execution_history if record['success']),
            "failed_executions": sum(1 for record in self.execution_history if not record['success']),
            "unique_aliases": len(set(record['alias'] for record in self.execution_history)),
            "last_execution": self.execution_history[-1]
        }
        
        logger.info("📈 Execution Statistics:")
        for key, value in stats.items():
            logger.info(f"  • {key}: {value}")
            
        return stats
    
    def get_alias_history(self, alias_name: str) -> list:
        """📜 Get execution history for specific alias"""
        history = [
            record for record in self.execution_history 
            if record['alias'] == alias_name
        ]
        
        logger.info(f"📚 History for alias '{alias_name}':")
        for record in history:
            logger.info(
                f"  • {record['timestamp']}: "
                f"{'✅ Success' if record['success'] else '❌ Failed'}"
            )
            
        return history
