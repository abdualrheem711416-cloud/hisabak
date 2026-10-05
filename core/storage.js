(() => {
  'use strict';

  const PREFIX = 'hisabak_core_v1:';

  function makeKey(name) {
    return PREFIX + String(name);
  }

  function parse(raw, fallback) {
    if (raw === null || raw === undefined) {
      return fallback;
    }

    try {
      return JSON.parse(raw);
    } catch (error) {
      console.error('HisabakStorage: JSON parse error', error);
      return fallback;
    }
  }

  function read(name, fallback = null) {
    try {
      const raw = localStorage.getItem(makeKey(name));
      return parse(raw, fallback);
    } catch (error) {
      console.error('HisabakStorage: read error', error);
      return fallback;
    }
  }

  function write(name, value) {
    try {
      localStorage.setItem(makeKey(name), JSON.stringify(value));
      return true;
    } catch (error) {
      console.error('HisabakStorage: write error', error);
      return false;
    }
  }

  function remove(name) {
    try {
      localStorage.removeItem(makeKey(name));
      return true;
    } catch (error) {
      console.error('HisabakStorage: remove error', error);
      return false;
    }
  }

  function has(name) {
    try {
      return localStorage.getItem(makeKey(name)) !== null;
    } catch (error) {
      return false;
    }
  }

  function update(name, updater, fallback = null) {
    const current = read(name, fallback);

    const next =
      typeof updater === 'function'
        ? updater(current)
        : updater;

    write(name, next);

    return next;
  }

  function getCollection(name) {
    const value = read(name, []);
    return Array.isArray(value) ? value : [];
  }

  function setCollection(name, items) {
    return write(
      name,
      Array.isArray(items) ? items : []
    );
  }

  function generateId(prefix = 'id') {
    if (
      typeof crypto !== 'undefined' &&
      typeof crypto.randomUUID === 'function'
    ) {
      return `${prefix}_${crypto.randomUUID()}`;
    }

    return (
      `${prefix}_` +
      Date.now().toString(36) +
      '_' +
      Math.random().toString(36).substring(2, 10)
    );
  }

  function nowISO() {
    return new Date().toISOString();
  }

  const KEYS = Object.freeze({
    settings: 'settings',
    accounts: 'accounts',
    journalEntries: 'journal_entries',
    customers: 'customers',
    suppliers: 'suppliers',
    items: 'items',
    warehouses: 'warehouses',
    invoices: 'invoices',
    vouchers: 'vouchers',
    inventoryMovements: 'inventory_movements',
    auditLog: 'audit_log'
  });

  window.HisabakStorage = Object.freeze({
    PREFIX,
    KEYS,
    makeKey,
    read,
    write,
    remove,
    has,
    update,
    getCollection,
    setCollection,
    generateId,
    nowISO
  });

})();
