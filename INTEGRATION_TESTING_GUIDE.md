# 🧪 Aamati Integration Testing Guide

This guide covers the comprehensive testing system for the Aamati project, ensuring all components work together seamlessly.

## 🎯 Testing Overview

The Aamati testing system consists of three main components:

1. **Integration Tests** - Test all system components and their interactions
2. **Health Monitoring** - Continuous system health monitoring
3. **Performance Tests** - Performance benchmarking and optimization

## 🚀 Quick Start

### Run All Tests
```bash
# Run complete test suite
python3 run_tests.py

# Run with verbose output
python3 run_tests.py --verbose

# Run specific test categories
python3 run_tests.py --integration-only
python3 run_tests.py --health-only
python3 run_tests.py --performance-only
```

### Run Individual Components
```bash
# Integration tests only
python3 test_aamati.py

# Health check only
python3 system_health.py --check

# Continuous health monitoring
python3 system_health.py --monitor --duration 60
```

## 🔍 Integration Tests

### Test Categories

#### 1. Python Environment Test
- **Purpose**: Verify Python version and dependencies
- **Checks**:
  - Python 3.8+ installed
  - Required packages available (pandas, numpy, scikit-learn, etc.)
  - ONNX Runtime availability

#### 2. ML Dependencies Test
- **Purpose**: Verify ML system components
- **Checks**:
  - Model files exist and are valid
  - Feature extraction modules loadable
  - Training data accessible

#### 3. JUCE Environment Test
- **Purpose**: Verify JUCE plugin development environment
- **Checks**:
  - Source files present
  - CMake available
  - Build directory accessible

#### 4. Data Structure Test
- **Purpose**: Verify data organization
- **Checks**:
  - Required directories exist
  - MIDI files accessible
  - CSV files writable

#### 5. Feature Extraction Test
- **Purpose**: Test core ML functionality
- **Checks**:
  - MIDI file processing
  - Feature extraction accuracy
  - Data logging functionality

#### 6. Model Training Test
- **Purpose**: Test model training pipeline
- **Checks**:
  - Training data validation
  - Model creation
  - Performance metrics

#### 7. Model Prediction Test
- **Purpose**: Test prediction functionality
- **Checks**:
  - Model loading
  - Prediction generation
  - Output validation

#### 8. Model Export Test
- **Purpose**: Test model export for JUCE
- **Checks**:
  - ONNX model creation
  - Resource file copying
  - Format validation

#### 9. JUCE Compilation Test
- **Purpose**: Test plugin compilation
- **Checks**:
  - CMake configuration
  - Compilation success
  - Plugin file generation

#### 10. Plugin Integration Test
- **Purpose**: Test final plugin integration
- **Checks**:
  - Plugin files present
  - Resource loading
  - Format compatibility

#### 11. End-to-End Pipeline Test
- **Purpose**: Test complete workflow
- **Checks**:
  - Full ML pipeline execution
  - Data flow validation
  - System integration

### Running Integration Tests

```bash
# Run all integration tests
python3 test_aamati.py

# Run specific component tests
python3 test_aamati.py --component python
python3 test_aamati.py --component ml
python3 test_aamati.py --component juce
python3 test_aamati.py --component integration

# Generate test report
python3 test_aamati.py --report
```

## 🏥 Health Monitoring

### System Health Checks

#### Resource Monitoring
- **CPU Usage**: Monitor processor utilization
- **Memory Usage**: Track RAM consumption
- **Disk Usage**: Monitor storage space
- **Load Average**: System load monitoring

#### ML System Health
- **Python Availability**: Runtime status
- **Dependencies**: Package availability
- **Models**: Model file integrity
- **Data Directories**: File system access
- **Feature Extraction**: Core functionality

#### JUCE System Health
- **Source Files**: Code availability
- **CMake**: Build system status
- **Build Directory**: Compilation environment
- **Plugin Files**: Generated artifacts
- **Resources**: Model file availability

#### Data Integrity
- **CSV Files**: Data file validation
- **Model Files**: Model integrity
- **MIDI Files**: Audio file accessibility
- **Log Files**: Write permissions

### Health Monitoring Commands

```bash
# Single health check
python3 system_health.py --check

# Generate health report
python3 system_health.py --report

# Start continuous monitoring
python3 system_health.py --monitor --duration 60

# Monitor with verbose output
python3 system_health.py --monitor --verbose
```

### Health Status Levels

- **💚 Excellent**: All systems optimal
- **✅ Good**: Minor issues, fully functional
- **⚠️ Fair**: Some issues, mostly functional
- **❌ Poor**: Major issues, limited functionality

## ⚡ Performance Tests

### Performance Benchmarks

#### Feature Extraction Performance
- **Target**: < 5 seconds per MIDI file
- **Measurement**: Processing time for test files
- **Optimization**: Batch processing, caching

#### Model Loading Performance
- **Target**: < 10 seconds for all models
- **Measurement**: Model loading time
- **Optimization**: Lazy loading, caching

#### Memory Usage
- **Target**: < 1GB total memory usage
- **Measurement**: Process memory consumption
- **Optimization**: Memory management, cleanup

### Performance Monitoring

```bash
# Run performance tests
python3 run_tests.py --performance-only

# Monitor system resources
python3 system_health.py --monitor --duration 30
```

## 📊 Logging System

### Log Categories

#### 1. Feature Extraction Logs
- **File**: `logs/feature_extraction.log`
- **Content**: MIDI processing, feature data
- **Format**: JSON with timestamps

#### 2. Model Training Logs
- **File**: `logs/model_training.log`
- **Content**: Training metrics, performance data
- **Format**: JSON with timestamps

#### 3. Prediction Logs
- **File**: `logs/predictions.log`
- **Content**: Input data, predictions, confidence
- **Format**: JSON with timestamps

#### 4. System Event Logs
- **File**: `logs/system_events.log`
- **Content**: System events, errors, warnings
- **Format**: JSON with timestamps

#### 5. Performance Logs
- **File**: `logs/performance.log`
- **Content**: Operation timing, resource usage
- **Format**: Structured performance data

### Log Management

```bash
# View recent logs
tail -f logs/aamati.log

# View error logs
tail -f logs/aamati_errors.log

# View performance logs
tail -f logs/performance.log

# Clean up old logs (30+ days)
python3 logging_config.py --cleanup
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Integration Test Failures

**Python Environment Issues**
```bash
# Check Python version
python3 --version

# Install missing dependencies
pip install pandas numpy scikit-learn joblib pretty_midi scipy matplotlib seaborn onnx
```

**ML System Issues**
```bash
# Check model files
ls -la MLPython/ModelClassificationScripts/models/

# Verify data directories
ls -la MLPython/data/csv/
ls -la MLPython/MusicGroovesMIDI/TrainingMIDIs/
```

**JUCE System Issues**
```bash
# Check source files
ls -la Source/

# Verify CMake
cmake --version

# Check build directory
ls -la build/
```

#### 2. Health Check Issues

**High Resource Usage**
- Check for memory leaks
- Optimize batch processing
- Clean up temporary files

**Model Loading Failures**
- Verify model file integrity
- Check file permissions
- Re-train models if corrupted

**Data Access Issues**
- Check file permissions
- Verify directory structure
- Ensure sufficient disk space

#### 3. Performance Issues

**Slow Feature Extraction**
- Reduce batch size
- Optimize MIDI processing
- Use non-interactive mode

**High Memory Usage**
- Process smaller batches
- Clear unused variables
- Monitor memory leaks

**Slow Model Loading**
- Implement lazy loading
- Cache loaded models
- Optimize model files

### Debug Mode

```bash
# Enable debug logging
export AAMATI_DEBUG=1

# Run tests with debug output
python3 run_tests.py --verbose

# Check detailed logs
grep "DEBUG" logs/aamati.log
```

## 📈 Continuous Integration

### Automated Testing

#### GitHub Actions (if using Git)
```yaml
name: Aamati Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python3 run_tests.py --verbose
```

#### Local Automation
```bash
# Create test script
cat > run_daily_tests.sh << 'EOF'
#!/bin/bash
cd /path/to/aamati
python3 run_tests.py --verbose
python3 system_health.py --report
EOF

chmod +x run_daily_tests.sh

# Add to crontab for daily testing
crontab -e
# Add: 0 2 * * * /path/to/aamati/run_daily_tests.sh
```

## 📋 Test Reports

### Report Formats

#### 1. Console Output
- Real-time test progress
- Color-coded status indicators
- Summary statistics

#### 2. JSON Reports
- **File**: `aamati_test_report.json`
- **Content**: Detailed test results
- **Format**: Machine-readable JSON

#### 3. Health Reports
- **File**: `aamati_health_report.txt`
- **Content**: System health status
- **Format**: Human-readable text

### Report Analysis

```bash
# View test results
cat aamati_test_report.json | jq '.'

# Check health status
python3 system_health.py --report

# Analyze performance data
grep "PERFORMANCE" logs/performance.log
```

## 🎯 Best Practices

### Testing Strategy

1. **Run tests regularly** - Daily health checks, weekly full tests
2. **Monitor performance** - Track resource usage and optimization
3. **Log everything** - Comprehensive logging for debugging
4. **Automate testing** - Use scripts and cron jobs
5. **Document issues** - Keep track of problems and solutions

### Performance Optimization

1. **Batch processing** - Process multiple files together
2. **Memory management** - Clean up unused resources
3. **Caching** - Cache frequently used data
4. **Parallel processing** - Use multiple cores when possible
5. **Resource monitoring** - Track and optimize usage

### Maintenance

1. **Regular cleanup** - Remove old logs and temporary files
2. **Update dependencies** - Keep packages current
3. **Monitor disk space** - Ensure sufficient storage
4. **Backup data** - Regular backups of training data
5. **Version control** - Track changes and rollbacks

## 🆘 Getting Help

### Debug Information

```bash
# Generate debug report
python3 run_tests.py --verbose > debug_report.txt 2>&1

# Check system status
python3 system_health.py --report

# View recent errors
grep "ERROR" logs/aamati_errors.log | tail -20
```

### Support Resources

- **Logs**: Check `logs/` directory for detailed information
- **Reports**: Review test and health reports
- **Documentation**: Refer to other guide files
- **Troubleshooting**: Use debug mode and verbose output

---

**🎵 Happy Testing with Aamati! 🎵**

*This testing system ensures your Aamati installation is robust, performant, and ready for production use.*
