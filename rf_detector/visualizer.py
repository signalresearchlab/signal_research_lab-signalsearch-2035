import time
import json
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import numpy as np
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

class SignalVisualizer:
    """Advanced Signal Visualization"""
    
    def __init__(self):
        self.fig = None
    
    def realtime_plot(self, detector, duration):
        """Real-time signal strength visualization"""
        if not PLOTTING_AVAILABLE:
            print("[!] matplotlib not available for real-time plotting")
            return
        
        plt.ion()
        self.fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        start_time = time.time()
        timestamps = []
        strengths = []
        channels = []
        
        while time.time() - start_time < duration and detector.is_scanning:
            if detector.results['devices']:
                # Update data
                latest = detector.results['devices'][-1]
                timestamps.append(time.time() - start_time)
                strengths.append(latest['strength'])
                channels.append(latest['channel'])
                
                # Clear and replot
                ax1.clear()
                ax2.clear()
                
                # Signal strength over time
                ax1.plot(timestamps, strengths, 'b-', alpha=0.7)
                ax1.set_title('Signal Strength Over Time')
                ax1.set_ylabel('Strength (dBm)')
                ax1.grid(True, alpha=0.3)
                
                # Channel distribution
                ax2.hist(channels, bins=20, alpha=0.7, edgecolor='black')
                ax2.set_title('Channel Distribution')
                ax2.set_xlabel('Channel')
                ax2.set_ylabel('Count')
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.pause(0.1)
            
            time.sleep(1)
        
        plt.ioff()
    
    def analyze_results(self, data, generate_plots=False):
        """Analyze and visualize scan results"""
        if not data.get('devices'):
            print("No data to analyze")
            return
        
        print("\n" + "="*50)
        print("DETAILED ANALYSIS")
        print("="*50)
        
        # Channel analysis
        channels = [d['channel'] for d in data['devices']]
        unique_channels = set(channels)
        
        print(f"Channels with activity: {sorted(unique_channels)}")
        
        # Strength analysis
        strengths = [d['strength'] for d in data['devices']]
        print(f"Signal strength range: {min(strengths)} to {max(strengths)} dBm")
        
        # Security analysis
        security = {}
        for device in data['devices']:
            sec = device.get('security', 'Unknown')
            security[sec] = security.get(sec, 0) + 1
        
        print("\nSecurity Types:")
        for sec_type, count in security.items():
            print(f"  {sec_type}: {count} networks")
        
        if generate_plots and PLOTTING_AVAILABLE:
            self._generate_analysis_plots(data)
    
    def _generate_analysis_plots(self, data):
        """Generate detailed analysis plots"""
        if not PLOTTING_AVAILABLE:
            print("[!] matplotlib not available for plotting")
            return
        
        devices = data['devices']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Channel distribution
        channels = [d['channel'] for d in devices]
        ax1.hist(channels, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Channel Distribution')
        ax1.set_xlabel('Channel')
        ax1.set_ylabel('Number of Networks')
        
        # Signal strength distribution
        strengths = [d['strength'] for d in devices]
        ax2.hist(strengths, bins=15, alpha=0.7, color='lightcoral', edgecolor='black')
        ax2.set_title('Signal Strength Distribution')
        ax2.set_xlabel('Strength (dBm)')
        ax2.set_ylabel('Count')
        
        # Channel vs Strength
        ax3.scatter(channels, strengths, alpha=0.6, color='green')
        ax3.set_title('Channel vs Signal Strength')
        ax3.set_xlabel('Channel')
        ax3.set_ylabel('Strength (dBm)')
        ax3.grid(True, alpha=0.3)
        
        # Security types
        security_types = {}
        for device in devices:
            sec = device.get('security', 'Unknown')
            security_types[sec] = security_types.get(sec, 0) + 1
        
        ax4.bar(security_types.keys(), security_types.values(), 
                color=['gold', 'lightblue', 'lightgreen', 'orange'])
        ax4.set_title('Security Types Distribution')
        ax4.set_ylabel('Count')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
