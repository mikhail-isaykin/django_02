/**
 * cart.js — Alpine.js глобальное состояние корзины.
 * Адаптирован из raum.html (CartContext + CartSidebar JS).
 *
 * Данные о товарах хранятся на сервере (Django session).
 * Этот файл хранит только UI-состояние:
 * открыт/закрыт сайдбар, счётчик, сумма.
 *
 * Синхронизация с сервером происходит через HTMX-события.
 */
function cartStore() {
  return {
    // UI-состояние
    isCartOpen: false,
    cartCount:  0,
    cartTotal:  0.00,

    // Инициализация: загружаем данные с сервера
    async initCart() {
      try {
        const res  = await fetch('/cart/summary/', {
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        this.cartCount = data.count;
        this.cartTotal = data.total;
      } catch (e) {
        // Молча падаем — корзина обновится при следующем действии
        console.warn('Cart init failed:', e);
      }
    },

    // Открыть сайдбар + триггер для HTMX (загрузит список товаров)
    openCart() {
      this.isCartOpen = true;
      // HTMX-событие: cart_sidebar.html слушает "open-cart from:body"
      document.body.dispatchEvent(new Event('open-cart'));
    },

    closeCart() {
      this.isCartOpen = false;
    },

    /**
     * Вызывается когда HTMX получил ответ от /cart/add/ или /cart/update/.
     * Django возвращает HX-Trigger заголовок с {"cartUpdated": {count, total}}.
     */
    onCartUpdated(detail) {
      if (detail.count !== undefined) this.cartCount = detail.count;
      if (detail.total !== undefined) this.cartTotal  = detail.total;
      this.openCart();
    },
  };
}
