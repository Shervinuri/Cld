# 🚀 راهنمای Deploy روی Cloudflare

## 🎯 **دو روش Deploy:**

### 🔥 **روش 1: Cloudflare Workers (پیشنهادی)**
**مزایا:** Auto-update، سرعت بالا، رایگان تا 100K request

#### مراحل:
1. **وارد Cloudflare Dashboard شو:**
   - برو به [dash.cloudflare.com](https://dash.cloudflare.com)
   - روی **Workers & Pages** کلیک کن

2. **ایجاد Worker جدید:**
   - **Create** → **Create Worker**
   - اسم بذار: `shen-v2ray-aggregator`

3. **کد Worker رو کپی کن:**
   - فایل `cloudflare-worker.js` رو باز کن
   - همه کد رو کپی کن و جایگزین کن

4. **Deploy کن:**
   - **Save and Deploy** رو بزن
   - URL دریافت می‌کنی: `https://shen-v2ray-aggregator.YOUR-SUBDOMAIN.workers.dev`

5. **Custom Domain (اختیاری):**
   - **Settings** → **Triggers** → **Add Custom Domain**
   - `shervin.kortix.cloud` رو اضافه کن

---

### 📄 **روش 2: Cloudflare Pages (ساده‌تر)**
**محدودیت:** فقط فایل static، بدون auto-update

#### مراحل:
1. **وارد Cloudflare Dashboard شو:**
   - **Workers & Pages** → **Create** → **Pages**

2. **آپلود فایل:**
   - **Upload assets** رو انتخاب کن
   - فقط فایل `index.html` رو آپلود کن

3. **تنظیمات:**
   - Project name: `shen-subscription`
   - **Deploy site**

4. **Custom Domain:**
   - **Custom domains** → **Set up a custom domain**
   - `shervin.kortix.cloud` رو اضافه کن

---

## ⚡ **مقایسه روش‌ها:**

| ویژگی | Workers | Pages |
|--------|---------|-------|
| Auto-update | ✅ هر ساعت | ❌ دستی |
| سرعت | ⚡ خیلی سریع | 🚀 سریع |
| کانفیگ‌ها | 🔄 Live fetch | 📁 Static |
| پیچیدگی | 🔧 متوسط | 🎯 ساده |
| هزینه | 💰 رایگان | 💰 رایگان |

---

## 🛠️ **تنظیمات پیشرفته Workers:**

### 1️⃣ **Environment Variables:**
```javascript
// در Worker settings → Variables
SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/SUBscripSHEN/refs/heads/main/SUBscripSHEN.json"
BRAND_NAME = "SHΞN™"
UPDATE_INTERVAL = "3600" // 1 hour
```

### 2️⃣ **Cron Triggers (برای cache warming):**
```javascript
// در wrangler.toml
[triggers]
crons = ["0 * * * *"] // هر ساعت

export default {
  async scheduled(event, env, ctx) {
    // Warm up cache
    await fetch('https://your-worker.workers.dev');
  }
}
```

### 3️⃣ **KV Storage (برای cache):**
```javascript
// اضافه کردن KV namespace
const cache = await env.SHEN_CACHE.get('configs');
if (!cache || Date.now() - cache.timestamp > 3600000) {
  // Fetch new data
  const newData = await fetchConfigs();
  await env.SHEN_CACHE.put('configs', JSON.stringify({
    data: newData,
    timestamp: Date.now()
  }));
}
```

---

## 🔧 **تست و عیب‌یابی:**

### تست Worker:
```bash
# تست در مرورگر
https://your-worker.workers.dev

# تست با curl
curl -H "User-Agent: v2ray" https://your-worker.workers.dev
```

### مشاهده Logs:
```javascript
// در Worker code
console.log('Fetched configs:', configs.length);

// در Cloudflare Dashboard
// Workers → your-worker → Logs
```

### Performance Monitoring:
- **Analytics** tab در Dashboard
- **Real-time logs** برای debugging
- **Metrics** برای performance

---

## 🌐 **تنظیم Custom Domain:**

### 1️⃣ **اگر Domain در Cloudflare هست:**
- **DNS** → **Add record**
- Type: `CNAME`
- Name: `shervin` یا `@`
- Target: `your-worker.workers.dev`

### 2️⃣ **اگر Domain خارج از Cloudflare:**
- **Workers** → **Triggers** → **Add Custom Domain**
- Domain رو verify کن
- DNS record رو اضافه کن

---

## 📊 **بهینه‌سازی Performance:**

### 1️⃣ **Cache Headers:**
```javascript
return new Response(content, {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    'CDN-Cache-Control': 'max-age=7200'
  }
});
```

### 2️⃣ **Compression:**
```javascript
// Cloudflare automatically compresses
// Just ensure proper content-type
'Content-Type': 'text/html; charset=utf-8'
```

### 3️⃣ **Edge Caching:**
```javascript
const response = await fetch(url, {
  cf: {
    cacheTtl: 3600, // Cache at edge for 1 hour
    cacheEverything: true
  }
});
```

---

## 🔒 **امنیت:**

### Rate Limiting:
```javascript
// در Worker
const clientIP = request.headers.get('CF-Connecting-IP');
const rateLimitKey = `rate_limit:${clientIP}`;
const current = await env.KV.get(rateLimitKey);

if (current && parseInt(current) > 100) {
  return new Response('Rate limit exceeded', { status: 429 });
}
```

### CORS Security:
```javascript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Max-Age': '86400'
};
```

---

## 🎯 **نتیجه:**

### **برای شروع سریع:** Pages
### **برای قابلیت کامل:** Workers

**🚀 پیشنهاد من: Workers استفاده کن چون:**
- ✅ Auto-update داره
- ✅ سریع‌تره
- ✅ کانفیگ‌های بیشتری جمع می‌کنه
- ✅ مانیتورینگ بهتری داره

**📞 اگر مشکلی داشتی، بگو تا کمکت کنم!**