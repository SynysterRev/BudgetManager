# Budget Manager – Django Project

**Budget Manager** is a Django-based web application designed to help users manage their personal finances with ease. It allows users to securely create an account, track income and expenses, organize transactions by category, and export their financial data.

---

## Features

### Currently Available

- **User Authentication**: Secure sign up and login.
- **Category Management**: Create custom categories for transactions.
- **Transaction Management**: Add income and expense transactions linked to specific categories.
- **Filtering System**: Filter transactions by:
  - Date
  - Type (income or expense)
  - Category
  - Keyword search
- **Results Summary**:
  - Total number of matching transactions
  - Displayed balance (total of filtered transactions)
- **User Profile Editing**: Update name and email.
- **CSV Export**: Export displayed transactions as a CSV file.

---

## Upcoming Features

- **Password Change**
- **Account Deletion**
- **Dashboard Statistics**:
  - Total number of transactions
  - Number of categories
  - Account creation date
- **Dashboard Overview**:
  - Most recent transactions
  - Current month balance, income, and expenses
- **Data Visualization (if achievable)**:
  - Line chart showing income and expenses over several months
  - Pie chart of income/expense distribution per category for the current month
- **Responsive Design**: Improve layout and usability on mobile and tablet devices

---

## Tech Stack

- Python
- Django
- HTML / CSS (Django templates)
- Tailwind
- JavaScript (optional for interactivity and future charts)
- SQLite (for local development)
- PostgreSQL (for production)

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/budget-manager.git
   cd budget-manager
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` in your browser.

---

## License

This project is licensed under the MIT License.
