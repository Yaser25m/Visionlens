@echo off
echo ========================================
echo    فتح جدار الحماية للمنفذ 8000
echo ========================================
echo.

echo جاري فتح المنفذ 8000 في جدار الحماية...
netsh advfirewall firewall add rule name="Django Server Port 8000" dir=in action=allow protocol=TCP localport=8000

echo.
echo جاري فتح المنفذ 8000 للاتصالات الخارجة...
netsh advfirewall firewall add rule name="Django Server Port 8000 Out" dir=out action=allow protocol=TCP localport=8000

echo.
echo ========================================
echo تم فتح المنفذ 8000 بنجاح!
echo الآن يمكن للأجهزة الأخرى الوصول للخادم
echo ========================================
echo.

pause
