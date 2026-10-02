with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. نافذة الإعدادات العامة المتكاملة
settings_modal = """
<!-- General Settings Modal -->
<div id="general-settings-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:12500; align-items:center; justify-content:center; direction:rtl; font-family:'Cairo', sans-serif;" onclick="if(event.target===this) closeGeneralSettings()">
  <div style="background:#fff; width:92%; max-width:480px; border-radius:14px; padding:18px; box-shadow:0 8px 25px rgba(0,0,0,0.3); max-height:90vh; display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #0b5cab; padding-bottom:8px;">
      <h3 style="margin:0; color:#0b5cab; font-size:1.15rem; display:flex; align-items:center; gap:6px;">⚙️ الإعدادات العامة</h3>
      <button onclick="closeGeneralSettings()" style="background:#fee2e2; color:#dc2626; border:none; font-size:20px; font-weight:bold; width:34px; height:34px; border-radius:50%; cursor:pointer;">&#x2715;</button>
    </div>

    <div style="flex:1; overflow-y:auto; margin-top:12px; display:flex; flex-direction:column; gap:12px;">
      <!-- قسم دليل واستيراد الأصناف -->
      <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:10px; padding:12px;">
        <h4 style="margin:0 0 8px 0; color:#1e293b; font-size:0.95rem; display:flex; align-items:center; gap:6px;">📦 دليل وإدارة الأصناف (Excel)</h4>
        <p style="margin:0 0 10px 0; font-size:12px; color:#64748b;">استيراد قائمة المواد والأسعار من ملف إكسل لتكون متاحة لجميع الفواتير والموردين.</p>
        
        <div style="display:flex; gap:8px; margin-bottom:10px;">
          <input type="file" id="global-excel-file" accept=".xlsx, .xls, .csv" style="display:none;" onchange="handleGlobalExcelUpload(event)">
          <button onclick="document.getElementById('global-excel-file').click()" style="flex:1; background:#16a34a; color:#fff; border:none; padding:9px 12px; border-radius:6px; font-weight:bold; font-size:0.85rem; cursor:pointer; font-family:'Cairo';">📥 استيراد ملف إكسل</button>
          <button onclick="clearAllItemsConfirm()" style="background:#ef4444; color:#fff; border:none; padding:9px 12px; border-radius:6px; font-size:0.85rem; font-weight:bold; cursor:pointer; font-family:'Cairo';">مسح الكل</button>
        </div>

        <!-- إضافة صنف سريع -->
        <div style="display:flex; gap:6px;">
          <input type="text" id="g-item-name" placeholder="اسم الصنف" style="flex:2; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
          <input type="number" id="g-item-price" placeholder="السعر" style="flex:1; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
          <button onclick="addGlobalItem()" style="background:#0b5cab; color:#fff; border:none; padding:7px 14px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.85rem; font-family:'Cairo';">إضافة</button>
        </div>
      </div>

      <!-- عرض الأصناف المخزنة -->
      <div style="border:1px solid #e2e8f0; border-radius:8px; overflow:hidden;">
        <div style="background:#e2e8f0; padding:6px 10px; font-size:0.85rem; font-weight:bold; color:#334155; display:flex; justify-content:space-between;">
          <span>الأصناف المسجلة بالنظام</span>
          <span id="g-items-count" style="color:#0b5cab;">0 صنف</span>
        </div>
        <div style="max-height:180px; overflow-y:auto;">
          <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:center;">
            <thead>
              <tr style="background:#f1f5f9; color:#475569; border-bottom:1px solid #cbd5e1;">
                <th style="padding:6px; text-align:right;">اسم الصنف</th>
                <th style="padding:6px;">السعر الافتراضي</th>
                <th style="padding:6px; width:45px;">حذف</th>
              </tr>
            </thead>
            <tbody id="g-items-table-body"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- زر إغلاق بالأسفل -->
    <div style="margin-top:12px; border-top:1px solid #eee; padding-top:10px;">
      <button onclick="closeGeneralSettings()" style="width:100%; background:#64748b; color:#fff; border:none; padding:10px; border-radius:8px; font-weight:bold; font-size:0.95rem; cursor:pointer; font-family:'Cairo';">إغلاق الإعدادات &#x2715;</button>
    </div>
  </div>
</div>

<script>
function openGeneralSettings() {
  renderGlobalItemsList();
  document.getElementById('general-settings-modal').style.display = 'flex';
}

function closeGeneralSettings() {
  document.getElementById('general-settings-modal').style.display = 'none';
  if (typeof populateInvoiceItemsDropdown === 'function') {
    populateInvoiceItemsDropdown();
  }
}

function renderGlobalItemsList() {
  const items = JSON.parse(localStorage.getItem('hisabak_items') || '[]');
  const countSpan = document.getElementById('g-items-count');
  if (countSpan) countSpan.innerText = items.length + ' صنف';
  const tbody = document.getElementById('g-items-table-body');
  if (!tbody) return;

  if (items.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" style="padding:15px; color:#94a3b8;">لا توجد أصناف، يمكنك الاستيراد من إكسل</td></tr>';
    return;
  }

  let rows = '';
  items.forEach((item, idx) => {
    rows += `<tr style="border-bottom:1px solid #f1f5f9;">
      <td style="padding:6px; text-align:right; font-weight:600;">${item.name}</td>
      <td style="padding:6px; color:#0b5cab;">${Number(item.price || 0).toLocaleString()} ر.ي</td>
      <td style="padding:6px;"><button onclick="deleteGlobalItem(${idx})" style="background:#fee2e2; color:#ef4444; border:none; border-radius:4px; padding:2px 8px; cursor:pointer; font-weight:bold;">✕</button></td>
    </tr>`;
  });
  tbody.innerHTML = rows;
}

function addGlobalItem() {
  const nameInput = document.getElementById('g-item-name');
  const priceInput = document.getElementById('g-item-price');
  const name = nameInput.value.trim();
  const price = parseFloat(priceInput.value) || 0;

  if (!name) { alert('يرجى كتابة اسم الصنف'); return; }

  const items = JSON.parse(localStorage.getItem('hisabak_items') || '[]');
  items.push({ name, price });
  localStorage.setItem('hisabak_items', JSON.stringify(items));

  nameInput.value = '';
  priceInput.value = '';
  renderGlobalItemsList();
}

function deleteGlobalItem(idx) {
  const items = JSON.parse(localStorage.getItem('hisabak_items') || '[]');
  items.splice(idx, 1);
  localStorage.setItem('hisabak_items', JSON.stringify(items));
  renderGlobalItemsList();
}

function clearAllItemsConfirm() {
  if (confirm('هل أنت متأكد من مسح جميع الأصناف؟')) {
    localStorage.removeItem('hisabak_items');
    renderGlobalItemsList();
  }
}

function handleGlobalExcelUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const data = new Uint8Array(evt.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
      
      const imported = [];
      rows.forEach((row, i) => {
        if (i === 0 && isNaN(parseFloat(row[1]))) return;
        if (row[0]) {
          imported.push({
            name: String(row[0]).trim(),
            price: parseFloat(row[1]) || 0
          });
        }
      });

      if (imported.length > 0) {
        const current = JSON.parse(localStorage.getItem('hisabak_items') || '[]');
        localStorage.setItem('hisabak_items', JSON.stringify(current.concat(imported)));
        renderGlobalItemsList();
        alert('تم بنجاح استيراد ' + imported.length + ' صنف إلى النظام!');
      } else {
        alert('الملف فارغ أو غير متوافق');
      }
    } catch(err) {
      alert('خطأ أثناء قراءة ملف الإكسل');
    }
    e.target.value = '';
  };
  reader.readAsArrayBuffer(file);
}
</script>
"""

# 2. زر فتح الإعدادات أعلى الشريط العلوي
settings_btn_icon = '<button onclick="openGeneralSettings()" title="الإعدادات العامة" style="background:transparent; border:none; color:#fff; font-size:1.25rem; cursor:pointer; padding:4px 8px; display:inline-flex; align-items:center;">⚙️</button>'

import re
# إزالة النسخة السابقة إذا وُجدت
if 'id="general-settings-modal"' in html:
    html = re.sub(r'<!-- General Settings Modal -->[\s\S]*?</script>', '', html)

# إضافة زر الإعدادات في الهيدر (Header) بجانب أيقونات الشريط العلوي
if 'openGeneralSettings()' not in html:
    if '<header' in html:
        html = re.sub(r'(<header[^>]*>)', r'\1\n' + settings_btn_icon, html, count=1)
    else:
        # إضافته في أول شريط يحتوي على كلمة حسابك
        html = html.replace('حسابك', 'حسابك ' + settings_btn_icon, 1)

html = html.replace('</body>', settings_modal + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SETTINGS_SYSTEM_READY")
