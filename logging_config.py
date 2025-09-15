#!/usr/bin/env python3
"""
Centralized logging configuration for Aamati project.
Provides consistent logging across all components.
"""

import os
import sys
import logging
import logging.handlers
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json


class AamatiLogger:
    """Centralized logger for Aamati project."""
    
    def __init__(self, name: str = "aamati", log_dir: str = None):
        """Initialize logger."""
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_handlers()
        
        # Performance tracking
        self.performance_data = {}
    
    def _setup_handlers(self):
        """Setup logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.FileHandler(
            self.log_dir / f"{self.name}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Error handler
        error_handler = logging.FileHandler(
            self.log_dir / f"{self.name}_errors.log"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        self.logger.addHandler(error_handler)
        
        # Performance handler
        perf_handler = logging.FileHandler(
            self.log_dir / f"{self.name}_performance.log"
        )
        perf_handler.setLevel(logging.INFO)
        perf_format = logging.Formatter(
            '%(asctime)s - PERFORMANCE - %(message)s'
        )
        perf_handler.setFormatter(perf_format)
        self.logger.addHandler(perf_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def log_performance(self, operation: str, duration: float, **metadata):
        """Log performance data."""
        perf_data = {
            "operation": operation,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            **metadata
        }
        
        self.performance_data[operation] = perf_data
        
        # Log to performance file
        perf_logger = logging.getLogger(f"{self.name}.performance")
        perf_logger.info(json.dumps(perf_data))
    
    def log_feature_extraction(self, midi_file: str, features: Dict[str, Any], 
                              duration: float = None):
        """Log feature extraction data."""
        data = {
            "midi_file": midi_file,
            "features": features,
            "timestamp": datetime.now().isoformat()
        }
        
        if duration:
            data["duration"] = duration
        
        # Log to features file
        features_logger = logging.getLogger(f"{self.name}.features")
        features_handler = logging.FileHandler(
            self.log_dir / "feature_extraction.log"
        )
        features_handler.setFormatter(logging.Formatter('%(message)s'))
        features_logger.addHandler(features_handler)
        features_logger.info(json.dumps(data))
    
    def log_model_training(self, model_name: str, metrics: Dict[str, Any], 
                          duration: float = None):
        """Log model training data."""
        data = {
            "model_name": model_name,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        if duration:
            data["duration"] = duration
        
        # Log to training file
        training_logger = logging.getLogger(f"{self.name}.training")
        training_handler = logging.FileHandler(
            self.log_dir / "model_training.log"
        )
        training_handler.setFormatter(logging.Formatter('%(message)s'))
        training_logger.addHandler(training_handler)
        training_logger.info(json.dumps(data))
    
    def log_prediction(self, input_data: Dict[str, Any], prediction: str, 
                      confidence: float = None, duration: float = None):
        """Log prediction data."""
        data = {
            "input_data": input_data,
            "prediction": prediction,
            "timestamp": datetime.now().isoformat()
        }
        
        if confidence:
            data["confidence"] = confidence
        if duration:
            data["duration"] = duration
        
        # Log to predictions file
        pred_logger = logging.getLogger(f"{self.name}.predictions")
        pred_handler = logging.FileHandler(
            self.log_dir / "predictions.log"
        )
        pred_handler.setFormatter(logging.Formatter('%(message)s'))
        pred_logger.addHandler(pred_handler)
        pred_logger.info(json.dumps(data))
    
    def log_system_event(self, event_type: str, message: str, **metadata):
        """Log system events."""
        data = {
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **metadata
        }
        
        # Log to system file
        system_logger = logging.getLogger(f"{self.name}.system")
        system_handler = logging.FileHandler(
            self.log_dir / "system_events.log"
        )
        system_handler.setFormatter(logging.Formatter('%(message)s'))
        system_logger.addHandler(system_handler)
        system_logger.info(json.dumps(data))
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.performance_data:
            return {}
        
        operations = list(self.performance_data.values())
        durations = [op.get('duration', 0) for op in operations]
        
        return {
            "total_operations": len(operations),
            "average_duration": sum(durations) / len(durations) if durations else 0,
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "operations": operations
        }
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """Clean up old log files."""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date:
                log_file.unlink()
                self.info(f"Cleaned up old log file: {log_file.name}")


# Global logger instance
_global_logger = None

def get_logger(name: str = "aamati") -> AamatiLogger:
    """Get global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = AamatiLogger(name)
    return _global_logger


def setup_component_logging(component_name: str) -> AamatiLogger:
    """Setup logging for a specific component."""
    return AamatiLogger(f"aamati.{component_name}")


# Context manager for performance logging
class PerformanceLogger:
    """Context manager for logging performance."""
    
    def __init__(self, logger: AamatiLogger, operation: str, **metadata):
        self.logger = logger
        self.operation = operation
        self.metadata = metadata
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.debug(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.logger.log_performance(
            self.operation, 
            duration, 
            **self.metadata
        )
        
        if exc_type:
            self.logger.error(f"Error in {self.operation}: {exc_val}")
        else:
            self.logger.debug(f"Completed {self.operation} in {duration:.2f}s")


# Decorator for automatic performance logging
def log_performance(operation_name: str = None, **metadata):
    """Decorator for automatic performance logging."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            with PerformanceLogger(logger, op_name, **metadata):
                return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test the logging system
    logger = get_logger("test")
    
    logger.info("Testing Aamati logging system")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test performance logging
    with PerformanceLogger(logger, "test_operation"):
        import time
        time.sleep(0.1)
    
    # Test feature extraction logging
    logger.log_feature_extraction(
        "test.mid",
        {"tempo": 120, "swing": 0.5, "density": 15.0},
        duration=0.5
    )
    
    # Test model training logging
    logger.log_model_training(
        "test_model",
        {"accuracy": 0.95, "precision": 0.92, "recall": 0.88},
        duration=30.0
    )
    
    # Test prediction logging
    logger.log_prediction(
        {"tempo": 120, "swing": 0.5},
        "energetic",
        confidence=0.85,
        duration=0.1
    )
    
    # Test system event logging
    logger.log_system_event(
        "startup",
        "Aamati system started",
        version="1.0.0"
    )
    
    print("✅ Logging system test completed")
    print(f"📁 Logs saved to: {logger.log_dir}")
