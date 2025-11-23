import time
import random
import json
from datetime import datetime
import threading
try:
    import numpy as np
except ImportError:
    np = None

class RFDetector:
    """Advanced RF Signal Detection Engine"""
    
    # WiFi channels for different bands
    CHANNELS_2G = list(range(1, 14))
    CHANNELS_5G = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
    
    def __init__(self):
        self.is_scanning = False
        self.results = {
            'devices': [],
            'scan_info': {},
            'summary': {}
        }
    
    def scan_band(self, band='2.4G', duration=60, visualizer=None):
        """Scan specified frequency band"""
        channels = self.CHANNELS_2G if band == '2.4G' else self.CHANNELS_5G
        if band == 'all':
            channels = self.CHANNELS_2G + self.CHANNELS_5G
        
        self.results['scan_info'] = {
            'band': band,
            'channels': channels,
            'start_time': datetime.now().isoformat(),
            'duration': duration
        }
        
        self.is_scanning = True
        start_time = time.time()
        
        # Start visualization in separate thread if requested
        if visualizer:
            viz_thread = threading.Thread(
                target=visualizer.realtime_plot,
                args=(self, duration)
            )
            viz_thread.daemon = True
            viz_thread.start()
        
        print("CHAN\tSTRENGTH\tSSID")
        print("-" * 40)
        
        while time.time() - start_time < duration and self.is_scanning:
            # Simulate scanning different channels
            for channel in random.sample(channels, min(3, len(channels))):
                if not self.is_scanning:
                    break
                    
                device = self._simulate_device(channel, band)
                self.results['devices'].append(device)
                
                # Print device info
                ssid = device['ssid'] or 'Hidden Network'
                print(f"{channel:2d}\t{device['strength']:3d} dBm\t{ssid}")
                
                time.sleep(0.5)
            
            time.sleep(2)
        
        self._generate_summary()
        return self.results
    
    def monitor_channel(self, channel, duration=300):
        """Monitor specific channel for activity"""
        print(f"Monitoring channel {channel}...")
        print("TIME\t\tSTRENGTH\tPACKETS")
        print("-" * 40)
        
        activity_data = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Simulate network activity
            strength = random.randint(-90, -20)
            packets = random.randint(0, 1000)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{timestamp}\t{strength:3d} dBm\t{packets:4d}")
            
            activity_data.append({
                'timestamp': timestamp,
                'strength': strength,
                'packets': packets
            })
            
            time.sleep(1)
        
        return {
            'channel': channel,
            'duration': duration,
            'activity': activity_data
        }
    
    def _simulate_device(self, channel, band):
        """Simulate detecting a wireless device"""
        strengths = ['Very Strong', 'Strong', 'Good', 'Fair', 'Weak']
        ssids = [
            'Home_Network', 'TP-Link_ABCD', 'AndroidAP', 'iPhone',
            'XfinityWiFi', 'ATTWiFi', 'NETGEAR', 'Linksys',
            'Hidden_Network', 'Public_WiFi', 'Guest', None
        ]
        
        return {
            'channel': channel,
            'strength': random.randint(-90, -20),
            'ssid': random.choice(ssids),
            'band': band,
            'security': random.choice(['WPA2', 'WPA3', 'WEP', 'Open']),
            'first_seen': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat()
        }
    
    def _generate_summary(self):
        """Generate scan summary"""
        if not self.results['devices']:
            self.results['summary'] = {
                'total_signals': 0,
                'avg_strength': 0,
                'max_strength': 0,
                'channels': set(),
                'duration': 0
            }
            return
        
        strengths = [d['strength'] for d in self.results['devices']]
        channels = set(d['channel'] for d in self.results['devices'])
        
        self.results['summary'] = {
            'total_signals': len(self.results['devices']),
            'avg_strength': int(sum(strengths) / len(strengths)),
            'max_strength': max(strengths),
            'min_strength': min(strengths),
            'channels': list(channels),
            'duration': self.results['scan_info']['duration']
        }
    
    def stop_scan(self):
        """Stop ongoing scan"""
        self.is_scanning = False
