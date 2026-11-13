# School Canteen Pre-Order System

A Year 12 Enterprise Computing functional prototype. Students can view a sample canteen menu, submit an order and receive an order number. Staff can log in, view orders, update order statuses and manage menu availability.

## Features

- Student menu with categories and prices
- Quantity selection and automatic total calculation
- Order submission and unique order number
- SQLite database for menu items and orders
- Staff login and order dashboard
- Order status updates
- Add menu items and hide/show menu items
- Responsive layout for computers and phones

## Run the project on your computer

1. Install Python 3.
2. Open Terminal in this project folder.
3. Create and activate a virtual environment:

   **Mac:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**
   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

4. Install the packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the website:
   ```bash
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

The database is created automatically the first time the app runs.

## Demo staff login

- Username: `staff`
- Password: `ChangeMe123!`

This is a demonstration login only. Do not use it for a real school system.

## Upload to GitHub

1. Create a new repository on GitHub, for example `canteen-preorder-system`.
2. Extract this ZIP file.
3. Open the extracted folder in VS Code.
4. Open the VS Code terminal in that folder and run:

   ```bash
   git init
   git add .
   git commit -m "Create canteen pre-order prototype"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/canteen-preorder-system.git
   git push -u origin main
   ```

5. Replace `YOUR-USERNAME` with your GitHub username and use your actual repository URL.

You can also upload the extracted files using GitHub's website, but using Git makes it easier to save later changes.

## Important project notes

- This is a local school-assessment prototype, not a production-ready ordering service.
- It does not process payments, send notifications or connect to a real school database.
- Use fictional student details during testing. Do not enter real student personal information.
- The sample menu and prices are fictional and should be changed if your teacher provides a specific scenario.
- The demo staff login is hard-coded for prototype demonstration. A real system needs secure password storage, HTTPS, stronger session protection, access controls and a privacy/security review.
- The Flask development server is for local testing only, not public deployment.

## Suggested evidence for your assessment

Capture your own screenshots after running the program:
1. Student menu
2. Selected quantities and calculated total
3. Order confirmation with order number
4. Staff login
5. Staff dashboard showing the order
6. Updated order status

Record actual test results and feedback in your development journal. Do not claim a test passed until you have run it.
