#!/usr/bin/env python3
"""
RF Signal Detector CLI
Advanced wireless signal detection and analysis tool
"""

import argparse
import sys
import time
from datetime import datetime
import json
import numpy as np
from .detector import RFDetector
from .visualizer import SignalVisualizer

def main():
    parser = argparse.ArgumentParser(
        description='RF Signal Detector - Advanced Wireless Signal Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Examples:
  rf-detector scan                          # Basic scan
  rf-detector scan -b 2.4G                  # Scan 2.4GHz band
  rf-detector scan -b 5G -t 30             # Scan 5GHz for 30 seconds
  rf-detector monitor -c 6 -o output.json   # Monitor channel 6 and save results
  rf-detector analyze -f scan_results.json  # Analyze previous scan
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for RF signals')
    scan_parser.add_argument('-b', '--band', choices=['2.4G', '5G', 'all'], 
                           default='2.4G', help='Frequency band to scan')
    scan_parser.add_argument('-t', '--time', type=int, default=60, 
                           help='Scan duration in seconds')
    scan_parser.add_argument('-o', '--output', help='Output file for results')
    scan_parser.add_argument('-v', '--visualize', action='store_true',
                           help='Show real-time visualization')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor specific channel')
    monitor_parser.add_argument('-c', '--channel', type=int, required=True,
                              help='WiFi channel to monitor')
    monitor_parser.add_argument('-t', '--time', type=int, default=300,
                              help='Monitoring duration in seconds')
    monitor_parser.add_argument('-o', '--output', help='Output file')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze scan results')
    analyze_parser.add_argument('-f', '--file', required=True, help='Scan results file')
    analyze_parser.add_argument('-p', '--plot', action='store_true',
                              help='Generate plots')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'scan':
            return run_scan(args)
        elif args.command == 'monitor':
            return run_monitor(args)
        elif args.command == 'analyze':
            return run_analyze(args)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        return 130
    except Exception as e:
        print(f"[!] Error: {e}")
        return 1

def run_scan(args):
    """Execute scan command"""
    print(f"[+] Starting RF scan on {args.band} band for {args.time} seconds...")
    print("[+] Press Ctrl+C to stop\n")
    
    detector = RFDetector()
    visualizer = SignalVisualizer() if args.visualize else None
    
    results = detector.scan_band(args.band, args.time, visualizer)
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {args.output}")
    
    # Print summary
    print_summary(results)
    return 0

def run_monitor(args):
    """Execute monitor command"""
    print(f"[+] Monitoring channel {args.channel} for {args.time} seconds...")
    
    detector = RFDetector()
    results = detector.monitor_channel(args.channel, args.time)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {args.output}")
    
    return 0

def run_analyze(args):
    """Execute analyze command"""
    print(f"[+] Analyzing results from {args.file}...")
    
    with open(args.file, 'r') as f:
        data = json.load(f)
    
    visualizer = SignalVisualizer()
    visualizer.analyze_results(data, args.plot)
    
    return 0

def print_summary(results):
    """Print scan summary"""
    print("\n" + "="*50)
    print("SCAN SUMMARY")
    print("="*50)
    print(f"Total signals detected: {results['summary']['total_signals']}")
    print(f"Scan duration: {results['summary']['duration']}s")
    print(f"Average signal strength: {results['summary']['avg_strength']} dBm")
    print(f"Strongest signal: {results['summary']['max_strength']} dBm")
    print(f"Unique channels: {len(results['summary']['channels'])}")
    
    if results['devices']:
        print("\nTOP DEVICES:")
        for device in results['devices'][:5]:
            print(f"  {device['ssid'] or 'Hidden'} - {device['strength']} dBm")

if __name__ == '__main__':
    sys.exit(main())
