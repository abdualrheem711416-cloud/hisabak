import re

code = """
<!-- نافذة كشف حساب المورد -->
<div id="supplier-ledger-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:11000; align-items:center; justify-content:center; direction:rtl; font-family:'Cairo', sans-serif;">
  <div style="background:#fff; width:92%; max-width:440px; border-radius:14px; padding:18px; box-shadow:0 8px 25px rgba(0,0,0,0.3); max-height:90vh; display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #0b5cab; padding-bottom:8px;">
      <div>
        <h3 id="ledger-sup-name" style="margin:0; color:#0b5cab; font-size:1.15rem;">كشف الحساب</h3>
        <span id="ledger-sup-balance" style="font-size:0.9rem; font-weight:bold; color:#d9534f;">الرصيد: 0 ر.ي</span>
      </div>
      <button onclick="closeLedgerModal()" style="background:#eee; border:none; border-radius:50%; width:32px; height:32px; font-size:18px; font-weight:bold; cursor:pointer;">&times;</button>
    </div>

    <div style="background:#f8f9fa; border-radius:8px; padding:10px; margin-top:12px; border:1px solid #e9ecef;">
      <div style="font-size:0.85rem; font-weight:bold; color:#555; margin-bottom:6px;">تسجيل عملية جديدة:</div>
      <div style="display:flex; gap:6px; margin-bottom:6px;">
        <select id="tx-type" style="padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem; font-family:'Cairo';">
          <option value="invoice">فاتورة توريد (+ له)</option>
          <option value="payment">سداد دفعة (- عليه)</option>
        </select>
        <input type="number" id="tx-amount" placeholder="المبلغ" style="flex:1; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem;">
      </div>
      <div style="display:flex; gap:6px;">
        <input type="text" id="tx-note" placeholder="البيان / رقم السند" style="flex:1; padding:7px; border:1px solid #ccc; border-radius:6px; font-size:0.85rem;">
        <button onclick="addTransaction()" style="background:#28a745; color:#fff; border:none; padding:7px 14px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.85rem;">حفظ</button>
      </div>
    </div>

    <div style="flex:1; overflow-y:auto; margin-top:12px;">
      <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:center;">
        <thead>
          <tr style="background:#0b5cab; color:#fff;">
            <th style="padding:6px;">التاريخ</th>
            <th style="padding:6px;">البيان</th>
            <th style="padding:6px;">له (فاتورة)</th>
            <th style="padding:6px;">عليه (سداد)</th>
          </tr>
        </thead>
        <tbody id="ledger-rows"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
let currentSupIndex = -1;

function renderSuppliers() {
  const list = getSuppliers();
  const container = document.getElementById('suppliers-list');
  if (!container) return;
  if (list.length === 0) {
    container.innerHTML = '<p style="color:#888; font-size:14px; text-align:center;">لا يوجد موردين مسجلين</p>';
    return;
  }
  let html = '';
  list.forEach((s, idx) => {
    html += '<div style="display:flex; justify-content:space-between; align-items:center; padding:10px 8px; border-bottom:1px solid #eee;">' +
      '<div onclick="openSupplierLedger(' + idx + ')" style="cursor:pointer; flex:1;">' +
        '<strong style="color:#0b5cab; font-size:1.05rem; display:block;">' + s.name + ' <span style="font-size:11px; background:#e3f2fd; color:#0b5cab; padding:2px 6px; border-radius:4px; margin-right:4px;">فتح الحساب &larr;</span></strong>' +
        '<div style="font-size:12px; color:#d9534f; margin-top:2px;">الرصيد: ' + Number(s.balance).toLocaleString() + ' ر.ي</div>' +
      '</div>' +
      '<button onclick="event.stopPropagation(); deleteSupplier(' + idx + ')" style="background:#ff4d4d; color:white; border:none; border-radius:6px; padding:5px 10px; font-size:12px; cursor:pointer;">حذف</button>' +
    '</div>';
  });
  container.innerHTML = html;
}

function openSupplierLedger(idx) {
  currentSupIndex = idx;
  const list = getSuppliers();
  const sup = list[idx];
  if (!sup) return;

  document.getElementById('ledger-sup-name').innerText = 'حساب: ' + sup.name;
  document.getElementById('ledger-sup-balance').innerText = 'الرصيد الإجمالي: ' + Number(sup.balance).toLocaleString() + ' ر.ي';
  
  if (!sup.transactions) {
    sup.transactions = [
      { date: new Date().toLocaleDateString('ar-EG'), note: 'رصيد افتتاحي', credit: sup.balance, debit: 0 }
    ];
    list[idx] = sup;
    localStorage.setItem('hisabak_suppliers', JSON.stringify(list));
  }

  renderLedgerRows(sup.transactions);
  document.getElementById('supplier-ledger-modal').style.display = 'flex';
}

function closeLedgerModal() {
  document.getElementById('supplier-ledger-modal').style.display = 'none';
  renderSuppliers();
}

function renderLedgerRows(txList) {
  const tbody = document.getElementById('ledger-rows');
  if (!txList || txList.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" style="padding:10px; color:#999;">لا توجد حركات سابقة</td></tr>';
    return;
  }
  let trs = '';
  txList.slice().reverse().forEach(tx => {
    trs += '<tr style="border-bottom:1px solid #eee;">' +
      '<td style="padding:6px; color:#666;">' + (tx.date || '-') + '</td>' +
      '<td style="padding:6px; font-weight:bold;">' + (tx.note || '-') + '</td>' +
      '<td style="padding:6px; color:#d9534f;">' + (tx.credit ? Number(tx.credit).toLocaleString() : '-') + '</td>' +
      '<td style="padding:6px; color:#28a745;">' + (tx.debit ? Number(tx.debit).toLocaleString() : '-') + '</td>' +
    '</tr>';
  });
  tbody.innerHTML = trs;
}

function addTransaction() {
  const type = document.getElementById('tx-type').value;
  const amt = parseFloat(document.getElementById('tx-amount').value);
  const note = document.getElementById('tx-note').value.trim() || (type === 'invoice' ? 'فاتورة' : 'سداد دفعة');

  if (!amt || amt <= 0) {
    alert('يرجى إدخال مبلغ صحيح');
    return;
  }

  const list = getSuppliers();
  const sup = list[currentSupIndex];
  if (!sup) return;

  const credit = type === 'invoice' ? amt : 0;
  const debit = type === 'payment' ? amt : 0;

  sup.balance = (parseFloat(sup.balance) || 0) + credit - debit;
  if (!sup.transactions) sup.transactions = [];
  
  sup.transactions.push({
    date: new Date().toLocaleDateString('ar-EG'),
    note: note,
    credit: credit,
    debit: debit
  });

  list[currentSupIndex] = sup;
  localStorage.setItem('hisabak_suppliers', JSON.stringify(list));

  document.getElementById('tx-amount').value = '';
  document.getElementById('tx-note').value = '';

  document.getElementById('ledger-sup-balance').innerText = 'الرصيد الإجمالي: ' + Number(sup.balance).toLocaleString() + ' ر.ي';
  renderLedgerRows(sup.transactions);
}
</script>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'id="supplier-ledger-modal"' in html:
    html = re.sub(r'<!-- نافذة كشف حساب المورد -->[\s\S]*?</script>', '', html)

html = html.replace('</body>', code + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("LEDGER_READY")
