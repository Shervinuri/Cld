// Cloudflare Worker for SHΞN™ V2Ray Aggregator
// This runs the aggregation logic in Cloudflare's edge

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle CORS for V2Ray clients
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      // Fetch from your source
      const sourceUrl = 'https://raw.githubusercontent.com/Shervinuri/SUBscripSHEN/refs/heads/main/SUBscripSHEN.json';
      const sourceResponse = await fetch(sourceUrl);
      const sourceText = await sourceResponse.text();
      
      // Extract URLs (simplified version)
      const urls = sourceText.match(/https?:\/\/[^\s\n\\]+/g) || [];
      const validUrls = urls.filter(url => 
        url.includes('github') && 
        (url.includes('vless') || url.includes('v2ray'))
      ).slice(0, 10); // Limit for performance
      
      let allConfigs = [];
      
      // Fetch configs from multiple sources
      const promises = validUrls.map(async (url) => {
        try {
          const response = await fetch(url, { 
            headers: { 'User-Agent': 'Mozilla/5.0' },
            cf: { cacheTtl: 3600 } // Cache for 1 hour
          });
          
          if (response.ok) {
            let content = await response.text();
            
            // Try base64 decode
            try {
              content = atob(content);
            } catch (e) {
              // Already decoded
            }
            
            // Extract VLESS configs
            const vlessConfigs = content.match(/vless:\/\/[^\s\n]+/g) || [];
            
            // Add SHΞN™ branding
            return vlessConfigs.map(config => {
              const baseConfig = config.split('#')[0];
              return `${baseConfig}#SHΞN™ 🏳️`;
            });
          }
        } catch (e) {
          console.error('Failed to fetch:', url, e);
        }
        return [];
      });
      
      const results = await Promise.all(promises);
      allConfigs = results.flat();
      
      // Remove duplicates
      const uniqueConfigs = [...new Set(allConfigs)];
      
      // Generate subscription content
      const profileTitle = btoa('SHΞN™ Subscription');
      const metadata = `#profile-title: base64:${profileTitle}
#profile-update-interval:1
#subscription-userinfo: upload=0; download=0; total=10737418240; expire=1735689600
#hiddify-config: https://raw.githubusercontent.com/Shervinuri/SUBscripSHEN/refs/heads/main/SUBscripSHEN.json

`;
      
      const configContent = uniqueConfigs.join('\n');
      
      const redirectScript = `
<script>
setTimeout(function() {
    if (window.location.href.indexOf('hiddify://') === -1) {
        window.location.href = 'hiddify://import/' + window.location.href + '#SHEN';
    }
}, 3000);

document.addEventListener('DOMContentLoaded', function() {
    if (navigator.userAgent.indexOf('v2ray') === -1 && navigator.userAgent.indexOf('clash') === -1) {
        document.body.innerHTML = \`
            <div style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh;">
                <h1 style="font-size: 3em; margin-bottom: 20px;">SHΞN™ V2Ray Subscription</h1>
                <div style="font-size: 1.5em; margin-bottom: 30px;">
                    <div style="animation: pulse 2s infinite;">🚀 Redirecting to Hiddify...</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px;">
                    <h3>📱 How to use:</h3>
                    <p>1. Copy this URL: <code style="background: rgba(0,0,0,0.3); padding: 5px; border-radius: 5px;">\${window.location.href}</code></p>
                    <p>2. Add to your V2Ray client as subscription link</p>
                    <p>3. Or wait for automatic redirect to Hiddify</p>
                </div>
                <div style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                    <p>🔄 Auto-updated every hour</p>
                    <p>🌍 Servers from multiple countries</p>
                    <p>⚡ High-speed connections</p>
                    <p>📊 Total configs: ${uniqueConfigs.length}</p>
                    <p>⏰ Last updated: ${new Date().toISOString()}</p>
                </div>
            </div>
            <style>
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.5; }
                    100% { opacity: 1; }
                }
                code {
                    word-break: break-all;
                }
            </style>
        \`;
    }
});
</script>`;
      
      const finalContent = metadata + configContent + redirectScript;
      
      return new Response(finalContent, {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
          ...corsHeaders
        }
      });
      
    } catch (error) {
      console.error('Worker error:', error);
      return new Response('Error generating subscription', { 
        status: 500,
        headers: corsHeaders 
      });
    }
  }
};