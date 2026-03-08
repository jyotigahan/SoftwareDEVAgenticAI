"""Logging configuration for tracking agent activities."""

import logging
import colorlog
from datetime import datetime
import os


class AgentLogger:
    """Custom logger for tracking agent activities."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"agent_activity_{timestamp}.log")
        
        # Setup logger
        self.logger = logging.getLogger("AgentTeam")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def agent_start(self, agent_name: str, task: str):
        """Log when an agent starts working."""
        self.logger.info(f"🤖 {agent_name} STARTED")
        self.logger.debug(f"   Task: {task[:100]}...")
    
    def agent_thinking(self, agent_name: str, message: str):
        """Log agent's thinking process."""
        self.logger.debug(f"   💭 {agent_name}: {message}")
    
    def agent_complete(self, agent_name: str, output_length: int):
        """Log when an agent completes work."""
        self.logger.info(f"✅ {agent_name} COMPLETED (Output: {output_length} chars)")
    
    def phase_start(self, phase: str):
        """Log phase transition."""
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"📍 PHASE: {phase.upper()}")
        self.logger.info(f"{'='*60}\n")
    
    def email_sent(self, recipient: str, subject: str):
        """Log email notification."""
        self.logger.info(f"📧 Email sent to {recipient}: {subject}")
    
    def error(self, message: str):
        """Log error."""
        self.logger.error(f"❌ ERROR: {message}")
    
    def warning(self, message: str):
        """Log warning."""
        self.logger.warning(f"⚠️  WARNING: {message}")
    
    def info(self, message: str):
        """Log general info."""
        self.logger.info(message)
    
    def get_log_file(self) -> str:
        """Get the log file path."""
        return self.log_file
