# Omilife Backend

Django REST API backend for the Omilife pharmacy website.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start XAMPP MySQL server (port 3306)

3. Run migrations (automatically creates `omilife_db` database):
   ```bash
   python manage.py migrate
   ```

4. Populate products:
   ```bash
   python manage.py populate_products
   ```

5. Run server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /api/products/` - List products with search and category filters
- `GET /api/products/categories/` - Get unique categories
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create new order
- `GET /admin/` - Django admin panel

## Admin Dashboard

Access the admin dashboard at: `http://127.0.0.1:8000/admin/`

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

Use the admin panel to:
- **📦 Manage Products**: Add, edit, delete pharmaceutical products with full details
  - **✏️ Inline Editing**: Edit prices and stock status directly from the list view
  - **🔍 Advanced Search**: Find products by name, ingredients, manufacturer
  - **📊 Filter & Sort**: Filter by category, stock status, manufacturer
- **📋 Manage Orders**: View customer orders, update status, track delivery
  - **⚡ Quick Status Updates**: Change order status directly from the list
  - **🔍 Search Orders**: Find by pharmacy name, contact person, phone
- **🖼️ Product Images**: Manage product image galleries
- **👥 User Management**: Create admin users and manage permissions
- **📊 Recent Actions**: Monitor all system activity and changes

## Frontend Integration

Update the frontend to fetch data from the API:

- Products: Replace hardcoded products array with API calls
- BookingForm: Update submit handler to POST to `/api/orders/`

## Database Switch

Currently using SQLite for development. To switch to MySQL:

1. Start XAMPP MySQL
2. Update settings.py DATABASES section
3. Run migrations again