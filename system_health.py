#!/usr/bin/env python3
"""
Aamati System Health Monitor
Continuously monitors system health and logs status.
"""

import os
import sys
import time
import json
import logging
import psutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import threading
import queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aamati_health.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AamatiHealthMonitor:
    """System health monitor for Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize health monitor."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.ml_dir = self.base_dir / "MLPython"
        self.resources_dir = self.base_dir / "Resources"
        
        # Health status
        self.health_status = {
            "timestamp": None,
            "system_resources": {},
            "ml_system": {},
            "juce_system": {},
            "data_integrity": {},
            "overall_health": "unknown"
        }
        
        # Monitoring settings
        self.monitor_interval = 30  # seconds
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "ml_latency": 5.0  # seconds
        }
        
        # Alert queue
        self.alert_queue = queue.Queue()
        
        logger.info("🏥 Aamati Health Monitor initialized")
    
    def check_system_resources(self) -> Dict:
        """Check system resource usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
            
            # Check for alerts
            if cpu_percent > self.alert_thresholds["cpu_percent"]:
                self.alert_queue.put(f"High CPU usage: {cpu_percent:.1f}%")
            
            if memory.percent > self.alert_thresholds["memory_percent"]:
                self.alert_queue.put(f"High memory usage: {memory.percent:.1f}%")
            
            if disk.percent > self.alert_thresholds["disk_percent"]:
                self.alert_queue.put(f"High disk usage: {disk.percent:.1f}%")
            
            return resources
            
        except Exception as e:
            logger.error(f"Failed to check system resources: {e}")
            return {}
    
    def check_ml_system(self) -> Dict:
        """Check ML system health."""
        try:
            ml_status = {
                "python_available": False,
                "dependencies_loaded": False,
                "models_available": False,
                "data_directories": False,
                "last_training": None,
                "feature_extraction_working": False
            }
            
            # Check Python
            try:
                import pandas, numpy, sklearn
                ml_status["python_available"] = True
                ml_status["dependencies_loaded"] = True
            except ImportError as e:
                logger.warning(f"ML dependencies issue: {e}")
            
            # Check models
            model_files = [
                "ModelClassificationScripts/models/energy_random_forest.joblib",
                "ModelClassificationScripts/models/swing_random_forest.joblib"
            ]
            
            models_found = 0
            for model_file in model_files:
                if (self.ml_dir / model_file).exists():
                    models_found += 1
            
            if models_found > 0:
                ml_status["models_available"] = True
            
            # Check data directories
            data_dirs = ["data/csv", "data/logs", "MusicGroovesMIDI/TrainingMIDIs"]
            all_dirs_exist = True
            for data_dir in data_dirs:
                if not (self.ml_dir / data_dir).exists():
                    all_dirs_exist = False
                    break
            
            ml_status["data_directories"] = all_dirs_exist
            
            # Check last training time
            log_file = self.ml_dir / "data/csv/groove_features_log_for_pred.csv"
            if log_file.exists():
                try:
                    import pandas as pd
                    df = pd.read_csv(log_file)
                    if 'timestamp' in df.columns and len(df) > 0:
                        last_timestamp = df['timestamp'].iloc[-1]
                        ml_status["last_training"] = last_timestamp
                except Exception:
                    pass
            
            # Test feature extraction
            try:
                test_cmd = [
                    "python3", "-c",
                    "import sys; sys.path.append('src'); from core.extract_groove_features import extract_features; print('OK')"
                ]
                result = subprocess.run(test_cmd, cwd=self.ml_dir, 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    ml_status["feature_extraction_working"] = True
            except Exception:
                pass
            
            return ml_status
            
        except Exception as e:
            logger.error(f"Failed to check ML system: {e}")
            return {}
    
    def check_juce_system(self) -> Dict:
        """Check JUCE system health."""
        try:
            juce_status = {
                "source_files": False,
                "cmake_available": False,
                "build_directory": False,
                "plugin_files": False,
                "resources_available": False
            }
            
            # Check source files
            source_files = [
                "PluginProcessor.cpp", "PluginProcessor.h",
                "PluginEditor.cpp", "PluginEditor.h"
            ]
            
            source_dir = self.base_dir / "Source"
            source_files_exist = all((source_dir / f).exists() for f in source_files)
            juce_status["source_files"] = source_files_exist
            
            # Check CMake
            try:
                result = subprocess.run(["cmake", "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    juce_status["cmake_available"] = True
            except Exception:
                pass
            
            # Check build directory
            build_dir = self.base_dir / "build"
            juce_status["build_directory"] = build_dir.exists()
            
            # Check plugin files
            plugin_files = [
                "build/Aamati_artefacts/Release/VST3/Aamati.vst3",
                "build/Aamati_artefacts/Release/AU/Aamati.component"
            ]
            
            plugins_exist = any((self.base_dir / f).exists() for f in plugin_files)
            juce_status["plugin_files"] = plugins_exist
            
            # Check resources
            onnx_model = self.resources_dir / "groove_mood_model.onnx"
            juce_status["resources_available"] = onnx_model.exists()
            
            return juce_status
            
        except Exception as e:
            logger.error(f"Failed to check JUCE system: {e}")
            return {}
    
    def check_data_integrity(self) -> Dict:
        """Check data integrity."""
        try:
            data_status = {
                "csv_files_valid": False,
                "model_files_valid": False,
                "midi_files_accessible": False,
                "log_files_writable": False
            }
            
            # Check CSV files
            csv_files = [
                "data/csv/groove_features_log.csv",
                "data/csv/groove_features_log_for_pred.csv"
            ]
            
            csv_valid = True
            for csv_file in csv_files:
                file_path = self.ml_dir / csv_file
                if file_path.exists():
                    try:
                        import pandas as pd
                        df = pd.read_csv(file_path)
                        # Basic validation
                        if len(df) > 0 and 'tempo' in df.columns:
                            continue
                        else:
                            csv_valid = False
                    except Exception:
                        csv_valid = False
                else:
                    csv_valid = False
            
            data_status["csv_files_valid"] = csv_valid
            
            # Check model files
            model_files = [
                "ModelClassificationScripts/models/energy_random_forest.joblib",
                "ModelClassificationScripts/models/swing_random_forest.joblib"
            ]
            
            models_valid = True
            for model_file in model_files:
                file_path = self.ml_dir / model_file
                if not file_path.exists() or file_path.stat().st_size == 0:
                    models_valid = False
                    break
            
            data_status["model_files_valid"] = models_valid
            
            # Check MIDI files accessibility
            midi_dir = self.ml_dir / "MusicGroovesMIDI/TrainingMIDIs"
            if midi_dir.exists():
                midi_files = list(midi_dir.glob("*.mid")) + list(midi_dir.glob("*.midi"))
                data_status["midi_files_accessible"] = len(midi_files) > 0
            
            # Check log files writability
            log_dir = self.ml_dir / "data/logs"
            if log_dir.exists():
                try:
                    test_file = log_dir / "test_write.tmp"
                    test_file.write_text("test")
                    test_file.unlink()
                    data_status["log_files_writable"] = True
                except Exception:
                    data_status["log_files_writable"] = False
            
            return data_status
            
        except Exception as e:
            logger.error(f"Failed to check data integrity: {e}")
            return {}
    
    def run_health_check(self) -> Dict:
        """Run complete health check."""
        logger.info("🏥 Running health check...")
        
        # Update timestamp
        self.health_status["timestamp"] = datetime.now().isoformat()
        
        # Check all systems
        self.health_status["system_resources"] = self.check_system_resources()
        self.health_status["ml_system"] = self.check_ml_system()
        self.health_status["juce_system"] = self.check_juce_system()
        self.health_status["data_integrity"] = self.check_data_integrity()
        
        # Determine overall health
        self._calculate_overall_health()
        
        # Process alerts
        self._process_alerts()
        
        return self.health_status
    
    def _calculate_overall_health(self):
        """Calculate overall system health."""
        try:
            # Check critical systems
            critical_checks = [
                self.health_status["ml_system"].get("python_available", False),
                self.health_status["ml_system"].get("dependencies_loaded", False),
                self.health_status["juce_system"].get("source_files", False),
                self.health_status["data_integrity"].get("csv_files_valid", False)
            ]
            
            # Check resource usage
            cpu_ok = self.health_status["system_resources"].get("cpu_percent", 0) < 90
            memory_ok = self.health_status["system_resources"].get("memory_percent", 0) < 95
            
            # Calculate health score
            critical_score = sum(critical_checks) / len(critical_checks)
            resource_score = (cpu_ok and memory_ok) * 0.5 + 0.5
            
            overall_score = (critical_score + resource_score) / 2
            
            if overall_score >= 0.9:
                self.health_status["overall_health"] = "excellent"
            elif overall_score >= 0.7:
                self.health_status["overall_health"] = "good"
            elif overall_score >= 0.5:
                self.health_status["overall_health"] = "fair"
            else:
                self.health_status["overall_health"] = "poor"
                
        except Exception as e:
            logger.error(f"Failed to calculate overall health: {e}")
            self.health_status["overall_health"] = "unknown"
    
    def _process_alerts(self):
        """Process and log alerts."""
        while not self.alert_queue.empty():
            try:
                alert = self.alert_queue.get_nowait()
                logger.warning(f"🚨 ALERT: {alert}")
            except queue.Empty:
                break
    
    def start_monitoring(self, duration_minutes: int = None):
        """Start continuous monitoring."""
        logger.info(f"🏥 Starting health monitoring (interval: {self.monitor_interval}s)")
        if duration_minutes:
            logger.info(f"⏰ Monitoring duration: {duration_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60) if duration_minutes else None
        
        try:
            while True:
                # Run health check
                health_data = self.run_health_check()
                
                # Log status
                logger.info(f"💚 Overall Health: {health_data['overall_health'].upper()}")
                
                # Save health data
                self._save_health_data(health_data)
                
                # Check if we should stop
                if end_time and time.time() >= end_time:
                    logger.info("⏰ Monitoring duration completed")
                    break
                
                # Wait for next check
                time.sleep(self.monitor_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
    
    def _save_health_data(self, health_data: Dict):
        """Save health data to file."""
        try:
            health_file = self.base_dir / "aamati_health.json"
            
            # Load existing data
            if health_file.exists():
                with open(health_file, 'r') as f:
                    all_data = json.load(f)
            else:
                all_data = {"health_checks": []}
            
            # Add new data
            all_data["health_checks"].append(health_data)
            
            # Keep only last 100 checks
            if len(all_data["health_checks"]) > 100:
                all_data["health_checks"] = all_data["health_checks"][-100:]
            
            # Save data
            with open(health_file, 'w') as f:
                json.dump(all_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save health data: {e}")
    
    def generate_health_report(self) -> str:
        """Generate health report."""
        report = []
        report.append("🏥 AAMATI SYSTEM HEALTH REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall health
        health = self.health_status["overall_health"]
        health_emoji = {"excellent": "💚", "good": "✅", "fair": "⚠️", "poor": "❌", "unknown": "❓"}
        report.append(f"Overall Health: {health_emoji.get(health, '❓')} {health.upper()}")
        report.append("")
        
        # System resources
        resources = self.health_status["system_resources"]
        report.append("🖥️ SYSTEM RESOURCES:")
        report.append(f"  CPU Usage: {resources.get('cpu_percent', 0):.1f}%")
        report.append(f"  Memory Usage: {resources.get('memory_percent', 0):.1f}%")
        report.append(f"  Available Memory: {resources.get('memory_available_gb', 0):.1f} GB")
        report.append(f"  Disk Usage: {resources.get('disk_percent', 0):.1f}%")
        report.append(f"  Free Disk: {resources.get('disk_free_gb', 0):.1f} GB")
        report.append("")
        
        # ML System
        ml = self.health_status["ml_system"]
        report.append("🤖 ML SYSTEM:")
        report.append(f"  Python Available: {'✅' if ml.get('python_available') else '❌'}")
        report.append(f"  Dependencies Loaded: {'✅' if ml.get('dependencies_loaded') else '❌'}")
        report.append(f"  Models Available: {'✅' if ml.get('models_available') else '❌'}")
        report.append(f"  Data Directories: {'✅' if ml.get('data_directories') else '❌'}")
        report.append(f"  Feature Extraction: {'✅' if ml.get('feature_extraction_working') else '❌'}")
        if ml.get('last_training'):
            report.append(f"  Last Training: {ml['last_training']}")
        report.append("")
        
        # JUCE System
        juce = self.health_status["juce_system"]
        report.append("🎛️ JUCE SYSTEM:")
        report.append(f"  Source Files: {'✅' if juce.get('source_files') else '❌'}")
        report.append(f"  CMake Available: {'✅' if juce.get('cmake_available') else '❌'}")
        report.append(f"  Build Directory: {'✅' if juce.get('build_directory') else '❌'}")
        report.append(f"  Plugin Files: {'✅' if juce.get('plugin_files') else '❌'}")
        report.append(f"  Resources Available: {'✅' if juce.get('resources_available') else '❌'}")
        report.append("")
        
        # Data Integrity
        data = self.health_status["data_integrity"]
        report.append("📊 DATA INTEGRITY:")
        report.append(f"  CSV Files Valid: {'✅' if data.get('csv_files_valid') else '❌'}")
        report.append(f"  Model Files Valid: {'✅' if data.get('model_files_valid') else '❌'}")
        report.append(f"  MIDI Files Accessible: {'✅' if data.get('midi_files_accessible') else '❌'}")
        report.append(f"  Log Files Writable: {'✅' if data.get('log_files_writable') else '❌'}")
        
        return "\n".join(report)


def main():
    """Main entry point for health monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Aamati System Health Monitor")
    parser.add_argument("--check", action="store_true",
                       help="Run single health check")
    parser.add_argument("--monitor", action="store_true",
                       help="Start continuous monitoring")
    parser.add_argument("--duration", type=int, default=60,
                       help="Monitoring duration in minutes")
    parser.add_argument("--report", action="store_true",
                       help="Generate health report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create monitor
    monitor = AamatiHealthMonitor()
    
    if args.check:
        # Run single health check
        health_data = monitor.run_health_check()
        print(f"💚 Overall Health: {health_data['overall_health'].upper()}")
        
    elif args.monitor:
        # Start continuous monitoring
        monitor.start_monitoring(duration_minutes=args.duration)
        
    elif args.report:
        # Generate health report
        monitor.run_health_check()
        report = monitor.generate_health_report()
        print(report)
        
        # Save report
        report_file = Path("aamati_health_report.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\n📄 Health report saved to: {report_file}")
        
    else:
        # Default: run health check and show report
        monitor.run_health_check()
        report = monitor.generate_health_report()
        print(report)


if __name__ == "__main__":
    main()
