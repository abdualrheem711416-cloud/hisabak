(() => {
  'use strict';

  const Storage = window.HisabakStorage;

  if (!Storage) {
    console.error(
      'HisabakAccounting: يجب تحميل core/storage.js أولاً'
    );
    return;
  }

  const ACCOUNT_TYPES = Object.freeze({
    asset: 'asset',
    liability: 'liability',
    equity: 'equity',
    revenue: 'revenue',
    expense: 'expense'
  });

  function createAccount(data = {}) {
    if (!data.name) {
      throw new Error('اسم الحساب مطلوب');
    }

    const account = {
      id: data.id || Storage.generateId('acc'),
      code: String(data.code || ''),
      name: String(data.name),
      type: data.type || ACCOUNT_TYPES.asset,
      parentId: data.parentId || null,
      currencyId: data.currencyId || null,
      isActive: data.isActive !== false,
      level: Number(data.level || 1),
      createdAt: data.createdAt || Storage.nowISO(),
      updatedAt: Storage.nowISO()
    };

    const accounts = Storage.getCollection(
      Storage.KEYS.accounts
    );

    const duplicate = accounts.find(
      item =>
        item.id === account.id ||
        (
          account.code &&
          item.code === account.code
        )
      );

    if (duplicate) {
      throw new Error('الحساب موجود مسبقًا');
    }

    accounts.push(account);

    if (!Storage.setCollection(
      Storage.KEYS.accounts,
      accounts
    )) {
      throw new Error('تعذر حفظ الحساب');
    }

    return account;
  }

  function getAccounts() {
    return Storage.getCollection(
      Storage.KEYS.accounts
    );
  }

  function getAccount(id) {
    return getAccounts().find(
      account => account.id === id
    ) || null;
  }

  function updateAccount(id, changes = {}) {
    const accounts = getAccounts();
    const index = accounts.findIndex(
      account => account.id === id
    );

    if (index === -1) {
      throw new Error('الحساب غير موجود');
    }

    accounts[index] = {
      ...accounts[index],
      ...changes,
      id: accounts[index].id,
      updatedAt: Storage.nowISO()
    };

    if (!Storage.setCollection(
      Storage.KEYS.accounts,
      accounts
    )) {
      throw new Error('تعذر تحديث الحساب');
    }

    return accounts[index];
  }

  function validateLines(lines) {
    if (!Array.isArray(lines) || lines.length < 2) {
      throw new Error(
        'القيد يجب أن يحتوي على سطرين على الأقل'
      );
    }

    let debit = 0;
    let credit = 0;

    lines.forEach((line, index) => {
      if (!line.accountId) {
        throw new Error(
          `الحساب مفقود في السطر ${index + 1}`
        );
      }

      const account = getAccount(line.accountId);

      if (!account) {
        throw new Error(
          `الحساب غير موجود في السطر ${index + 1}`
        );
      }

      const d = Number(line.debit || 0);
      const c = Number(line.credit || 0);

      if (d < 0 || c < 0) {
        throw new Error(
          'لا يمكن استخدام مبلغ سالب'
        );
      }

      if (d > 0 && c > 0) {
        throw new Error(
          'السطر الواحد لا يمكن أن يحتوي مدين ودائن معًا'
        );
      }

      if (d === 0 && c === 0) {
        throw new Error(
          `يجب إدخال مبلغ في السطر ${index + 1}`
        );
      }

      debit += d;
      credit += c;
    });

    const difference = Math.round(
      (debit - credit) * 100
    ) / 100;

    if (difference !== 0) {
      throw new Error(
        `القيد غير متوازن. الفرق: ${difference}`
      );
    }

    return {
      debit,
      credit,
      difference
    };
  }

  function postJournalEntry(data = {}) {
    if (!data.date) {
      throw new Error('تاريخ القيد مطلوب');
    }

    if (!data.description) {
      throw new Error('بيان القيد مطلوب');
    }

    const lines = Array.isArray(data.lines)
      ? data.lines
      : [];

    const totals = validateLines(lines);

    const entry = {
      id: data.id || Storage.generateId('je'),
      entryNo: data.entryNo || (
        'JE-' +
        Date.now().toString()
      ),
      date: data.date,
      description: String(data.description),
      referenceType: data.referenceType || null,
      referenceId: data.referenceId || null,
      branchId: data.branchId || null,
      costCenterId: data.costCenterId || null,
      currencyId: data.currencyId || null,
      exchangeRate: Number(data.exchangeRate || 1),
      status: 'posted',
      totalDebit: totals.debit,
      totalCredit: totals.credit,
      lines: lines.map(line => ({
        id: line.id || Storage.generateId('line'),
        accountId: line.accountId,
        description: line.description || data.description,
        debit: Number(line.debit || 0),
        credit: Number(line.credit || 0)
      })),
      createdAt: Storage.nowISO(),
      updatedAt: Storage.nowISO()
    };

    const entries = Storage.getCollection(
      Storage.KEYS.journalEntries
    );

    entries.push(entry);

    if (!Storage.setCollection(
      Storage.KEYS.journalEntries,
      entries
    )) {
      throw new Error('تعذر حفظ القيد');
    }

    return entry;
  }

  function getJournalEntries() {
    return Storage.getCollection(
      Storage.KEYS.journalEntries
    );
  }

  function getJournalEntry(id) {
    return getJournalEntries().find(
      entry => entry.id === id
    ) || null;
  }

  function getAccountMovements(accountId) {
    const result = [];

    getJournalEntries().forEach(entry => {
      (entry.lines || []).forEach(line => {
        if (line.accountId === accountId) {
          result.push({
            entryId: entry.id,
            entryNo: entry.entryNo,
            date: entry.date,
            description: line.description,
            debit: Number(line.debit || 0),
            credit: Number(line.credit || 0),
            referenceType: entry.referenceType,
            referenceId: entry.referenceId
          });
        }
      });
    });

    return result.sort(
      (a, b) =>
        new Date(a.date) - new Date(b.date)
    );
  }

  function getAccountBalance(accountId) {
    const movements =
      getAccountMovements(accountId);

    let debit = 0;
    let credit = 0;

    movements.forEach(movement => {
      debit += Number(movement.debit || 0);
      credit += Number(movement.credit || 0);
    });

    const account = getAccount(accountId);

    let balance = 0;

    if (
      account &&
      (
        account.type === ACCOUNT_TYPES.asset ||
        account.type === ACCOUNT_TYPES.expense
      )
    ) {
      balance = debit - credit;
    } else {
      balance = credit - debit;
    }

    return {
      accountId,
      debit,
      credit,
      balance
    };
  }

  function reverseJournalEntry(
    entryId,
    reason = 'عكس قيد'
  ) {
    const original = getJournalEntry(entryId);

    if (!original) {
      throw new Error('القيد غير موجود');
    }

    if (original.status === 'reversed') {
      throw new Error('القيد معكوس مسبقًا');
    }

    const reversedLines = (original.lines || []).map(
      line => ({
        accountId: line.accountId,
        description: reason,
        debit: Number(line.credit || 0),
        credit: Number(line.debit || 0)
      })
    );

    const reversed = postJournalEntry({
      date: new Date().toISOString(),
      description: reason,
      referenceType: 'reversal',
      referenceId: original.id,
      lines: reversedLines
    });

    const entries = getJournalEntries();
    const index = entries.findIndex(
      entry => entry.id === original.id
    );

    if (index !== -1) {
      entries[index] = {
        ...entries[index],
        status: 'reversed',
        reversedBy: reversed.id,
        updatedAt: Storage.nowISO()
      };

      Storage.setCollection(
        Storage.KEYS.journalEntries,
        entries
      );
    }

    return reversed;
  }

  function getTrialBalance() {
    const accounts = getAccounts();

    return accounts.map(account => {
      const balance =
        getAccountBalance(account.id);

      return {
        id: account.id,
        code: account.code,
        name: account.name,
        type: account.type,
        debit: balance.debit,
        credit: balance.credit,
        balance: balance.balance
      };
    });
  }

  window.HisabakAccounting = Object.freeze({
    ACCOUNT_TYPES,
    createAccount,
    getAccounts,
    getAccount,
    updateAccount,
    validateLines,
    postJournalEntry,
    getJournalEntries,
    getJournalEntry,
    getAccountMovements,
    getAccountBalance,
    reverseJournalEntry,
    getTrialBalance
  });

})();
