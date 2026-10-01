with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# تضمين مكتبة XLSX لقراءة ملفات إكسل ونظام إدارة واستيراد الأصناف
items_feature = """
<!-- XLSX Library for Excel Import -->
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

<!-- Items & Excel Modal -->
<div id="items-excel-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:12000; align-items:center; justify-content:center; direction:rtl; font-family:'Cairo', sans-serif;">
  <div style="background:#fff; width:92%; max-width:480px; border-radius:14px; padding:18px; box-shadow:0 8px 25px rgba(0,0,0,0.3); max-height:90vh; display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #0b5cab; padding-bottom:8px;">
      <h3 style="margin:0; color:#0b5cab; font-size:1.15rem;">إدارة ودليل الأصناف</h3>
      <button onclick="closeItemsModal()" style="background:#fee2e2; color:#dc2626; border:none; font-size:20px; font-weight:bold; width:34px; height:34px; border-radius:50%; cursor:pointer;">&#x2715;</button>
    </div>

    <!-- استيراد ملف إكسل -->
    <div style="background:#f0fdf4; border:1px dashed #22c55e; border-radius:8px; padding:12px; margin-top:12px; text-align:center;">
      <div style="font-weight:bold; color:#15803d; font-size:0.9rem; margin-bottom:6px;">📥 استيراد أصناف من ملف إكسل (Excel/CSV)</div>
      <input type="file" id="excel-file-input" accept=".xlsx, .xls, .csv" style="display:none;" onchange="handleExcelUpload(event)">
      <button onclick="document.getElementById('excel-file-input').click()" style="background:#16a34a; color:#fff; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.85rem; font-family:'Cairo';">اختيار ملف إكسل 📊</button>
      <div style="font-size:11px; color:#666; margin-top:5px;">الأعمدة المطلوبة: اسم الصنف - السعر</div>
    </div>

    <!-- إضافة صنف يدوياً -->
    <div style="background:#f8f9fa; border-radius:8px; padding:10px; margin-top:10px; border:1px solid #e9ecef; display:flex; gap:6px;">
      <input type="text" id="manual-item-name" placeholder="اسم الصنف" style="flex:2; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
      <input type="number" id="manual-item-price" placeholder="السعر" style="flex:1; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
      <button onclick="addManualItem()" style="background:#0b5cab; color:#fff; border:none; padding:7px 12px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.85rem; font-family:'Cairo';">إضافة</button>
    </div>

    <!-- قائمة الأصناف -->
    <div style="flex:1; overflow-y:auto; margin-top:10px;">
      <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:center;">
        <thead>
          <tr style="background:#0b5cab; color:#fff;">
            <th style="padding:6px;">اسم الصنف</th>
            <th style="padding:6px;">السعر الافتراضي</th>
            <th style="padding:6px; width:45px;">حذف</th>
          </tr>
        </thead>
        <tbody id="items-table-rows"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
function getItems() {
  return JSON.parse(localStorage.getItem('hisabak_items') || '[]');
}

function saveItems(items) {
  localStorage.setItem('hisabak_items', JSON.stringify(items));
  renderItemsTable();
  populateInvoiceItemsDropdown();
}

function openItemsModal() {
  renderItemsTable();
  document.getElementById('items-excel-modal').style.display = 'flex';
}

function closeItemsModal() {
  document.getElementById('items-excel-modal').style.display = 'none';
}

function renderItemsTable() {
  const items = getItems();
  const tbody = document.getElementById('items-table-rows');
  if (!tbody) return;
  if (items.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" style="padding:15px; color:#888;">لم يتم استيراد أو إضافة أصناف بعد</td></tr>';
    return;
  }
  let trs = '';
  items.forEach((item, idx) => {
    trs += `<tr style="border-bottom:1px solid #eee;">
      <td style="padding:6px; text-align:right; font-weight:bold;">${item.name}</td>
      <td style="padding:6px; color:#0b5cab;">${Number(item.price || 0).toLocaleString()} ر.ي</td>
      <td style="padding:6px;"><button onclick="deleteItem(${idx})" style="background:#ef4444; color:#fff; border:none; border-radius:4px; padding:2px 6px; cursor:pointer;">✕</button></td>
    </tr>`;
  });
  tbody.innerHTML = trs;
}

function addManualItem() {
  const name = document.getElementById('manual-item-name').value.trim();
  const price = parseFloat(document.getElementById('manual-item-price').value) || 0;
  if (!name) { alert('يرجى كتابة اسم الصنف'); return; }
  const items = getItems();
  items.push({ name, price });
  saveItems(items);
  document.getElementById('manual-item-name').value = '';
  document.getElementById('manual-item-price').value = '';
}

function deleteItem(idx) {
  const items = getItems();
  items.splice(idx, 1);
  saveItems(items);
}

function handleExcelUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const data = new Uint8Array(evt.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
      
      const newItems = [];
      rows.forEach((row, i) => {
        if (i === 0 && isNaN(parseFloat(row[1]))) return; // تخطي رأس الجدول إن وجد
        if (row[0]) {
          newItems.push({
            name: String(row[0]).trim(),
            price: parseFloat(row[1]) || 0
          });
        }
      });

      if (newItems.length > 0) {
        const current = getItems();
        saveItems(current.concat(newItems));
        alert('تم استيراد ' + newItems.length + ' صنف بنجاح!');
      } else {
        alert('الملف فارغ أو التنسيق غير متطابق');
      }
    } catch(err) {
      alert('حدث خطأ أثناء قراءة ملف الإكسل');
    }
  };
  reader.readAsArrayBuffer(file);
}

function populateInvoiceItemsDropdown() {
  const sel = document.getElementById('invoice-item-select');
  if (!sel) return;
  const items = getItems();
  let opts = '<option value="">-- اختر صنفاً لإدراجه في الفاتورة --</option>';
  items.forEach((it, idx) => {
    opts += `<option value="${idx}">${it.name} (${Number(it.price).toLocaleString()} ر.ي)</option>`;
  });
  sel.innerHTML = opts;
}

function onInvoiceItemSelected() {
  const sel = document.getElementById('invoice-item-select');
  const items = getItems();
  const selected = items[sel.value];
  if (selected) {
    document.getElementById('item-qty').value = 1;
    document.getElementById('item-unit-price').value = selected.price;
    calcInvoiceItemTotal();
  }
}

function calcInvoiceItemTotal() {
  const qty = parseFloat(document.getElementById('item-qty').value) || 0;
  const price = parseFloat(document.getElementById('item-unit-price').value) || 0;
  const total = qty * price;
  document.getElementById('tx-amount').value = total > 0 ? total : '';
  const sel = document.getElementById('invoice-item-select');
  const items = getItems();
  const selected = items[sel.value];
  if (selected) {
    document.getElementById('tx-note').value = `${selected.name} (عدد ${qty} × ${price})`;
  }
}

// تشغيل التعبئة عند تحميل الصفحة
window.addEventListener('load', () => {
  populateInvoiceItemsDropdown();
});
</script>
"""

# زر الأصناف في أعلى كشف الحساب وتضمين حقول اختيار الصنف والكمية
ledger_insert_box = """
      <!-- ربط الفاتورة بالأصناف -->
      <div id="item-picker-box" style="margin-bottom:8px; background:#fff; padding:6px; border-radius:6px; border:1px solid #ddd;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
          <label style="font-size:0.8rem; font-weight:bold; color:#0b5cab;">اختيار من الأصناف:</label>
          <button type="button" onclick="openItemsModal()" style="background:#e3f2fd; color:#0b5cab; border:1px solid #90caf9; border-radius:4px; font-size:11px; padding:2px 8px; cursor:pointer; font-weight:bold; font-family:'Cairo';">📦 استيراد/إدارة الأصناف</button>
        </div>
        <select id="invoice-item-select" onchange="onInvoiceItemSelected()" style="width:100%; padding:6px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo'; margin-bottom:6px;">
        </select>
        <div style="display:flex; gap:6px;">
          <input type="number" id="item-qty" placeholder="الكمية" oninput="calcInvoiceItemTotal()" style="flex:1; padding:6px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
          <input type="number" id="item-unit-price" placeholder="سعر الوحدة" oninput="calcInvoiceItemTotal()" style="flex:1; padding:6px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
        </div>
      </div>
"""

import re
if 'items-excel-modal' not in html:
    # إدراج حقول الأصناف قبل حقل المبلغ
    html = html.replace('<div style="font-size:0.85rem; font-weight:bold; color:#555; margin-bottom:6px;">تسجيل عملية جديدة:</div>', '<div style="font-size:0.85rem; font-weight:bold; color:#555; margin-bottom:6px;">تسجيل عملية جديدة:</div>' + ledger_insert_box)
    html = html.replace('</body>', items_feature + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("ITEMS_EXCEL_READY")
