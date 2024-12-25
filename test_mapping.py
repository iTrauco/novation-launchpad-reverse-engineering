#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test Mapping Script with Debug Logging
Maps specific aliases to buttons and provides real-time feedback.
"""

from src.app import LaunchpadApp
from src.utils.constants import Colors
import logging
import time

# Setup ultra-verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    print("\n🚀 Initializing Launchpad Test...")
    
    # Initialize app
    app = LaunchpadApp()
    
    # Define our test mappings (starting with known working ones)
    test_mappings = [
        # x, y, color, alias
        (4, 4, Colors.RED, "claude1"),    # Known working
        (1, 5, Colors.BLUE, "claude3"),   # Known working
        (1, 1, Colors.GREEN, "claude2"),  # Test mapping
        (5, 1, Colors.YELLOW, "claude4")  # Test mapping
    ]
    
    # Register all mappings with detailed logging
    print("\n📍 Registering button mappings...")
    for x, y, color, alias in test_mappings:
        print(f"\n🔧 Mapping button ({x}, {y}):")
        print(f"   Alias: {alias}")
        print(f"   Color: {color}")
        app.add_mapping(x, y, color, alias)
        
    # Print test configuration
    print("\n🎮 Test Configuration Active")
    print("===========================")
    print("Mapped Buttons:")
    for x, y, color, alias in test_mappings:
        status = "✅ Known Working" if alias in ["claude1", "claude3"] else "🔄 Testing"
        print(f"  • ({x}, {y}) -> {alias}")
        print(f"    Color: {color}")
        print(f"    Status: {status}")
    
    print("\n📝 Debug Information:")
    print("  • Every button press will show coordinates")
    print("  • Successful triggers will be logged")
    print("  • Press buttons to see detailed mapping info")
    print("  • Check terminal for real-time debug output")
    print("\n⌨️  Press Ctrl+C to exit and see session summary\n")
    
    # Run the app
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Test session ended")

if __name__ == "__main__":
    main()
