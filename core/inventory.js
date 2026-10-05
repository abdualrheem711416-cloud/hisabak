(() => {
  'use strict';

  const Storage = window.HisabakStorage;

  if (!Storage) {
    console.error(
      'HisabakInventory: يجب تحميل core/storage.js أولاً'
    );
    return;
  }

  const MOVEMENT_TYPES = Object.freeze({
    opening: 'opening',
    purchase: 'purchase',
    sale: 'sale',
    purchaseReturn: 'purchase_return',
    saleReturn: 'sale_return',
    transferOut: 'transfer_out',
    transferIn: 'transfer_in',
    adjustment: 'adjustment',
    stocktake: 'stocktake'
  });

  function getMovements() {
    return Storage.getCollection(
      Storage.KEYS.inventoryMovements
    );
  }

  function getMovement(id) {
    return getMovements().find(
      movement => movement.id === id
    ) || null;
  }

  function saveMovements(movements) {
    if (!Storage.setCollection(
      Storage.KEYS.inventoryMovements,
      movements
    )) {
      throw new Error('تعذر حفظ حركة المخزون');
    }

    return movements;
  }

  function addMovement(data = {}) {
    if (!data.itemId) {
      throw new Error('الصنف مطلوب');
    }

    if (!data.warehouseId) {
      throw new Error('المخزن مطلوب');
    }

    if (!data.type) {
      throw new Error('نوع الحركة مطلوب');
    }

    const quantity = Number(data.quantity || 0);

if (quantity === 0) {
  throw new Error('الكمية لا يمكن أن تكون صفرًا');
}

if (
  quantity < 0 &&
  data.type !== MOVEMENT_TYPES.adjustment
) {
  throw new Error('الكمية السالبة مسموحة فقط في التسوية');
}

    const movement = {
      id: data.id || Storage.generateId('im'),
      date: data.date || Storage.nowISO(),
      itemId: String(data.itemId),
      warehouseId: String(data.warehouseId),
      type: String(data.type),
      quantity,
      unitCost: Number(data.unitCost || 0),
      referenceType: data.referenceType || null,
      referenceId: data.referenceId || null,
      description: data.description || '',
      branchId: data.branchId || null,
      createdAt: data.createdAt || Storage.nowISO(),
      updatedAt: Storage.nowISO()
    };

    const movements = getMovements();
    movements.push(movement);
    saveMovements(movements);

    return movement;
  }

  function getItemWarehouseMovements(
    itemId,
    warehouseId
  ) {
    return getMovements().filter(
      movement =>
        movement.itemId === String(itemId) &&
        movement.warehouseId === String(warehouseId)
    );
  }

  function getMovementEffect(movement) {
    const quantity = Number(
      movement.quantity || 0
    );

    switch (movement.type) {
      case MOVEMENT_TYPES.purchase:
      case MOVEMENT_TYPES.saleReturn:
      case MOVEMENT_TYPES.transferIn:
      case MOVEMENT_TYPES.opening:
        return quantity;

      case MOVEMENT_TYPES.sale:
      case MOVEMENT_TYPES.purchaseReturn:
      case MOVEMENT_TYPES.transferOut:
        return -quantity;

      case MOVEMENT_TYPES.adjustment:
      case MOVEMENT_TYPES.stocktake:
        return quantity;

      default:
        return 0;
    }
  }

  function getStock(
    itemId,
    warehouseId
  ) {
    const movements =
      getItemWarehouseMovements(
        itemId,
        warehouseId
      );

    let quantity = 0;

    movements.forEach(movement => {
      quantity += getMovementEffect(movement);
    });

    return {
      itemId: String(itemId),
      warehouseId: String(warehouseId),
      quantity
    };
  }

  function getItemTotalStock(itemId) {
    const warehouseIds = new Set();

    getMovements().forEach(movement => {
      if (movement.itemId === String(itemId)) {
        warehouseIds.add(movement.warehouseId);
      }
    });

    let total = 0;

    warehouseIds.forEach(warehouseId => {
      total += getStock(
        itemId,
        warehouseId
      ).quantity;
    });

    return {
      itemId: String(itemId),
      quantity: total
    };
  }

  function getWarehouseStock(warehouseId) {
    const itemIds = new Set();

    getMovements().forEach(movement => {
      if (
        movement.warehouseId ===
        String(warehouseId)
      ) {
        itemIds.add(movement.itemId);
      }
    });

    return Array.from(itemIds).map(itemId => ({
      itemId,
      ...getStock(
        itemId,
        warehouseId
      )
    }));
  }

  function recordPurchase(data = {}) {
    return addMovement({
      ...data,
      type: MOVEMENT_TYPES.purchase
    });
  }

  function recordSale(data = {}) {
    const stock = getStock(
      data.itemId,
      data.warehouseId
    );

    const quantity = Number(
      data.quantity || 0
    );

    if (stock.quantity < quantity) {
      throw new Error(
        `الكمية غير كافية. الرصيد الحالي: ${stock.quantity}`
      );
    }

    return addMovement({
      ...data,
      type: MOVEMENT_TYPES.sale
    });
  }

  function recordPurchaseReturn(data = {}) {
    return addMovement({
      ...data,
      type: MOVEMENT_TYPES.purchaseReturn
    });
  }

  function recordSaleReturn(data = {}) {
    return addMovement({
      ...data,
      type: MOVEMENT_TYPES.saleReturn
    });
  }

  function transferStock(data = {}) {
    if (
      !data.fromWarehouseId ||
      !data.toWarehouseId
    ) {
      throw new Error(
        'يجب تحديد المخزن المصدر والمخزن المستلم'
      );
    }

    if (
      data.fromWarehouseId ===
      data.toWarehouseId
    ) {
      throw new Error(
        'لا يمكن التحويل إلى نفس المخزن'
      );
    }

    const quantity = Number(
      data.quantity || 0
    );

    if (quantity <= 0) {
      throw new Error(
        'الكمية يجب أن تكون أكبر من صفر'
      );
    }

    const stock = getStock(
      data.itemId,
      data.fromWarehouseId
    );

    if (stock.quantity < quantity) {
      throw new Error(
        `الكمية غير كافية في المخزن المصدر. الرصيد الحالي: ${stock.quantity}`
      );
    }

    const referenceId =
      data.referenceId ||
      Storage.generateId('transfer');

    const out = addMovement({
      ...data,
      warehouseId: data.fromWarehouseId,
      type: MOVEMENT_TYPES.transferOut,
      referenceType: 'stock_transfer',
      referenceId,
      description:
        data.description ||
        'تحويل مخزون - صادر'
    });

    const incoming = addMovement({
      ...data,
      warehouseId: data.toWarehouseId,
      type: MOVEMENT_TYPES.transferIn,
      referenceType: 'stock_transfer',
      referenceId,
      description:
        data.description ||
        'تحويل مخزون - وارد'
    });

    return {
      referenceId,
      out,
      incoming
    };
  }

  function adjustStock(data = {}) {
    if (!data.itemId) {
      throw new Error('الصنف مطلوب');
    }

    if (!data.warehouseId) {
      throw new Error('المخزن مطلوب');
    }

    const quantity = Number(
      data.quantity || 0
    );

    if (quantity === 0) {
      throw new Error(
        'كمية التسوية لا يمكن أن تكون صفرًا'
      );
    }

    return addMovement({
      ...data,
      type: MOVEMENT_TYPES.adjustment,
      quantity:  quantity,
      description:
        data.description ||
        'تسوية مخزون'
    });
  }

  function getInventorySummary() {
    const movements = getMovements();

    const items = {};
    const warehouses = {};

    movements.forEach(movement => {
      const itemId = movement.itemId;
      const warehouseId = movement.warehouseId;

      if (!items[itemId]) {
        items[itemId] = 0;
      }

      if (!warehouses[warehouseId]) {
        warehouses[warehouseId] = 0;
      }

      const effect =
        getMovementEffect(movement);

      items[itemId] += effect;
      warehouses[warehouseId] += effect;
    });

    return {
      items,
      warehouses,
      movementsCount: movements.length
    };
  }

  window.HisabakInventory = Object.freeze({
    MOVEMENT_TYPES,
    getMovements,
    getMovement,
    addMovement,
    getStock,
    getItemTotalStock,
    getWarehouseStock,
    recordPurchase,
    recordSale,
    recordPurchaseReturn,
    recordSaleReturn,
    transferStock,
    adjustStock,
    getInventorySummary
  });

})();
