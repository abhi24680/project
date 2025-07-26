# Smart Energy Saver System 🔋

An intelligent energy management system that uses computer vision and motion detection to automatically control lights and fans in classrooms, offices, or any indoor space. The system helps reduce energy consumption by turning off appliances when no motion is detected for a specified period.

## 🌟 Features

- **Real-time Motion Detection**: Uses OpenCV and background subtraction algorithms
- **Automatic Appliance Control**: Controls lights and fans based on occupancy
- **Configurable Timeout**: Customizable no-motion timeout periods
- **Multiple Control Methods**: Supports GPIO (Raspberry Pi) and MQTT protocols
- **Event Logging**: Comprehensive logging of all motion events and actions
- **Statistics Tracking**: Daily statistics and analytics
- **Visual Interface**: Real-time video feed with motion detection overlay
- **Command Line Interface**: Full CLI support with various options

## 🎯 Use Cases

- **Classrooms**: Automatically manage lighting and ventilation
- **Offices**: Reduce energy costs in meeting rooms and workspaces
- **Smart Homes**: Integrate with home automation systems
- **Commercial Buildings**: Large-scale energy management

## 📋 Requirements

### Software Requirements
- Python 3.7 or higher
- OpenCV 4.5+
- NumPy
- Camera (webcam or USB camera)

### Hardware Requirements (Optional)
- Raspberry Pi (for GPIO control)
- Relay modules for appliance control
- MQTT broker (for IoT integration)

## 🚀 Quick Start

### 1. Clone or Download
```bash
# If you have the files, ensure you're in the project directory
cd smart-energy-saver
```

### 2. Automatic Setup
```bash
# Run the setup script (Linux/macOS)
./setup.sh

# Or manually install dependencies
pip install -r requirements.txt
```

### 3. Run the System
```bash
# Basic usage with default settings
python3 smart_energy_saver.py

# With custom settings
python3 smart_energy_saver.py --timeout 30 --camera 0
```

### 4. Demo Mode (No Camera Required)
```bash
# Run demo simulation
python3 demo_no_camera.py --duration 30
```

## ⚙️ Configuration

### Command Line Options
```bash
python3 smart_energy_saver.py [OPTIONS]

Options:
  --camera INDEX        Camera index (default: 0)
  --timeout SECONDS     No motion timeout (default: 60)
  --sensitivity VALUE   Motion sensitivity (default: 25)
  --min-area PIXELS     Minimum motion area (default: 1000)
  --help               Show help message
```

### Configuration File
Edit `config.json` to customize system behavior:

```json
{
  "camera": {
    "index": 0,
    "width": 640,
    "height": 480,
    "fps": 30
  },
  "motion_detection": {
    "sensitivity": 25,
    "min_area": 1000,
    "var_threshold": 50,
    "detect_shadows": true
  },
  "energy_control": {
    "no_motion_timeout": 60,
    "use_gpio": false,
    "use_mqtt": false
  }
}
```

## 🎮 Controls

While the system is running:

- **q**: Quit the application
- **s**: Show current daily statistics
- **r**: Reset motion timer
- **ESC**: Exit (alternative to 'q')

## 🔌 Hardware Integration

### GPIO Control (Raspberry Pi)
1. Uncomment GPIO imports in `smart_energy_saver.py`
2. Install RPi.GPIO: `pip install RPi.GPIO`
3. Connect relay modules to pins 18 (lights) and 19 (fans)
4. Set `use_gpio: true` in configuration

### MQTT Integration
1. Install MQTT client: `pip install paho-mqtt`
2. Set up MQTT broker (e.g., Mosquitto)
3. Configure MQTT settings in `config.json`
4. Set `use_mqtt: true` in configuration

## 📊 Monitoring and Analytics

### Log Files
- `energy_saver.log`: Detailed system logs
- `motion_events.json`: Motion events in JSON format
- `demo_results.json`: Demo simulation results

### Daily Statistics
The system tracks:
- Total motion detections
- Energy saving events
- System uptime
- Appliance usage patterns

## 🛠️ Customization

### Motion Detection Parameters
- **Sensitivity**: Lower values = more sensitive
- **Min Area**: Minimum pixel area to consider as motion
- **Timeout**: Seconds to wait before turning off appliances

### Adding New Appliance Types
Extend the `EnergyController` class to support additional devices:

```python
class EnergyController:
    def __init__(self):
        self.air_conditioning = True
        # ... existing code ...
    
    def control_ac(self, state):
        # Add AC control logic
        pass
```

## 🚨 Troubleshooting

### Camera Issues
```bash
# Check available cameras
python3 -c "import cv2; print('Camera available:', cv2.VideoCapture(0).isOpened())"

# Try different camera indices
python3 smart_energy_saver.py --camera 1
```

### Permission Issues (Linux)
```bash
# Add user to video group
sudo usermod -a -G video $USER

# For GPIO access
sudo usermod -a -G gpio $USER
```

### Performance Issues
- Reduce camera resolution in config.json
- Increase motion detection threshold
- Lower frame rate if CPU usage is high

## 📁 Project Structure

```
smart-energy-saver/
├── smart_energy_saver.py    # Main application
├── demo_no_camera.py        # Demo without camera
├── requirements.txt         # Dependencies
├── config.json             # Configuration
├── setup.sh                # Setup script
├── README.md               # Documentation
├── energy_saver.log        # Runtime logs
└── motion_events.json      # Event data
```

## 🔒 Security Considerations

- **Camera Privacy**: System processes video locally
- **Network Security**: Use secure MQTT configurations
- **Access Control**: Implement authentication for remote access
- **Data Privacy**: Motion events contain timestamps only

## 🌱 Environmental Impact

### Energy Savings Potential
- **Classroom**: Up to 30% reduction in lighting costs
- **Office Space**: 25-40% savings on HVAC costs
- **24/7 Monitoring**: Prevents overnight energy waste

### Carbon Footprint Reduction
- Automatically reduces unnecessary energy consumption
- Provides data for energy optimization
- Supports sustainable building practices

## 🤝 Contributing

### Areas for Improvement
- Machine learning for better motion detection
- Mobile app for remote monitoring
- Integration with smart home platforms
- Advanced analytics and reporting

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python3 -m pytest tests/

# Code formatting
black smart_energy_saver.py
```

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🆘 Support

### Common Issues
1. **Camera not detected**: Check camera permissions and connections
2. **High CPU usage**: Reduce video resolution or frame rate
3. **GPIO errors**: Ensure proper permissions and hardware connections

### Getting Help
- Check the troubleshooting section above
- Review log files for error messages
- Test with the demo mode first

## 📈 Future Enhancements

- [ ] Web-based dashboard
- [ ] Mobile app integration
- [ ] Machine learning motion prediction
- [ ] Multi-room support
- [ ] Energy usage analytics
- [ ] Integration with smart plugs
- [ ] Voice control support
- [ ] Automated scheduling

---

**Made with ❤️ for a sustainable future** 🌍