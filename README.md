# Oye Abbayi - Fresh from Farmers 🚜🌾

Welcome to **Oye Abbayi**, a premium e-commerce platform dedicated to bringing fresh, organic produce directly from local village farmers to your doorstep.

## 🌟 Key Features
- **Farmer-Centric UI**: A modern, clean, and intuitive design inspired by rural harvest.
- **Dynamic Categories**: Fruits, Vegetables, Dairy, and Groceries with custom icons.
- **Advanced Cart System**: Seamlessly add products with quantity selection and stock validation.
- **Branded Admin Panel**: Customized Django admin for easy inventory and order management.
- **PDF Bill Generation**: Download professional, branded receipts for every order.
- **Secure Checkout**: Streamlined ordering process with clear status updates.

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Frontend**: Bootstrap 5, FontAwesome 6, Google Fonts (Outfit)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **PDF Engine**: ReportLab

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Modern Browser

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/subrahmanyamkondeti773-sketch/oye_abbayi.git
   cd oye_abbayi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

5. Seed Initial Data (Oye Abbayi Branding):
   ```bash
   python manage.py seed_oye_abbayi
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

---
Developed with ❤️ for local farmers.
