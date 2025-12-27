#!/usr/bin/env python3
import os
import sys
from modules.generator import Generation
from modules.logger import Banner, Info, Success

def main():
    """Main entry point"""
    
    # Print banner
    Banner()
    
    # Check if running on Railway
    if os.getenv('RAILWAY_ENVIRONMENT'):
        Info("🚂 Running on Railway")
        Info("📋 Configuration loaded from environment variables")
    
    # Start generation
    try:
        Generation()
    except KeyboardInterrupt:
        Info("\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Don't wait for input on Railway (runs in background)
    if not os.getenv('RAILWAY_ENVIRONMENT'):
        print("\nPress enter to exit...")
        input()

if __name__ == "__main__":
    main()
