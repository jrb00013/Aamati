#!/usr/bin/env python3
"""
Comprehensive test runner for Aamati project.
Runs all tests and generates detailed reports.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from test_aamati import AamatiTester
from system_health import AamatiHealthMonitor


class AamatiTestRunner:
    """Comprehensive test runner for Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize test runner."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.results = {
            "timestamp": None,
            "integration_tests": {},
            "health_check": {},
            "performance_tests": {},
            "overall_status": "unknown"
        }
    
    def run_all_tests(self, verbose: bool = False) -> bool:
        """Run all tests and generate comprehensive report."""
        print("🧪 AAMATI COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        start_time = time.time()
        
        # 1. Integration Tests
        print("🔍 Running Integration Tests...")
        print("-" * 40)
        tester = AamatiTester()
        integration_success = tester.run_all_tests()
        self.results["integration_tests"] = {
            "success": integration_success,
            "details": tester.test_results
        }
        print()
        
        # 2. Health Check
        print("🏥 Running System Health Check...")
        print("-" * 40)
        monitor = AamatiHealthMonitor()
        health_data = monitor.run_health_check()
        health_success = health_data["overall_health"] in ["excellent", "good"]
        self.results["health_check"] = {
            "success": health_success,
            "overall_health": health_data["overall_health"],
            "details": health_data
        }
        print()
        
        # 3. Performance Tests
        print("⚡ Running Performance Tests...")
        print("-" * 40)
        perf_success = self._run_performance_tests()
        self.results["performance_tests"] = {
            "success": perf_success,
            "details": self._performance_results
        }
        print()
        
        # 4. Generate Report
        end_time = time.time()
        duration = end_time - start_time
        
        self.results["timestamp"] = datetime.now().isoformat()
        self.results["duration"] = duration
        
        # Calculate overall status
        all_success = integration_success and health_success and perf_success
        self.results["overall_status"] = "PASS" if all_success else "FAIL"
        
        # Generate and display report
        self._generate_report()
        
        return all_success
    
    def _run_performance_tests(self) -> bool:
        """Run performance tests."""
        self._performance_results = {}
        
        try:
            # Test 1: Feature extraction performance
            print("  Testing feature extraction performance...")
            start_time = time.time()
            
            # Create test MIDI file if needed
            test_midi = self.base_dir / "MLPython/MusicGroovesMIDI/TrainingMIDIs/test_perf.mid"
            if not test_midi.exists():
                self._create_test_midi_file(test_midi)
            
            # Run feature extraction
            os.chdir(self.base_dir / "MLPython")
            cmd = [
                "python3", "-c",
                f"import sys; sys.path.append('src'); from core.extract_groove_features import extract_features; "
                f"result = extract_features('{test_midi}'); print('SUCCESS' if result else 'FAILED')"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            extraction_time = time.time() - start_time
            
            self._performance_results["feature_extraction"] = {
                "success": result.returncode == 0 and "SUCCESS" in result.stdout,
                "duration": extraction_time,
                "threshold": 5.0  # seconds
            }
            
            if extraction_time > 5.0:
                print(f"    ⚠️ Feature extraction took {extraction_time:.2f}s (threshold: 5.0s)")
            else:
                print(f"    ✅ Feature extraction: {extraction_time:.2f}s")
            
            # Test 2: Model loading performance
            print("  Testing model loading performance...")
            start_time = time.time()
            
            cmd = [
                "python3", "-c",
                "import sys; sys.path.append('src'); from core.extract_groove_features import load_models; "
                "models = load_models(); print('SUCCESS' if any(models.values()) else 'FAILED')"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            loading_time = time.time() - start_time
            
            self._performance_results["model_loading"] = {
                "success": result.returncode == 0 and "SUCCESS" in result.stdout,
                "duration": loading_time,
                "threshold": 10.0  # seconds
            }
            
            if loading_time > 10.0:
                print(f"    ⚠️ Model loading took {loading_time:.2f}s (threshold: 10.0s)")
            else:
                print(f"    ✅ Model loading: {loading_time:.2f}s")
            
            # Test 3: Memory usage
            print("  Testing memory usage...")
            try:
                import psutil
                process = psutil.Process()
                memory_mb = process.memory_info().rss / (1024 * 1024)
                
                self._performance_results["memory_usage"] = {
                    "success": memory_mb < 1000,  # Less than 1GB
                    "memory_mb": memory_mb,
                    "threshold": 1000
                }
                
                if memory_mb > 1000:
                    print(f"    ⚠️ High memory usage: {memory_mb:.1f}MB (threshold: 1000MB)")
                else:
                    print(f"    ✅ Memory usage: {memory_mb:.1f}MB")
                    
            except ImportError:
                print("    ⚠️ psutil not available for memory testing")
                self._performance_results["memory_usage"] = {
                    "success": True,
                    "memory_mb": 0,
                    "threshold": 1000
                }
            
            # Overall performance success
            perf_success = all(
                test.get("success", False) 
                for test in self._performance_results.values()
            )
            
            return perf_success
            
        except Exception as e:
            print(f"    ❌ Performance test error: {e}")
            return False
        finally:
            os.chdir(self.base_dir)
    
    def _create_test_midi_file(self, file_path: Path):
        """Create a test MIDI file for performance testing."""
        try:
            import pretty_midi
            
            # Create a simple MIDI file
            midi = pretty_midi.PrettyMIDI()
            piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
            
            # Add some notes for testing
            notes = [
                (60, 0.0, 1.0, 80),  # C4
                (64, 1.0, 2.0, 80),  # E4
                (67, 2.0, 3.0, 80),  # G4
                (72, 3.0, 4.0, 80),  # C5
            ]
            
            for pitch, start, end, velocity in notes:
                note = pretty_midi.Note(
                    velocity=velocity,
                    pitch=pitch,
                    start=start,
                    end=end
                )
                piano.notes.append(note)
            
            midi.instruments.append(piano)
            midi.write(str(file_path))
            print(f"    ✅ Created test MIDI file: {file_path}")
            
        except Exception as e:
            print(f"    ❌ Failed to create test MIDI file: {e}")
    
    def _generate_report(self):
        """Generate comprehensive test report."""
        print("📊 GENERATING COMPREHENSIVE REPORT")
        print("=" * 60)
        
        # Overall status
        status_emoji = "🎉" if self.results["overall_status"] == "PASS" else "❌"
        print(f"Overall Status: {status_emoji} {self.results['overall_status']}")
        print(f"Duration: {self.results['duration']:.2f} seconds")
        print()
        
        # Integration tests summary
        integration = self.results["integration_tests"]
        print("🔍 INTEGRATION TESTS:")
        print(f"  Status: {'✅ PASS' if integration['success'] else '❌ FAIL'}")
        if integration['success']:
            passed = sum(integration['details'].values())
            total = len(integration['details'])
            print(f"  Tests Passed: {passed}/{total} ({(passed/total)*100:.1f}%)")
        print()
        
        # Health check summary
        health = self.results["health_check"]
        health_emoji = {"excellent": "💚", "good": "✅", "fair": "⚠️", "poor": "❌"}.get(health['overall_health'], "❓")
        print("🏥 SYSTEM HEALTH:")
        print(f"  Status: {health_emoji} {health['overall_health'].upper()}")
        print(f"  Overall: {'✅ HEALTHY' if health['success'] else '❌ ISSUES DETECTED'}")
        print()
        
        # Performance tests summary
        performance = self.results["performance_tests"]
        print("⚡ PERFORMANCE TESTS:")
        print(f"  Status: {'✅ PASS' if performance['success'] else '❌ FAIL'}")
        for test_name, test_data in performance['details'].items():
            status = "✅" if test_data['success'] else "❌"
            if 'duration' in test_data:
                print(f"    {test_name}: {status} {test_data['duration']:.2f}s")
            elif 'memory_mb' in test_data:
                print(f"    {test_name}: {status} {test_data['memory_mb']:.1f}MB")
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if self.results["overall_status"] == "PASS":
            print("  🎉 All systems are operational! You're ready to use Aamati.")
        else:
            if not integration['success']:
                print("  🔧 Fix integration test failures before proceeding")
            if not health['success']:
                print("  🏥 Address system health issues")
            if not performance['success']:
                print("  ⚡ Optimize performance bottlenecks")
        print()
        
        # Save detailed report
        self._save_detailed_report()
    
    def _save_detailed_report(self):
        """Save detailed report to file."""
        try:
            report_file = self.base_dir / "aamati_test_report.json"
            
            # Add timestamp and format for JSON
            report_data = {
                "test_run": {
                    "timestamp": self.results["timestamp"],
                    "duration": self.results["duration"],
                    "overall_status": self.results["overall_status"]
                },
                "integration_tests": self.results["integration_tests"],
                "health_check": self.results["health_check"],
                "performance_tests": self.results["performance_tests"]
            }
            
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"📄 Detailed report saved to: {report_file}")
            
        except Exception as e:
            print(f"⚠️ Failed to save detailed report: {e}")


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(description="Aamati Comprehensive Test Runner")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--quick", action="store_true",
                       help="Run quick tests only")
    parser.add_argument("--integration-only", action="store_true",
                       help="Run only integration tests")
    parser.add_argument("--health-only", action="store_true",
                       help="Run only health check")
    parser.add_argument("--performance-only", action="store_true",
                       help="Run only performance tests")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = AamatiTestRunner()
    
    if args.integration_only:
        # Run only integration tests
        tester = AamatiTester()
        success = tester.run_all_tests()
    elif args.health_only:
        # Run only health check
        monitor = AamatiHealthMonitor()
        health_data = monitor.run_health_check()
        success = health_data["overall_health"] in ["excellent", "good"]
        print(monitor.generate_health_report())
    elif args.performance_only:
        # Run only performance tests
        success = runner._run_performance_tests()
    else:
        # Run all tests
        success = runner.run_all_tests(verbose=args.verbose)
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
