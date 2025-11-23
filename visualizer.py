import time
import json
from datetime import datetime
import os

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("[!] matplotlib not available - plotting disabled")

class SignalVisualizer:
    """Robust Signal Visualization without threading issues"""
    
    def __init__(self):
        self.scan_data = {
            'timestamps': [],
            'strengths': [],
            'channels': [],
            'ssids': []
        }
    
    def realtime_plot(self, detector, duration):
        """
        Collect data for plotting but don't show real-time plots
        to avoid threading issues
        """
        if not PLOTTING_AVAILABLE:
            return
        
        print("[+] Collecting data for visualization...")
        print("[!] Real-time plots disabled to avoid system conflicts")
        print("[!] Use 'analyze' command with -p flag to generate plots after scanning")
        
        # Just collect data without plotting
        start_time = time.time()
        
        while time.time() - start_time < duration and detector.is_scanning:
            if detector.results['devices']:
                latest = detector.results['devices'][-1]
                current_time = time.time() - start_time
                
                self.scan_data['timestamps'].append(current_time)
                self.scan_data['strengths'].append(latest['strength'])
                self.scan_data['channels'].append(latest['channel'])
                self.scan_data['ssids'].append(latest.get('ssid', 'Unknown'))
            
            time.sleep(1)
    
    def analyze_results(self, data, generate_plots=False):
        """Analyze and visualize scan results with static plots"""
        if not data.get('devices'):
            print("No data to analyze")
            return
        
        print("\n" + "="*60)
        print("📊 RF SIGNAL DETECTOR - COMPREHENSIVE ANALYSIS")
        print("="*60)
        
        devices = data['devices']
        
        # Basic statistics
        strengths = [d['strength'] for d in devices]
        channels = [d['channel'] for d in devices]
        ssids = [d.get('ssid', 'Hidden') for d in devices]
        
        print(f"📶 Total Networks Detected: {len(devices)}")
        print(f"📡 Channels with Activity: {sorted(set(channels))}")
        print(f"💪 Signal Strength Range: {min(strengths)} to {max(strengths)} dBm")
        print(f"📊 Average Signal Strength: {sum(strengths)/len(strengths):.1f} dBm")
        
        # Network analysis
        visible_networks = [ssid for ssid in ssids if ssid and ssid != 'Hidden']
        hidden_networks = len([ssid for ssid in ssids if not ssid or ssid == 'Hidden'])
        
        print(f"🔍 Visible Networks: {len(visible_networks)}")
        print(f"🕶️  Hidden Networks: {hidden_networks}")
        
        # Security analysis
        security = {}
        for device in devices:
            sec = device.get('security', 'Unknown')
            security[sec] = security.get(sec, 0) + 1
        
        print(f"\n🔒 Security Types:")
        for sec_type, count in security.items():
            print(f"   {sec_type}: {count} networks")
        
        # Top 5 strongest signals
        strongest = sorted(devices, key=lambda x: x['strength'], reverse=True)[:5]
        print(f"\n🏆 Top 5 Strongest Signals:")
        for i, device in enumerate(strongest, 1):
            ssid = device.get('ssid', 'Hidden Network')
            print(f"   {i}. {ssid} - {device['strength']} dBm (Channel {device['channel']})")
        
        # Generate static plots if requested
        if generate_plots and PLOTTING_AVAILABLE:
            self._generate_static_plots(data)
        elif generate_plots and not PLOTTING_AVAILABLE:
            print(f"\n[!] matplotlib not available for plotting")
            print(f"[!] Install with: pip install matplotlib")
    
    def _generate_static_plots(self, data):
        """Generate comprehensive static plots"""
        try:
            devices = data['devices']
            
            # Create analysis directory
            os.makedirs('analysis_plots', exist_ok=True)
            
            # Plot 1: Comprehensive overview
            fig = plt.figure(figsize=(15, 12))
            fig.suptitle('RF Signal Detector - Comprehensive Analysis\nSignal Research Lab', 
                        fontsize=16, fontweight='bold', y=0.98)
            
            # Data preparation
            channels = [d['channel'] for d in devices]
            strengths = [d['strength'] for d in devices]
            ssids = [d.get('ssid', 'Hidden') for d in devices]
            security_types = [d.get('security', 'Unknown') for d in devices]
            
            # Subplot 1: Channel distribution
            ax1 = plt.subplot(2, 2, 1)
            unique_channels = sorted(set(channels))
            channel_counts = [channels.count(ch) for ch in unique_channels]
            
            bars = ax1.bar(unique_channels, channel_counts, 
                          color=plt.cm.viridis(np.linspace(0, 1, len(unique_channels))),
                          alpha=0.7, edgecolor='black')
            
            ax1.set_title('Channel Distribution', fontweight='bold', pad=20)
            ax1.set_xlabel('WiFi Channel')
            ax1.set_ylabel('Number of Networks')
            ax1.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            # Subplot 2: Signal strength distribution
            ax2 = plt.subplot(2, 2, 2)
            strength_ranges = ['-90 to -80', '-80 to -70', '-70 to -60', '-60 to -50', '-50 to -40', '-40 to -30', '-30 to -20']
            strength_bins = [-90, -80, -70, -60, -50, -40, -30, -20]
            hist, bins, patches = ax2.hist(strengths, bins=strength_bins, 
                                          alpha=0.7, color='lightcoral', 
                                          edgecolor='black')
            
            ax2.set_title('Signal Strength Distribution', fontweight='bold', pad=20)
            ax2.set_xlabel('Signal Strength (dBm)')
            ax2.set_ylabel('Number of Networks')
            ax2.grid(True, alpha=0.3)
            
            # Subplot 3: Channel vs Strength
            ax3 = plt.subplot(2, 2, 3)
            scatter = ax3.scatter(channels, strengths, c=strengths, 
                                 cmap='RdYlGn_r', alpha=0.6, s=60)
            ax3.set_title('Channel vs Signal Strength', fontweight='bold', pad=20)
            ax3.set_xlabel('Channel')
            ax3.set_ylabel('Strength (dBm)')
            ax3.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax3, label='Signal Strength (dBm)')
            
            # Subplot 4: Security types
            ax4 = plt.subplot(2, 2, 4)
            security_count = {}
            for sec in security_types:
                security_count[sec] = security_count.get(sec, 0) + 1
            
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            wedges, texts, autotexts = ax4.pie(security_count.values(), 
                                              labels=security_count.keys(),
                                              autopct='%1.1f%%',
                                              colors=colors[:len(security_count)],
                                              startangle=90)
            
            ax4.set_title('Security Types Distribution', fontweight='bold', pad=20)
            
            # Make the plot better
            plt.tight_layout()
            plt.subplots_adjust(top=0.93)
            
            # Save the plot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_file = f"analysis_plots/rf_analysis_{timestamp}.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f"\n💾 Analysis plot saved: {plot_file}")
            
            # Show the plot
            plt.show()
            
            # Generate additional detailed plot
            self._generate_detailed_plot(data, timestamp)
            
        except Exception as e:
            print(f"[!] Plot generation error: {e}")
    
    def _generate_detailed_plot(self, data, timestamp):
        """Generate additional detailed analysis plot"""
        try:
            devices = data['devices']
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            fig.suptitle('RF Signal Detector - Network Details\nSignal Research Lab', 
                        fontsize=14, fontweight='bold')
            
            # Plot 1: Networks by channel with strength heatmap
            channels = [d['channel'] for d in devices]
            strengths = [d['strength'] for d in devices]
            ssids = [d.get('ssid', 'Hidden') for d in devices]
            
            # Create channel-strength matrix
            unique_channels = sorted(set(channels))
            strength_matrix = []
            
            for channel in unique_channels:
                channel_strengths = [s for c, s in zip(channels, strengths) if c == channel]
                avg_strength = sum(channel_strengths) / len(channel_strengths) if channel_strengths else -90
                strength_matrix.append(avg_strength)
            
            im = ax1.imshow([strength_matrix], cmap='RdYlGn_r', aspect='auto', 
                           extent=[min(unique_channels)-0.5, max(unique_channels)+0.5, 0, 1])
            ax1.set_xlabel('WiFi Channel')
            ax1.set_title('Channel Signal Strength Heatmap', fontweight='bold')
            ax1.set_yticks([])
            plt.colorbar(im, ax=ax1, label='Average Signal Strength (dBm)')
            
            # Plot 2: Network type distribution
            visible_count = len([ssid for ssid in ssids if ssid and ssid != 'Hidden'])
            hidden_count = len([ssid for ssid in ssids if not ssid or ssid == 'Hidden'])
            
            labels = ['Visible Networks', 'Hidden Networks']
            sizes = [visible_count, hidden_count]
            colors = ['#4CAF50', '#FF9800']
            
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   startangle=90, textprops={'fontweight': 'bold'})
            ax2.set_title('Network Visibility Distribution', fontweight='bold')
            
            plt.tight_layout()
            plt.subplots_adjust(top=0.85)
            
            # Save detailed plot
            detail_file = f"analysis_plots/rf_details_{timestamp}.png"
            plt.savefig(detail_file, dpi=300, bbox_inches='tight')
            print(f"💾 Detailed plot saved: {detail_file}")
            
            plt.show()
            
        except Exception as e:
            print(f"[!] Detailed plot error: {e}")