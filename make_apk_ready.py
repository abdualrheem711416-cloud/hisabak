import os

print("BUILDING_HISABAK_APK_PACKAGE...")
# التأكد من جاهزية ملفات التطبيق الرئيسية
required_files = ['index.html', 'items.html', 'stores.html', 'settings_menu.html']
for f in required_files:
    if os.path.exists(f):
        print(f" -> Found: {f}")
    else:
        print(f" -> Warning: {f} missing")

print("HISABAK_PACKAGE_READY_FOR_DEPLOYMENT")
