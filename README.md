# eyeshop 🕶️

A boutique e-commerce store for designer eyewear frames. Fast, minimal, no fluff.

Built as a proper Django project — server-rendered, SPA-like navigation via HTMX, reactive cart via Alpine.js, crypto checkout via NowPayments. Runs in Docker, served by Nginx.

---

### What's inside

The stack is deliberately lean. No React, no webpack, no node_modules nightmare.

- **Django 5** does the heavy lifting — ORM, sessions, templates, admin
- **PostgreSQL** for the database
- **HTMX** makes the UI feel like a SPA without writing a single line of fetch()
- **Alpine.js** handles the cart sidebar state and product gallery
- **Tailwind** for styling, with a small `custom.css` for variables and animations
- **NowPayments** for crypto payment processing
- **Docker + Nginx + Gunicorn** for deployment

---

### How it works

The catalog page filters by category without a page reload — HTMX swaps just the product grid. Product navigation works the same way. The URL updates, the back button works, but the page never fully refreshes.

The cart lives in Django sessions server-side. When you hit "Add to Bag", HTMX posts to the backend, Django updates the session and fires back an `HX-Trigger` header. Alpine.js picks that up, updates the counter in the header, and opens the sidebar. The sidebar itself fetches its content fresh from the server each time it opens.

Payments go through NowPayments — an invoice gets created, the user pays in crypto, NowPayments sends a signed webhook, we verify it with HMAC-SHA512 and flip the order status to paid.

---

### Getting started

Clone the repo and copy the env file:

```bash
git clone https://github.com/yourname/eyeshop.git
cd eyeshop
cp .env.example .env
```

Fill in `.env` with your database credentials and NowPayments API keys, then:

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

That's it. Open `http://localhost` in your browser.
Admin lives at `http://localhost/admin`.

---

### Project layout

```
eyeshop/
│
├── apps/
│   ├── catalog/        — products, categories, images
│   ├── cart/           — session cart with a proper Cart class
│   ├── orders/         — order creation and management
│   └── payments/       — NowPayments integration, webhook handler
│
├── templates/
│   ├── base.html
│   ├── partials/       — header, footer, cart sidebar, toast
│   └── catalog/        — shop page, product detail, grid partial
│
├── static/
│   ├── css/custom.css  — CSS variables, animations
│   └── js/cart.js      — Alpine.js cart store
│
├── config/             — settings split into base / local / production
├── nginx/
├── Dockerfile
└── docker-compose.yml
```

---

### Environment variables

Copy `.env.example` to `.env` and fill these in:

```
SECRET_KEY              — Django secret key
DEBUG                   — True in dev, False in prod
ALLOWED_HOSTS           — comma-separated list of hostnames

DB_NAME / DB_USER / DB_PASSWORD / DB_HOST

NOWPAYMENTS_API_KEY     — from your NowPayments dashboard
NOWPAYMENTS_IPN_SECRET  — for webhook signature verification
NOWPAYMENTS_SANDBOX     — set True while testing
```

---

### A few things worth knowing

The cart uses Django sessions, not localStorage. This means the cart survives page refreshes and works without JavaScript enabled for reading — only the interactive bits (open/close sidebar, quantity buttons) need JS.

The `NowPaymentsService` class is fully isolated in `apps/payments/services.py`. Swapping out the payment provider means touching exactly one file.

Filtering on the catalog page is done entirely server-side. No client-side filtering, no JSON endpoints, no state management. HTMX sends a GET request with a query param, Django filters the queryset, returns a rendered HTML partial. Simple.

---

### License

MIT — do whatever you want with it.
