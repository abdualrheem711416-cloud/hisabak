# -*- coding: utf-8 -*-
content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>العملاء</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --p: #1976D2; --pk: #e91e63; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; -webkit-tap-highlight-color: transparent; }
        body { background: #f5f5f5; padding-bottom: 70px; }
        .app-bar { background: var(--p); color: #fff; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .app-bar h1 { font-size: 18px; }
        .app-bar-actions { display: flex; gap: 18px; font-size: 18px; }
        .app-bar-actions i { cursor: pointer; }
        .top-menu { display: none; position: fixed; top: 50px; left: 12px; background: #fff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.2); z-index: 2000; min-width: 180px; border: 1px solid #ddd; }
        .top-menu div { padding: 10px 14px; font-size: 13px; border-bottom: 1px solid #eee; cursor: pointer; display: flex; gap: 8px; color: #333; }
        .search-bar { display: none; background: #fff; padding: 8px 12px; border-bottom: 1px solid #ddd; }
        .search-bar input { width: 100%; padding: 8px 12px; border-radius: 20px; border: 1px solid var(--p); outline: none; font-size: 13px; text-align: right; }
        .time-filter { background: #fff; padding: 10px; display: flex; justify-content: space-around; border-bottom: 1px solid #ddd; font-size: 14px; }
        .filters-container { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
        .select-box { width: 100%; padding: 8px 12px; border: 1px solid var(--p); border-radius: 20px; background: #fff; font-size: 14px; text-align: center; }
        .row-filters { display: flex; gap: 8px; }
        .sort-order { display: flex; align-items: center; justify-content: space-around; border: 1px solid var(--p); border-radius: 20px; padding: 4px 10px; background: #fff; width: 50%; font-size: 13px; }
        .date-range { display: flex; background: var(--p); border-radius: 20px; overflow: hidden; border: 1px solid var(--p); }
        .date-field { flex: 1; display: flex; align-items: center; background: #fff; padding: 4px 8px; border-radius: 18px; margin: 2px; }
        .date-field label { background: var(--p); color: #fff; padding: 4px 8px; font-size: 11px; border-radius: 12px; margin-left: 4px; }
        .date-field input { border: none; width: 100%; text-align: center; font-size: 12px; outline: none; }
        .customer-card { background: #fff; margin: 8px; border-radius: 8px; padding: 12px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); cursor: pointer; }
        .customer-header { display: flex; justify-content: space-between; align-items: flex-start; }
        .customer-info h3 { font-size: 16px; color: #333; }
        .customer-info p { font-size: 12px; color: #777; margin-top: 2px; }
        .balance-badge { color: #d32f2f; font-weight: bold; font-size: 15px; }
        .customer-actions { display: flex; gap: 12px; margin-top: 10px; align-items: center; }
        .icon-btn { width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 14px; cursor: pointer; }
        .fab { position: fixed; bottom: 60px; left: 20px; width: 52px; height: 52px; background: var(--pk); color: #fff; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 8px rgba(0,0,0,0.25); cursor: pointer; z-index: 500; }
        .bottom-summary { position: fixed; bottom: 0; left: 0; right: 0; background: var(--p); color: #fff; display: flex; justify-content: space-around; padding: 8px 0; text-align: center; font-size: 12px; z-index: 100; }
        .bottom-summary span { display: block; font-size: 14px; font-weight: bold; margin-top: 2px; }
        .modal-layer { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 2000; align-items: center; justify-content: center; padding: 16px; }
        .modal-card { background: #fff; width: 100%; max-width: 340px; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 12px; }
        .modal-card input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; text-align: center; font-size: 14px; outline: none; }
        .modal-btns { display: flex; gap: 8px; }
        .modal-btns button { flex: 1; padding: 10px; border: none; border-radius: 8px; color: #fff; font-weight: bold; cursor: pointer; }
        .statement-screen { display: none; position: fixed; inset: 0; background: #fff; z-index: 1500; flex-direction: column; }
        .st-th { display: grid; grid-template-columns: 1fr 1fr 1fr; background: var(--p); color: #fff; padding: 10px; text-align: center; font-size: 13px; font-weight: bold; }
        .st-tr { display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 12px 10px; border-bottom: 1px solid #eee; text-align: center; font-size: 13px; }
    </style>
</head>
<body>
    <div class="app-bar">
        <h1>العملاء</h1>
        <div class="app-bar-actions">
            <i class="fas fa-search" onclick="toggleSearch()"></i>
            <i class="fas fa-print" onclick="window.print()"></i>
            <i class="fas fa-share-alt" onclick="shareAll()"></i>
            <i class="fas fa-ellipsis-v" onclick="toggleMenu(event)"></i>
        </div>
    </div>
    <div class="top-menu" id="topMenu">
        <div onclick="alert('استيراد من إكسل')"><i class="fas fa-file-import" style="color:var(--p)"></i> استيراد من إكسل</div>
        <div onclick="alert('تصدير إلى إكسل')"><i class="fas fa-file-excel" style="color:#2e7d32"></i> تصدير إلى إكسل</div>
        <div onclick="resetData()" style="color:#d32f2f"><i class="fas fa-undo"></i> تصفير جميع الحسابات</div>
    </div>
    <div class="search-bar" id="searchBar">
        <input type="text" id="sInp" oninput="render()" placeholder="بحث باسم العميل...">
    </div>
    <div class="time-filter">
        <label><input type="radio" name="period" checked onchange="render()"> الجميع</label>
        <label><input type="radio" name="period" onchange="render()"> سنوي</label>
        <label><input type="radio" name="period" onchange="render()"> شهري</label>
        <label><input type="radio" name="period" onchange="render()"> يومي</label>
    </div>
    <div class="filters-container">
        <select class="select-box"><option>عمله محليه</option></select>
        <div class="row-filters">
            <select class="select-box" style="width:50%"><option>ترتيب بالاسم</option></select>
            <div class="sort-order">
                <label><input type="radio" name="sort" checked> تصاعدي</label>
                <label><input type="radio" name="sort"> تنازلي</label>
            </div>
        </div>
        <div class="date-range">
            <div class="date-field"><label>من تاريخ</label><input type="text" value="01/01/2026"></div>
            <div class="date-field"><label>الى تاريخ</label><input type="text" value="02/10/2026"></div>
        </div>
    </div>
    <div id="list"></div>
    <div class="fab" onclick="openAdd()"><i class="fas fa-plus"></i></div>
    <div class="bottom-summary">
        <div>له<span id="totC">0</span></div>
        <div>عليه<span id="totD">0</span></div>
        <div>الرصيد عليه<span id="totN">0</span></div>
    </div>
    <div class="modal-layer" id="addModal">
        <div class="modal-card">
            <h3 style="color:var(--p);text-align:center;">إضافة عميل جديد</h3>
            <input type="text" id="cN" placeholder="اسم العميل">
            <input type="tel" id="cP" placeholder="رقم الهاتف">
            <input type="number" id="cB" placeholder="الرصيد الافتتاحي" value="0">
            <div style="display:flex;justify-content:space-around;font-weight:bold;font-size:13px;">
                <label style="color:#d32f2f"><input type="radio" name="cT" value="debit" checked> عليه</label>
                <label style="color:var(--p)"><input type="radio" name="cT" value="credit"> له</label>
            </div>
            <div class="modal-btns">
                <button style="background:var(--p)" onclick="saveCustomer()">حفظ</button>
                <button style="background:#78909c" onclick="closeAdd()">إلغاء</button>
            </div>
        </div>
    </div>
    <div class="statement-screen" id="stScreen">
        <div class="app-bar">
            <div style="display:flex;align-items:center;gap:10px;">
                <i class="fas fa-arrow-right" onclick="closeSt()" style="cursor:pointer"></i>
                <h1 id="stTitle">كشف الحساب</h1>
            </div>
            <div class="app-bar-actions">
                <i class="fas fa-print" onclick="window.print()"></i>
                <i class="fas fa-share-alt" onclick="shareSt()"></i>
            </div>
        </div>
        <div class="st-th"><div>النوع</div><div>المبلغ</div><div>التاريخ</div></div>
        <div id="stRows" style="flex:1;overflow-y:auto;"></div>
        <div class="fab" onclick="openVoucher()" style="bottom:60px"><i class="fas fa-plus"></i></div>
        <div class="bottom-summary"><div style="width:100%">الرصيد الإجمالي: <span id="stBal">0</span></div></div>
    </div>
    <div class="modal-layer" id="vModal">
        <div class="modal-card">
            <h3 style="color:var(--p);text-align:center;" id="vTitle">إضافة سند للعميل</h3>
            <input type="number" id="vA" placeholder="المبلغ" style="font-size:16px;font-weight:bold;">
            <input type="text" id="vDesc" placeholder="البيان (دفعة نقدية)">
            <div style="display:flex;justify-content:space-around;font-weight:bold;font-size:13px;">
                <label style="color:#d32f2f"><input type="radio" name="vK" value="صرف" checked> صرف</label>
                <label style="color:var(--p)"><input type="radio" name="vK" value="قبض"> قبض</label>
            </div>
            <div class="modal-btns">
                <button style="background:var(--p)" onclick="saveVoucher()">حفظ السند</button>
                <button style="background:#78909c" onclick="closeVoucher()">إلغاء</button>
            </div>
        </div>
    </div>
    <script>
        var KEY = 'hisabak_customers';
        var data = [];
        var active = null;
        try { data = JSON.parse(localStorage.getItem(KEY)) || []; } catch(e){}
        if(!data.length){
            data = [
                {id:'1', name:'احمد', phone:'', balance:0, type:'debit', v:[]},
                {id:'2', name:'عميل نقدي عام', phone:'', balance:50000, type:'credit', v:[]},
                {id:'3', name:'شركة النور', phone:'', balance:150000, type:'credit', v:[]},
                {id:'4', name:'عبد الرحيم', phone:'776332929', balance:400000, type:'debit', v:[]}
            ];
            localStorage.setItem(KEY, JSON.stringify(data));
        }
        function render(){
            var c = document.getElementById('list');
            c.innerHTML = '';
            var q = (document.getElementById('sInp')?.value || '').trim().toLowerCase();
            var sC = 0, sD = 0;
            data.forEach(function(item){
                if(q && item.name.toLowerCase().indexOf(q) === -1 && (!item.phone || item.phone.indexOf(q) === -1)) return;
                var b = parseFloat(item.balance || 0);
                if(item.type === 'credit') sC += b; else sD += b;
                var dBal = (item.type === 'debit' && b > 0 ? '-' : '') + b.toLocaleString();
                var card = document.createElement('div');
                card.className = 'customer-card';
                card.onclick = function(){ openSt(item); };
                card.innerHTML = 
                    '<div class="customer-header">' +
                        '<div class="customer-info"><h3>' + item.name + '</h3><p>سقف المديونيه : 0</p></div>' +
                        '<div class="balance-badge">' + dBal + '</div>' +
                    '</div>' +
                    '<div class="customer-actions">' +
                        '<div class="icon-btn" style="background:#4fc3f7" onclick="event.stopPropagation(); quickV(\\'' + item.id + '\\')"><i class="fas fa-pen"></i></div>' +
                        '<div class="icon-btn" style="background:#0288d1" onclick="event.stopPropagation(); if(item.phone) location.href=\\'sms:\\' + item.phone;"><i class="fas fa-comment-dots"></i></div>' +
                        '<div class="icon-btn" style="background:#25d366" onclick="event.stopPropagation(); window.open(\\'https://wa.me/\\' + (item.phone||\\'\\') + \\'?text=\\' + encodeURIComponent(\\'رصيدكم: \\' + dBal), \\'_blank\\');"><i class="fab fa-whatsapp"></i></div>' +
                        '<i class="fas fa-caret-down" style="color:#666;margin-right:auto;"></i>' +
                    '</div>';
                c.appendChild(card);
            });
            document.getElementById('totC').innerText = sC.toLocaleString();
            document.getElementById('totD').innerText = sD.toLocaleString();
            document.getElementById('totN').innerText = (sD - sC).toLocaleString();
        }
        function openAdd(){ document.getElementById('addModal').style.display = 'flex'; }
        function closeAdd(){ document.getElementById('addModal').style.display = 'none'; }
        function saveCustomer(){
            var n = document.getElementById('cN').value.trim();
            if(!n){ alert('ادخل اسم العميل'); return; }
            var p = document.getElementById('cP').value.trim();
            var b = parseFloat(document.getElementById('cB').value) || 0;
            var t = document.querySelector('input[name="cT"]:checked').value;
            data.push({id:String(Date.now()), name:n, phone:p, balance:b, type:t, v:[]});
            localStorage.setItem(KEY, JSON.stringify(data));
            closeAdd();
            render();
        }
        function openSt(item){
            active = item;
            document.getElementById('stTitle').innerText = item.name;
            var b = parseFloat(item.balance || 0);
            var dBal = (item.type === 'debit' && b > 0 ? '-' : '') + b.toLocaleString();
            document.getElementById('stBal').innerText = dBal;
            var r = '<div class="st-tr"><div>رصيد افتتاحي</div><div style="color:var(--p);font-weight:bold;">' + b.toLocaleString() + '</div><div>01/01/2026</div></div>';
            if(item.v && item.v.length){
                item.v.forEach(function(x){
                    r += '<div class="st-tr"><div>' + x.k + ' (' + x.d + ')</div><div style="color:#d32f2f;font-weight:bold;">' + x.a.toLocaleString() + '</div><div>' + x.date + '</div></div>';
                });
            }
            document.getElementById('stRows').innerHTML = r;
            document.getElementById('stScreen').style.display = 'flex';
        }
        function closeSt(){ document.getElementById('stScreen').style.display = 'none'; render(); }
        function quickV(id){ active = data.find(function(x){ return x.id === id; }); if(active) openVoucher(); }
        function openVoucher(){
            if(!active) return;
            document.getElementById('vTitle').innerText = 'إضافة سند: ' + active.name;
            document.getElementById('vA').value = '';
            document.getElementById('vDesc').value = '';
            document.getElementById('vModal').style.display = 'flex';
        }
        function closeVoucher(){ document.getElementById('vModal').style.display = 'none'; }
        function saveVoucher(){
            var a = parseFloat(document.getElementById('vA').value) || 0;
            if(!a || !active){ alert('ادخل المبلغ'); return; }
            var k = document.querySelector('input[name="vK"]:checked').value;
            var d = document.getElementById('vDesc').value.trim() || (k === 'صرف' ? 'سند صرف' : 'سند قبض');
            var cur = parseFloat(active.balance || 0);
            if(k === 'صرف'){ active.balance = (active.type === 'credit') ? (cur - a) : (cur + a); }
            else { active.balance = (active.type === 'credit') ? (cur + a) : (cur - a); }
            if(!active.v) active.v = [];
            active.v.push({k:k, a:a, d:d, date:'02/10/2026'});
            localStorage.setItem(KEY, JSON.stringify(data));
            closeVoucher();
            if(document.getElementById('stScreen').style.display === 'flex') openSt(active);
            render();
        }
        function toggleSearch(){
            var s = document.getElementById('searchBar');
            s.style.display = (s.style.display === 'block') ? 'none' : 'block';
            if(s.style.display === 'block') document.getElementById('sInp').focus();
        }
        function toggleMenu(e){
            e.stopPropagation();
            var m = document.getElementById('topMenu');
            m.style.display = (m.style.display === 'block') ? 'none' : 'block';
        }
        function resetData(){
            if(confirm('هل تريد تصفير جميع الأرصدة؟')){
                data.forEach(function(x){ x.balance = 0; x.v = []; });
                localStorage.setItem(KEY, JSON.stringify(data));
                render();
            }
        }
        function shareAll(){
            var t = '*أرصدة العملاء*\\n';
            data.forEach(function(x){ t += '- ' + x.name + ': ' + (x.balance||0) + '\\n'; });
            window.open('https://wa.me/?text=' + encodeURIComponent(t), '_blank');
        }
        function shareSt(){
            if(!active) return;
            window.open('https://wa.me/' + (active.phone||'') + '?text=' + encodeURIComponent('*كشف حساب*\\nالعميل: ' + active.name + '\\nالرصيد: ' + active.balance), '_blank');
        }
        window.onclick = function(){ var m = document.getElementById('topMenu'); if(m) m.style.display = 'none'; };
        render();
    </script>
</body>
</html>"""

with open("customers.html", "w", encoding="utf-8") as f:
    f.write(content)

print("CUSTOMERS_FILE_OVERWRITTEN_OK")
