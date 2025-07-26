#!/usr/bin/env python3
"""
Smart Energy Saver using Motion Detection with OpenCV
Automatically controls lights and fans based on classroom occupancy
"""

import cv2
import numpy as np
import time
import logging
from datetime import datetime
import json
import threading
from typing import Optional, Tuple, Dict, Any
import argparse

# For GPIO control (uncomment when using Raspberry Pi)
# import RPi.GPIO as GPIO

# For MQTT communication (optional)
# import paho.mqtt.client as mqtt


class EnergyController:
    """Handles the control of electrical appliances"""
    
    def __init__(self, use_gpio: bool = False, use_mqtt: bool = False):
        self.use_gpio = use_gpio
        self.use_mqtt = use_mqtt
        self.lights_on = True
        self.fans_on = True
        
        if self.use_gpio:
            self.setup_gpio()
        
        if self.use_mqtt:
            self.setup_mqtt()
    
    def setup_gpio(self):
        """Initialize GPIO pins for relay control"""
        # GPIO.setmode(GPIO.BCM)
        # self.LIGHT_PIN = 18
        # self.FAN_PIN = 19
        # GPIO.setup(self.LIGHT_PIN, GPIO.OUT)
        # GPIO.setup(self.FAN_PIN, GPIO.OUT)
        # GPIO.output(self.LIGHT_PIN, GPIO.HIGH)  # Lights ON initially
        # GPIO.output(self.FAN_PIN, GPIO.HIGH)    # Fans ON initially
        print("GPIO setup completed (simulated)")
    
    def setup_mqtt(self):
        """Initialize MQTT client for IoT communication"""
        # self.mqtt_client = mqtt.Client()
        # self.mqtt_client.connect("localhost", 1883, 60)
        print("MQTT setup completed (simulated)")
    
    def turn_off_appliances(self):
        """Turn off lights and fans"""
        if self.lights_on or self.fans_on:
            print("🔴 ENERGY SAVING: Turning OFF lights and fans")
            
            if self.use_gpio:
                # GPIO.output(self.LIGHT_PIN, GPIO.LOW)
                # GPIO.output(self.FAN_PIN, GPIO.LOW)
                pass
            
            if self.use_mqtt:
                # self.mqtt_client.publish("classroom/lights", "OFF")
                # self.mqtt_client.publish("classroom/fans", "OFF")
                pass
            
            self.lights_on = False
            self.fans_on = False
            return True
        return False
    
    def turn_on_appliances(self):
        """Turn on lights and fans"""
        if not self.lights_on or not self.fans_on:
            print("🟢 MOTION DETECTED: Turning ON lights and fans")
            
            if self.use_gpio:
                # GPIO.output(self.LIGHT_PIN, GPIO.HIGH)
                # GPIO.output(self.FAN_PIN, GPIO.HIGH)
                pass
            
            if self.use_mqtt:
                # self.mqtt_client.publish("classroom/lights", "ON")
                # self.mqtt_client.publish("classroom/fans", "ON")
                pass
            
            self.lights_on = True
            self.fans_on = True
            return True
        return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.use_gpio:
            # GPIO.cleanup()
            pass


class MotionDetector:
    """Handles motion detection using OpenCV"""
    
    def __init__(self, sensitivity: int = 25, min_area: int = 1000):
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            detectShadows=True, varThreshold=50
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, list]:
        """
        Detect motion in the given frame
        Returns: (motion_detected, processed_frame, contours)
        """
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(frame)
        
        # Remove shadows
        fg_mask[fg_mask == 127] = 0
        
        # Morphological operations to reduce noise
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, self.kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, self.kernel)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        significant_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                motion_detected = True
                significant_contours.append(contour)
        
        return motion_detected, fg_mask, significant_contours


class EventLogger:
    """Handles logging of motion events and system actions"""
    
    def __init__(self, log_file: str = "energy_saver.log"):
        self.log_file = log_file
        self.setup_logging()
        self.events = []
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_motion_event(self, detected: bool, appliance_action: str = None):
        """Log motion detection events"""
        timestamp = datetime.now()
        event = {
            'timestamp': timestamp.isoformat(),
            'motion_detected': detected,
            'appliance_action': appliance_action
        }
        
        self.events.append(event)
        
        if detected:
            self.logger.info(f"Motion detected at {timestamp}")
        else:
            self.logger.info(f"No motion detected at {timestamp}")
        
        if appliance_action:
            self.logger.info(f"Appliance action: {appliance_action}")
    
    def save_events_to_file(self, filename: str = "motion_events.json"):
        """Save events to JSON file for analytics"""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def get_daily_stats(self) -> Dict[str, Any]:
        """Get daily statistics"""
        today = datetime.now().date()
        today_events = [e for e in self.events 
                       if datetime.fromisoformat(e['timestamp']).date() == today]
        
        motion_count = sum(1 for e in today_events if e['motion_detected'])
        energy_saves = sum(1 for e in today_events if e['appliance_action'] == 'OFF')
        
        return {
            'date': today.isoformat(),
            'total_events': len(today_events),
            'motion_detections': motion_count,
            'energy_saves': energy_saves
        }


class SmartEnergySaver:
    """Main class that orchestrates the energy saving system"""
    
    def __init__(self, camera_index: int = 0, no_motion_timeout: int = 60):
        self.camera_index = camera_index
        self.no_motion_timeout = no_motion_timeout
        self.last_motion_time = time.time()
        self.running = False
        
        # Initialize components
        self.motion_detector = MotionDetector()
        self.energy_controller = EnergyController()
        self.logger = EventLogger()
        
        # Video capture
        self.cap = None
        
        # Threading for non-blocking operation
        self.timer_thread = None
        self.timer_running = False
    
    def initialize_camera(self) -> bool:
        """Initialize the camera"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"Camera {self.camera_index} initialized successfully")
        return True
    
    def timer_worker(self):
        """Worker thread that monitors the no-motion timeout"""
        while self.timer_running:
            current_time = time.time()
            time_since_motion = current_time - self.last_motion_time
            
            if time_since_motion >= self.no_motion_timeout:
                if self.energy_controller.lights_on or self.energy_controller.fans_on:
                    if self.energy_controller.turn_off_appliances():
                        self.logger.log_motion_event(False, "OFF")
            
            time.sleep(1)  # Check every second
    
    def draw_info_overlay(self, frame: np.ndarray, motion_detected: bool, 
                         time_since_motion: float) -> np.ndarray:
        """Draw information overlay on the frame"""
        overlay = frame.copy()
        
        # Status information
        status_text = "MOTION DETECTED" if motion_detected else "NO MOTION"
        status_color = (0, 255, 0) if motion_detected else (0, 0, 255)
        
        cv2.putText(overlay, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        
        # Timer information
        remaining_time = max(0, self.no_motion_timeout - time_since_motion)
        timer_text = f"Time to shutdown: {remaining_time:.1f}s"
        cv2.putText(overlay, timer_text, (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Appliance status
        lights_status = "ON" if self.energy_controller.lights_on else "OFF"
        fans_status = "ON" if self.energy_controller.fans_on else "OFF"
        
        cv2.putText(overlay, f"Lights: {lights_status}", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(overlay, f"Fans: {fans_status}", (10, 140), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(overlay, current_time, (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return overlay
    
    def run(self):
        """Main execution loop"""
        if not self.initialize_camera():
            return
        
        self.running = True
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.timer_worker)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
        print("Smart Energy Saver started. Press 'q' to quit.")
        print(f"No motion timeout: {self.no_motion_timeout} seconds")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Detect motion
                motion_detected, fg_mask, contours = self.motion_detector.detect_motion(frame)
                
                current_time = time.time()
                time_since_motion = current_time - self.last_motion_time
                
                # Handle motion detection
                if motion_detected:
                    self.last_motion_time = current_time
                    if self.energy_controller.turn_on_appliances():
                        self.logger.log_motion_event(True, "ON")
                    
                    # Draw contours on frame
                    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
                
                # Draw information overlay
                display_frame = self.draw_info_overlay(frame, motion_detected, time_since_motion)
                
                # Show frames
                cv2.imshow('Smart Energy Saver - Main Feed', display_frame)
                cv2.imshow('Motion Detection', fg_mask)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current statistics
                    stats = self.logger.get_daily_stats()
                    print(f"Daily stats: {stats}")
                elif key == ord('r'):
                    # Reset motion timer
                    self.last_motion_time = current_time
                    print("Motion timer reset")
        
        except KeyboardInterrupt:
            print("\nShutdown requested by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        
        self.running = False
        self.timer_running = False
        
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=2)
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        # Save events and statistics
        self.logger.save_events_to_file()
        stats = self.logger.get_daily_stats()
        print(f"Final daily statistics: {stats}")
        
        self.energy_controller.cleanup()
        print("Cleanup completed")


def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='Smart Energy Saver using Motion Detection')
    parser.add_argument('--camera', type=int, default=0, 
                       help='Camera index (default: 0)')
    parser.add_argument('--timeout', type=int, default=60, 
                       help='No motion timeout in seconds (default: 60)')
    parser.add_argument('--sensitivity', type=int, default=25, 
                       help='Motion detection sensitivity (default: 25)')
    parser.add_argument('--min-area', type=int, default=1000, 
                       help='Minimum area for motion detection (default: 1000)')
    
    args = parser.parse_args()
    
    # Create and run the energy saver system
    energy_saver = SmartEnergySaver(
        camera_index=args.camera,
        no_motion_timeout=args.timeout
    )
    
    # Configure motion detector with custom parameters
    energy_saver.motion_detector.sensitivity = args.sensitivity
    energy_saver.motion_detector.min_area = args.min_area
    
    try:
        energy_saver.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        energy_saver.cleanup()


if __name__ == "__main__":
    main()