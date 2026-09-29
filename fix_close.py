with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# تكبير زر الإغلاق العلوي ليكون دائرياً وواضحاً وسهل اللمس
new_close = '''<button onclick="closeSuppliersModal()" style="background:#fee2e2; color:#dc2626; border:none; font-size:22px; font-weight:bold; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; touch-action:manipulation;">&#x2715;</button>'''

import re
html = re.sub(r'<button onclick="closeSuppliersModal\(\)"[^>]*>.*?</button>', new_close, html)

# تمكين إغلاق النافذة بالنقر على الخلفية المعتمة
html = html.replace('id="suppliers-modal"', 'id="suppliers-modal" onclick="if(event.target===this) closeSuppliersModal()"')

# إضافة زر إغلاق سفلي عريض وواضح
bottom_btn = '''
    <div style="margin-top:14px; border-top:1px solid #eee; padding-top:10px;">
      <button onclick="closeSuppliersModal()" style="width:100%; background:#4b5563; color:#fff; border:none; padding:11px; border-radius:8px; font-weight:bold; font-size:1rem; cursor:pointer; font-family:'Cairo',sans-serif;">إغلاق النافذة &#x2715;</button>
    </div>
  </div>
</div>'''

if 'إغلاق النافذة' not in html:
    html = html.replace('</div>\n  </div>\n</div>', bottom_btn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("CLOSE_FIXED")
