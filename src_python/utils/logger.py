"""
Logging Utility Module
Provides structured logging functionality for the data scooper project.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class Logger:
    """
    Simple Logger class for structured logging.
    """
    
    def __init__(self, name: str = "data-scooper", level: int = logging.INFO):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def info(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Log info message."""
        if meta:
            self.logger.info(f"{message} - {meta}")
        else:
            self.logger.info(message)
    
    def error(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Log error message."""
        if meta:
            self.logger.error(f"{message} - {meta}")
        else:
            self.logger.error(message)
    
    def warning(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message."""
        if meta:
            self.logger.warning(f"{message} - {meta}")
        else:
            self.logger.warning(message)
    
    def debug(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message."""
        if meta:
            self.logger.debug(f"{message} - {meta}")
        else:
            self.logger.debug(message)


# Create default logger instance
logger = Logger()


def get_logger(name: str = "data-scooper") -> Logger:
    """
    Get or create logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return Logger(name)
