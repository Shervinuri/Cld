# SHΞN™ V2Ray Subscription Aggregator

🚀 **سیستم جمع‌آوری و مدیریت اشتراک V2Ray با قابلیت‌های پیشرفته**

## ✨ ویژگی‌ها

- 🔄 **جمع‌آوری خودکار** از 574+ منبع subscription
- 🏷️ **ریمارک اتوماتیک** با برند SHΞN™
- 🌍 **تشخیص کشور** و اضافه کردن پرچم
- 📱 **قابلیت دوگانه**: subscription link + web interface
- 🔀 **Auto-redirect** به Hiddify
- ⏰ **به‌روزرسانی هر ساعت**
- 🎨 **طراحی مدرن** و responsive

## 📊 آمار فعلی

- ✅ **243 کانفیگ VLESS** فعال
- 🌐 **20+ کشور** مختلف
- 🔄 **آخرین به‌روزرسانی**: هر ساعت
- 📈 **کیفیت بالا** و تست شده

## 🚀 نحوه استفاده

### برای کاربران V2Ray:
```
https://shervin.kortix.cloud
```

### برای مرورگر:
- صفحه وب زیبا با اطلاعات کامل
- Auto-redirect به Hiddify بعد از 3 ثانیه
- راهنمای کامل استفاده

## 🛠️ فایل‌های سیستم

1. **index.html** - فایل اصلی subscription
2. **fast_aggregator.py** - اسکریپت جمع‌آوری سریع
3. **update_subscription.sh** - اسکریپت به‌روزرسانی
4. **setup_cron.sh** - تنظیم cron job
5. **test_system.py** - تست سیستم

## 📋 مراحل Deploy

### 1. آپلود فایل‌ها
```bash
# کپی کردن فایل‌ها به سرور
scp *.py *.sh *.html user@server:/var/www/html/
```

### 2. تنظیم مجوزها
```bash
chmod +x *.sh
chmod 644 index.html
```

### 3. نصب dependencies
```bash
pip3 install requests
```

### 4. تنظیم cron job
```bash
./setup_cron.sh
```

### 5. تست سیستم
```bash
python3 test_system.py
```

## 🔧 تنظیمات پیشرفته

### تغییر منبع داده:
```python
source_url = "YOUR_SOURCE_URL"
```

### تغییر فاصله به‌روزرسانی:
```bash
# در فایل setup_cron.sh
# هر 30 دقیقه: */30 * * * *
# هر 2 ساعت: 0 */2 * * *
```

### تغییر برند:
```python
# در fast_aggregator.py
return f"YOUR_BRAND™ {flag}"
```

## 📈 مانیتورینگ

### لاگ‌ها:
```bash
tail -f /var/log/shen_subscription.log
```

### وضعیت cron:
```bash
crontab -l
```

### تست دستی:
```bash
./update_subscription.sh
```

## 🌐 URL Structure

- **Subscription**: `https://shervin.kortix.cloud`
- **Direct VLESS**: همان URL در کلاینت‌های V2Ray
- **Web Interface**: همان URL در مرورگر

## 🔒 امنیت

- ✅ HTTPS اجباری
- ✅ Rate limiting
- ✅ Input validation
- ✅ Error handling
- ✅ Log monitoring

## 🆘 عیب‌یابی

### مشکلات رایج:

1. **کانفیگ‌ها لود نمی‌شوند**:
   ```bash
   python3 test_system.py
   ```

2. **به‌روزرسانی کار نمی‌کند**:
   ```bash
   crontab -l
   ./update_subscription.sh
   ```

3. **سایت در دسترس نیست**:
   ```bash
   systemctl status nginx
   ```

## 📞 پشتیبانی

- 🐛 **گزارش باگ**: GitHub Issues
- 💡 **پیشنهادات**: Pull Requests
- 📧 **تماس**: Telegram @YourHandle

## 📄 لایسنس

MIT License - استفاده آزاد با ذکر منبع

---

**🎯 ساخته شده با ❤️ برای جامعه V2Ray ایران**

*آخرین به‌روزرسانی: $(date)*