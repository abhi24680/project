#!/usr/bin/env python3
"""
Smart Energy Saver Demo - No Camera Required
Simulates motion detection for testing and demonstration purposes
"""

import time
import random
import threading
from datetime import datetime
import json

class MockMotionDetector:
    """Simulates motion detection for demo purposes"""
    
    def __init__(self):
        self.motion_probability = 0.3  # 30% chance of motion per check
    
    def detect_motion(self):
        """Simulate motion detection"""
        return random.random() < self.motion_probability

class EnergyController:
    """Handles the control of electrical appliances"""
    
    def __init__(self):
        self.lights_on = True
        self.fans_on = True
    
    def turn_off_appliances(self):
        """Turn off lights and fans"""
        if self.lights_on or self.fans_on:
            print("🔴 ENERGY SAVING: Turning OFF lights and fans")
            self.lights_on = False
            self.fans_on = False
            return True
        return False
    
    def turn_on_appliances(self):
        """Turn on lights and fans"""
        if not self.lights_on or not self.fans_on:
            print("🟢 MOTION DETECTED: Turning ON lights and fans")
            self.lights_on = True
            self.fans_on = True
            return True
        return False

class DemoEnergySaver:
    """Demo version of the energy saver system"""
    
    def __init__(self, no_motion_timeout=10):  # Shorter timeout for demo
        self.no_motion_timeout = no_motion_timeout
        self.last_motion_time = time.time()
        self.running = False
        
        self.motion_detector = MockMotionDetector()
        self.energy_controller = EnergyController()
        self.events = []
    
    def log_event(self, motion_detected, action=None):
        """Log events for demo"""
        timestamp = datetime.now()
        event = {
            'timestamp': timestamp.strftime("%H:%M:%S"),
            'motion_detected': motion_detected,
            'action': action
        }
        self.events.append(event)
        
        if motion_detected:
            print(f"📹 [{event['timestamp']}] Motion detected!")
        else:
            print(f"⏰ [{event['timestamp']}] No motion - timeout reached")
    
    def run_demo(self, duration=60):
        """Run the demo for specified duration"""
        print("🎬 Starting Smart Energy Saver Demo")
        print(f"⏱️  Demo duration: {duration} seconds")
        print(f"🔄 Motion check interval: 2 seconds")
        print(f"⏰ No motion timeout: {self.no_motion_timeout} seconds")
        print("-" * 50)
        
        start_time = time.time()
        self.running = True
        
        try:
            while self.running and (time.time() - start_time) < duration:
                # Simulate motion detection check
                motion_detected = self.motion_detector.detect_motion()
                current_time = time.time()
                time_since_motion = current_time - self.last_motion_time
                
                if motion_detected:
                    self.last_motion_time = current_time
                    if self.energy_controller.turn_on_appliances():
                        self.log_event(True, "Appliances turned ON")
                else:
                    # Check if timeout reached
                    if time_since_motion >= self.no_motion_timeout:
                        if self.energy_controller.lights_on or self.energy_controller.fans_on:
                            if self.energy_controller.turn_off_appliances():
                                self.log_event(False, "Appliances turned OFF")
                
                # Display current status
                status = f"Lights: {'ON' if self.energy_controller.lights_on else 'OFF'} | "
                status += f"Fans: {'ON' if self.energy_controller.fans_on else 'OFF'} | "
                status += f"Time since motion: {time_since_motion:.1f}s"
                print(f"📊 Status: {status}")
                
                time.sleep(2)  # Check every 2 seconds for demo
                
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        
        self.running = False
        self.show_summary()
    
    def show_summary(self):
        """Show demo summary"""
        print("\n" + "=" * 50)
        print("📈 DEMO SUMMARY")
        print("=" * 50)
        
        motion_events = [e for e in self.events if e['motion_detected']]
        energy_saves = [e for e in self.events if e['action'] == 'Appliances turned OFF']
        
        print(f"📹 Total motion detections: {len(motion_events)}")
        print(f"💡 Total energy save events: {len(energy_saves)}")
        print(f"📊 Total events logged: {len(self.events)}")
        
        if self.events:
            print("\n⏰ Event Timeline:")
            for event in self.events[-10:]:  # Show last 10 events
                status = "🟢 Motion" if event['motion_detected'] else "🔴 Timeout"
                print(f"  {event['timestamp']} - {status} - {event['action']}")
        
        # Save demo results
        with open('demo_results.json', 'w') as f:
            json.dump({
                'demo_summary': {
                    'motion_detections': len(motion_events),
                    'energy_saves': len(energy_saves),
                    'total_events': len(self.events)
                },
                'events': self.events
            }, f, indent=2)
        
        print(f"\n💾 Demo results saved to 'demo_results.json'")

def main():
    """Main demo function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Energy Saver Demo (No Camera)')
    parser.add_argument('--duration', type=int, default=60, 
                       help='Demo duration in seconds (default: 60)')
    parser.add_argument('--timeout', type=int, default=10, 
                       help='No motion timeout in seconds (default: 10)')
    
    args = parser.parse_args()
    
    demo = DemoEnergySaver(no_motion_timeout=args.timeout)
    demo.run_demo(duration=args.duration)

if __name__ == "__main__":
    main()