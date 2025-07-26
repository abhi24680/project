#!/usr/bin/env python3
"""
System Test Script for Smart Energy Saver
Tests all components without requiring a camera
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
        print(f"   OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        print(f"   NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import logging, json, threading, time, argparse
        print("✅ Standard library modules imported successfully")
    except ImportError as e:
        print(f"❌ Standard library import failed: {e}")
        return False
    
    return True

def test_classes():
    """Test if all custom classes can be instantiated"""
    print("\n🧪 Testing class instantiation...")
    
    try:
        # Import the main script as a module
        sys.path.append('.')
        from smart_energy_saver import EnergyController, MotionDetector, EventLogger, SmartEnergySaver
        
        # Test EnergyController
        controller = EnergyController()
        print("✅ EnergyController instantiated successfully")
        
        # Test MotionDetector
        detector = MotionDetector()
        print("✅ MotionDetector instantiated successfully")
        
        # Test EventLogger
        logger = EventLogger()
        print("✅ EventLogger instantiated successfully")
        
        # Test SmartEnergySaver
        saver = SmartEnergySaver()
        print("✅ SmartEnergySaver instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Class instantiation failed: {e}")
        traceback.print_exc()
        return False

def test_energy_controller():
    """Test EnergyController functionality"""
    print("\n🧪 Testing EnergyController...")
    
    try:
        from smart_energy_saver import EnergyController
        
        controller = EnergyController()
        
        # Test initial state
        assert controller.lights_on == True
        assert controller.fans_on == True
        print("✅ Initial state correct")
        
        # Test turning off appliances
        result = controller.turn_off_appliances()
        assert result == True
        assert controller.lights_on == False
        assert controller.fans_on == False
        print("✅ Turn off functionality works")
        
        # Test turning on appliances
        result = controller.turn_on_appliances()
        assert result == True
        assert controller.lights_on == True
        assert controller.fans_on == True
        print("✅ Turn on functionality works")
        
        return True
        
    except Exception as e:
        print(f"❌ EnergyController test failed: {e}")
        return False

def test_motion_detector():
    """Test MotionDetector with synthetic data"""
    print("\n🧪 Testing MotionDetector...")
    
    try:
        import numpy as np
        from smart_energy_saver import MotionDetector
        
        detector = MotionDetector()
        
        # Create a synthetic frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Test motion detection (should return no motion for first frames)
        motion_detected, fg_mask, contours = detector.detect_motion(frame)
        print("✅ Motion detection method works")
        print(f"   Motion detected: {motion_detected}")
        print(f"   Contours found: {len(contours)}")
        
        return True
        
    except Exception as e:
        print(f"❌ MotionDetector test failed: {e}")
        return False

def test_event_logger():
    """Test EventLogger functionality"""
    print("\n🧪 Testing EventLogger...")
    
    try:
        from smart_energy_saver import EventLogger
        
        logger = EventLogger("test_energy_saver.log")
        
        # Test logging an event
        logger.log_motion_event(True, "ON")
        logger.log_motion_event(False, "OFF")
        print("✅ Event logging works")
        
        # Test statistics
        stats = logger.get_daily_stats()
        print(f"✅ Statistics generation works: {stats}")
        
        # Test saving events
        logger.save_events_to_file("test_motion_events.json")
        print("✅ Event saving works")
        
        return True
        
    except Exception as e:
        print(f"❌ EventLogger test failed: {e}")
        return False

def test_configuration():
    """Test configuration file loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        import json
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check required sections
        required_sections = ['camera', 'motion_detection', 'energy_control', 'mqtt', 'logging']
        for section in required_sections:
            assert section in config, f"Missing section: {section}"
        
        print("✅ Configuration file is valid")
        print(f"   Camera index: {config['camera']['index']}")
        print(f"   Timeout: {config['energy_control']['no_motion_timeout']}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    import os
    
    test_files = [
        'test_energy_saver.log',
        'test_motion_events.json'
    ]
    
    for file in test_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass

def main():
    """Run all tests"""
    print("🚀 Smart Energy Saver System Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Classes", test_classes),
        ("EnergyController", test_energy_controller),
        ("MotionDetector", test_motion_detector),
        ("EventLogger", test_event_logger),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Connect a camera")
        print("2. Run: python3 smart_energy_saver.py")
        print("3. Or try the demo: python3 demo_no_camera.py")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    # Clean up test files
    cleanup_test_files()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)