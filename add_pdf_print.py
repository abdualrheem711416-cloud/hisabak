with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# كود زر الطباعة والتنسيق الخاص بـ PDF
pdf_print_code = """
<style>
@media print {
  body * {
    visibility: hidden;
  }
  #print-area, #print-area * {
    visibility: visible;
  }
  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0;
    padding: 20px;
    direction: rtl;
    font-family: 'Cairo', sans-serif !important;
  }
  .no-print {
    display: none !important;
  }
}
</style>

<script>
function printSupplierLedgerPDF() {
  const list = getSuppliers();
  const sup = list[currentSupIndex];
  if (!sup) return;

  const txList = sup.transactions || [];
  let rowsHtml = '';
  
  txList.forEach((tx, idx) => {
    rowsHtml += `
      <tr style="border-bottom: 1px solid #ddd; text-align: center;">
        <td style="padding: 8px;">${idx + 1}</td>
        <td style="padding: 8px;">${tx.date || '-'}</td>
        <td style="padding: 8px; font-weight: bold;">${tx.note || '-'}</td>
        <td style="padding: 8px; color: #b91c1c;">${tx.credit ? Number(tx.credit).toLocaleString() : '-'}</td>
        <td style="padding: 8px; color: #15803d;">${tx.debit ? Number(tx.debit).toLocaleString() : '-'}</td>
      </tr>
    `;
  });

  const printArea = document.createElement('div');
  printArea.id = 'print-area';
  printArea.innerHTML = `
    <div style="text-align: center; border-bottom: 2px solid #0b5cab; padding-bottom: 12px; margin-bottom: 15px;">
      <h2 style="margin: 0; color: #0b5cab; font-size: 1.4rem;">تطبيق حسابك</h2>
      <h3 style="margin: 5px 0; color: #333; font-size: 1.15rem;">كشف حساب مورد</h3>
      <div style="display: flex; justify-content: space-between; font-size: 0.95rem; margin-top: 10px; padding: 0 10px;">
        <span><strong>اسم المورد:</strong> ${sup.name}</span>
        <span><strong>تاريخ التقرير:</strong> ${new Date().toLocaleDateString('ar-EG')}</span>
      </div>
      <div style="text-align: right; margin-top: 5px; padding: 0 10px; font-size: 1rem; color: #b91c1c;">
        <strong>الرصيد الإجمالي:</strong> ${Number(sup.balance).toLocaleString()} ر.ي
      </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; margin-top: 10px;">
      <thead>
        <tr style="background: #0b5cab; color: white; text-align: center;">
          <th style="padding: 8px; border: 1px solid #0b5cab;">#</th>
          <th style="padding: 8px; border: 1px solid #0b5cab;">التاريخ</th>
          <th style="padding: 8px; border: 1px solid #0b5cab;">البيان</th>
          <th style="padding: 8px; border: 1px solid #0b5cab;">له (فاتورة)</th>
          <th style="padding: 8px; border: 1px solid #0b5cab;">عليه (سداد)</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml || '<tr><td colspan="5" style="padding: 15px; text-align: center;">لا توجد عمليات مسجلة</td></tr>'}
      </tbody>
    </table>

    <div style="margin-top: 30px; display: flex; justify-content: space-between; font-size: 0.9rem; padding: 0 20px;">
      <div>توقيع المحاسب: ....................</div>
      <div>توقيع المستلم: ....................</div>
    </div>
  `;

  document.body.appendChild(printArea);
  window.print();
  document.body.removeChild(printArea);
}
</script>
"""

# زر الطباعة داخل نافذة كشف الحساب بجانب زر الإغلاق
btn_target = '<button onclick="closeLedgerModal()"'
new_btn = '<button onclick="printSupplierLedgerPDF()" style="background:#17a2b8; color:#fff; border:none; border-radius:6px; padding:6px 12px; font-size:0.85rem; font-weight:bold; cursor:pointer; margin-left:8px; font-family:\'Cairo\';">📄 طباعة / PDF</button>\n      <button onclick="closeLedgerModal()"'

if 'printSupplierLedgerPDF' not in html:
    html = html.replace(btn_target, new_btn)
    html = html.replace('</body>', pdf_print_code + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("PDF_FEATURE_READY")
