#!/usr/bin/env python3
"""
SHΞN™ V2Ray Subscription Aggregator - Fast Version
Optimized for speed and reliability
"""

import requests
import base64
import re
import time
import socket
from urllib.parse import unquote
from typing import List, Dict, Set
import logging
import concurrent.futures
from threading import Lock

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FastGeoIP:
    """Fast GeoIP resolver with caching and fallback"""
    
    COUNTRY_FLAGS = {
        'US': '🇺🇸', 'GB': '🇬🇧', 'DE': '🇩🇪', 'FR': '🇫🇷', 'JP': '🇯🇵',
        'KR': '🇰🇷', 'CN': '🇨🇳', 'HK': '🇭🇰', 'TW': '🇹🇼', 'SG': '🇸🇬',
        'CA': '🇨🇦', 'AU': '🇦🇺', 'NL': '🇳🇱', 'RU': '🇷🇺', 'IN': '🇮🇳',
        'BR': '🇧🇷', 'IT': '🇮🇹', 'ES': '🇪🇸', 'SE': '🇸🇪', 'NO': '🇳🇴',
        'FI': '🇫🇮', 'DK': '🇩🇰', 'CH': '🇨🇭', 'AT': '🇦🇹', 'BE': '🇧🇪',
        'IE': '🇮🇪', 'PL': '🇵🇱', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'GR': '🇬🇷',
        'PT': '🇵🇹', 'TR': '🇹🇷', 'IL': '🇮🇱', 'AE': '🇦🇪', 'SA': '🇸🇦',
        'IR': '🇮🇷', 'LV': '🇱🇻', 'LT': '🇱🇹', 'EE': '🇪🇪', 'UA': '🇺🇦'
    }
    
    # Common IP ranges for quick lookup
    IP_RANGES = {
        '1.1.1.': '🇺🇸',      # Cloudflare
        '8.8.8.': '🇺🇸',      # Google
        '104.': '🇺🇸',        # US ranges
        '172.': '🇺🇸',        # US ranges
        '185.': '🇪🇺',        # EU ranges
        '46.': '🇪🇺',         # EU ranges
        '78.': '🇪🇺',         # EU ranges
        '91.': '🇪🇺',         # EU ranges
    }
    
    def __init__(self):
        self.cache = {}
        self.lock = Lock()
        
    def get_country_flag(self, ip: str) -> str:
        """Get country flag emoji for IP address with fast lookup"""
        with self.lock:
            if ip in self.cache:
                return self.cache[ip]
        
        # Quick range-based lookup
        for prefix, flag in self.IP_RANGES.items():
            if ip.startswith(prefix):
                with self.lock:
                    self.cache[ip] = flag
                return flag
        
        # Default flag for unknown IPs
        flag = '🏳️'
        with self.lock:
            self.cache[ip] = flag
        return flag

class FastV2RayProcessor:
    """Fast V2Ray config processor"""
    
    def __init__(self):
        self.geoip = FastGeoIP()
        self.processed_configs = set()
        self.lock = Lock()
        
    def extract_ip_from_vless(self, vless_url: str) -> str:
        """Extract IP address from VLESS URL - fast version"""
        try:
            if not vless_url.startswith('vless://'):
                return None
                
            # Quick regex extraction
            match = re.search(r'vless://[^@]+@([^:]+):', vless_url)
            if not match:
                return None
                
            host = match.group(1)
            
            # Check if it's already an IP
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', host):
                return host
            
            # Skip domain resolution for speed - just use domain-based flags
            if '.ir' in host:
                return '🇮🇷'
            elif '.de' in host or 'germany' in host.lower():
                return '🇩🇪'
            elif '.fr' in host or 'france' in host.lower():
                return '🇫🇷'
            elif '.nl' in host or 'netherlands' in host.lower():
                return '🇳🇱'
            elif '.us' in host or 'usa' in host.lower():
                return '🇺🇸'
            
            return None
                    
        except Exception:
            return None
    
    def create_remark(self, vless_url: str) -> str:
        """Create new remark with SHΞN™ branding"""
        ip_or_flag = self.extract_ip_from_vless(vless_url)
        
        if ip_or_flag and ip_or_flag.startswith('�'):
            # Already a flag
            return f"SHΞN™ {ip_or_flag}"
        elif ip_or_flag:
            # It's an IP
            flag = self.geoip.get_country_flag(ip_or_flag)
            return f"SHΞN™ {flag}"
        else:
            return "SHΞN™ 🏳️"
    
    def update_vless_remark(self, vless_url: str) -> str:
        """Update VLESS URL with new remark"""
        try:
            base_url = vless_url.split('#')[0] if '#' in vless_url else vless_url
            new_remark = self.create_remark(vless_url)
            return f"{base_url}#{new_remark}"
        except Exception:
            return vless_url
    
    def process_subscription_content(self, content: str) -> List[str]:
        """Process subscription content - fast version"""
        configs = []
        
        try:
            # Try base64 decode
            try:
                decoded_content = base64.b64decode(content).decode('utf-8', errors='ignore')
                content = decoded_content
            except:
                pass
            
            # Find all VLESS configs using regex
            vless_pattern = r'vless://[^\s\n]+'
            vless_configs = re.findall(vless_pattern, content)
            
            for config in vless_configs:
                config = config.strip()
                if config:
                    # Check for duplicates
                    config_hash = hash(config.split('#')[0])
                    with self.lock:
                        if config_hash not in self.processed_configs:
                            updated_config = self.update_vless_remark(config)
                            configs.append(updated_config)
                            self.processed_configs.add(config_hash)
                            
        except Exception as e:
            logger.warning(f"Failed to process content: {e}")
            
        return configs
    
    def fetch_subscription(self, url: str) -> List[str]:
        """Fetch and process a single subscription URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return self.process_subscription_content(response.text)
                
        except Exception as e:
            logger.warning(f"Error fetching {url[:50]}...: {e}")
            
        return []

class FastAggregator:
    """Fast subscription aggregator"""
    
    def __init__(self, source_url: str):
        self.source_url = source_url
        self.processor = FastV2RayProcessor()
        
    def get_source_urls(self) -> List[str]:
        """Get subscription URLs from source"""
        try:
            response = requests.get(self.source_url, timeout=15)
            if response.status_code == 200:
                content = response.text
                
                # Extract URLs
                url_pattern = r'https?://[^\s\n\\]+'
                urls = re.findall(url_pattern, content)
                
                # Filter valid URLs
                valid_urls = []
                for url in urls:
                    url = url.rstrip('\\n').rstrip('\\')
                    if any(domain in url for domain in ['github', 'raw.githubusercontent', 'gitlab']):
                        if 'vless' in url.lower() or 'v2ray' in url.lower() or 'sub' in url.lower():
                            valid_urls.append(url)
                
                logger.info(f"Found {len(valid_urls)} subscription URLs")
                return valid_urls[:20]  # Limit to 20 for speed
                
        except Exception as e:
            logger.error(f"Failed to get source URLs: {e}")
            
        return []
    
    def fetch_configs_parallel(self, urls: List[str]) -> List[str]:
        """Fetch configs from multiple URLs in parallel"""
        all_configs = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.processor.fetch_subscription, url): url for url in urls}
            
            for future in concurrent.futures.as_completed(future_to_url, timeout=60):
                url = future_to_url[future]
                try:
                    configs = future.result()
                    all_configs.extend(configs)
                    logger.info(f"Fetched {len(configs)} configs from {url[:50]}...")
                    
                    # Limit total configs
                    if len(all_configs) > 150:
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch {url[:50]}...: {e}")
        
        return all_configs
    
    def generate_subscription_file(self, configs: List[str]) -> str:
        """Generate final subscription file"""
        
        # Metadata
        profile_title = base64.b64encode("SHΞN™ Subscription".encode()).decode()
        
        metadata = f"""#profile-title: base64:{profile_title}
#profile-update-interval:1
#subscription-userinfo: upload=0; download=0; total=10737418240; expire=1735689600
#hiddify-config: https://raw.githubusercontent.com/Shervinuri/SUBscripSHEN/refs/heads/main/SUBscripSHEN.json

"""
        
        # Configs
        config_content = '\n'.join(configs)
        
        # Redirect script
        redirect_script = f"""
<script>
setTimeout(function() {{
    if (window.location.href.indexOf('hiddify://') === -1) {{
        window.location.href = 'hiddify://import/' + window.location.href + '#SHEN';
    }}
}}, 3000);

document.addEventListener('DOMContentLoaded', function() {{
    if (navigator.userAgent.indexOf('v2ray') === -1 && navigator.userAgent.indexOf('clash') === -1) {{
        document.body.innerHTML = `
            <div style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh;">
                <h1 style="font-size: 3em; margin-bottom: 20px;">SHΞN™ V2Ray Subscription</h1>
                <div style="font-size: 1.5em; margin-bottom: 30px;">
                    <div style="animation: pulse 2s infinite;">🚀 Redirecting to Hiddify...</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px;">
                    <h3>📱 How to use:</h3>
                    <p>1. Copy this URL: <code style="background: rgba(0,0,0,0.3); padding: 5px; border-radius: 5px;">shervin.kortix.cloud</code></p>
                    <p>2. Add to your V2Ray client as subscription link</p>
                    <p>3. Or wait for automatic redirect to Hiddify</p>
                </div>
                <div style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                    <p>🔄 Auto-updated every hour</p>
                    <p>🌍 Servers from multiple countries</p>
                    <p>⚡ High-speed connections</p>
                    <p>📊 Total configs: {len(configs)}</p>
                    <p>⏰ Last updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
            </div>
            <style>
                @keyframes pulse {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0.5; }}
                    100% {{ opacity: 1; }}
                }}
                code {{
                    word-break: break-all;
                }}
            </style>
        `;
    }}
}});
</script>"""
        
        return metadata + config_content + redirect_script

def main():
    """Main function"""
    logger.info("Starting SHΞN™ Fast V2Ray Aggregator")
    
    source_url = "https://raw.githubusercontent.com/Shervinuri/SUBscripSHEN/refs/heads/main/SUBscripSHEN.json"
    
    aggregator = FastAggregator(source_url)
    
    # Get URLs
    urls = aggregator.get_source_urls()
    
    if urls:
        # Fetch configs in parallel
        configs = aggregator.fetch_configs_parallel(urls)
        
        if configs:
            # Generate subscription file
            subscription_content = aggregator.generate_subscription_file(configs)
            
            # Save to file
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(subscription_content)
                
            logger.info(f"✅ Subscription generated with {len(configs)} configs")
            logger.info("📁 File saved as index.html")
            logger.info("🌐 Ready for deployment!")
        else:
            logger.error("❌ No configs found!")
    else:
        logger.error("❌ No source URLs found!")

if __name__ == "__main__":
    main()