import re

modal_code = """
<!-- Suppliers Modal -->
<div id="suppliers-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:10000; align-items:center; justify-content:center; direction:rtl;">
  <div style="background:#fff; width:90%; max-width:400px; border-radius:12px; padding:20px; box-shadow:0 4px 15px rgba(0,0,0,0.2); max-height:85vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ddd; padding-bottom:10px;">
      <h3 style="margin:0; color:#0b5cab;">إدارة الموردين</h3>
      <button onclick="closeSuppliersModal()" style="background:none; border:none; font-size:24px; cursor:pointer;">&times;</button>
    </div>
    
    <div style="margin-top:15px;">
      <input type="text" id="sup-name" placeholder="اسم المورد" style="width:100%; padding:10px; margin-bottom:8px; border:1px solid #ccc; border-radius:6px; box-sizing:border-box;">
      <input type="number" id="sup-balance" placeholder="الرصيد الافتتاحي (ر.ي)" style="width:100%; padding:10px; margin-bottom:8px; border:1px solid #ccc; border-radius:6px; box-sizing:border-box;">
      <button onclick="addSupplier()" style="width:100%; background:#0b5cab; color:#fff; border:none; padding:10px; border-radius:6px; font-weight:bold; cursor:pointer;">إضافة مورد</button>
    </div>

    <div style="margin-top:20px;">
      <h4 style="margin:0 0 10px 0; color:#333;">قائمة الموردين:</h4>
      <div id="suppliers-list" style="max-height:200px; overflow-y:auto;"></div>
    </div>
  </div>
</div>

<script>
function openSuppliers() {
  document.getElementById('suppliers-modal').style.display = 'flex';
  renderSuppliers();
}

function closeSuppliersModal() {
  document.getElementById('suppliers-modal').style.display = 'none';
}

function getSuppliers() {
  const data = localStorage.getItem('hisabak_suppliers');
  return data ? JSON.parse(data) : [
    { name: 'شركة الأمل للتوريدات', balance: 3507845 }
  ];
}

function renderSuppliers() {
  const list = getSuppliers();
  const container = document.getElementById('suppliers-list');
  if (list.length === 0) {
    container.innerHTML = '<p style="color:#888; font-size:14px; text-align:center;">لا يوجد موردين مسجلين</p>';
    return;
  }
  let html = '';
  list.forEach((s, idx) => {
    html += '<div style="display:flex; justify-content:space-between; align-items:center; padding:8px; border-bottom:1px solid #eee;">' +
      '<div>' +
        '<strong>' + s.name + '</strong>' +
        '<div style="font-size:12px; color:#d9534f;">' + Number(s.balance).toLocaleString() + ' ر.ي</div>' +
      '</div>' +
      '<button onclick="deleteSupplier(' + idx + ')" style="background:#ff4d4d; color:white; border:none; border-radius:4px; padding:4px 8px; font-size:12px; cursor:pointer;">حذف</button>' +
    '</div>';
  });
  container.innerHTML = html;
}

function addSupplier() {
  const name = document.getElementById('sup-name').value.trim();
  const bal = parseFloat(document.getElementById('sup-balance').value) || 0;
  if (!name) {
    alert('يرجى كتابة اسم المورد');
    return;
  }
  const list = getSuppliers();
  list.unshift({ name: name, balance: bal });
  localStorage.setItem('hisabak_suppliers', JSON.stringify(list));
  document.getElementById('sup-name').value = '';
  document.getElementById('sup-balance').value = '';
  renderSuppliers();
}

function deleteSupplier(idx) {
  const list = getSuppliers();
  list.splice(idx, 1);
  localStorage.setItem('hisabak_suppliers', JSON.stringify(list));
  renderSuppliers();
}
</script>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any click alert on suppliers with openSuppliers()
content = re.sub(r'onclick=["\'][^"\']*الموردين[^"\']*["\']', 'onclick="openSuppliers()"', content)

if 'suppliers-modal' not in content:
    content = content.replace('</body>', modal_code + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
