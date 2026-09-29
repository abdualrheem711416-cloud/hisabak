with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# إزالة كاش الـ Service worker لفرض التحديث الفوري
html = html.replace('hisabak-v3', 'hisabak-v4').replace('hisabak-v2', 'hisabak-v4')

override_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  // اعتراض أي عنصر يحتوي على كلمة الموردين وتحويله لفتح النافذة
  document.querySelectorAll('*').forEach(el => {
    if (el.children.length === 0 && el.innerText && el.innerText.includes('الموردين')) {
      const card = el.closest('.card') || el.parentElement;
      if (card) {
        card.onclick = (e) => {
          e.preventDefault();
          e.stopPropagation();
          if (typeof openSuppliers === 'function') {
            openSuppliers();
          } else {
            alert('جاري تجهيز قسم الموردين');
          }
        };
      }
    }
  });
});

// تعطيل نافذة التنبيه المزعجة في حال استدعائها
const _oldAlert = window.alert;
window.alert = function(msg) {
  if (typeof msg === 'string' && msg.includes('الموردين')) {
    if (typeof openSuppliers === 'function') {
      openSuppliers();
      return;
    }
  }
  _oldAlert(msg);
};
</script>
"""

if 'fix-suppliers-override' not in html:
    html = html.replace('</body>', '<div id="fix-suppliers-override"></div>\n' + override_script + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("FIX_APPLIED")
