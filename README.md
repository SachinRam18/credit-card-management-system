# Credit Card Management System

A simple web application for managing your credit cards, featuring secure user authentication (Login/Register), card addition, listing, deletion, searching, and a dashboard summary limit calculator. This project uses a **Flask (Python)** backend and a pure HTML/CSS/JS frontend, powered by an **SQLite3** database.

## Prerequisites

Make sure you have the following installed on your machine:
- **Python 3.x**
- **Git** (optional, if cloning via terminal)

## Instructions: From Cloning to Running Locally

Follow these step-by-step instructions to get the application running on your local machine.

### 1. Clone the Repository
Open your terminal (or Command Prompt / PowerShell) and run:
```bash
git clone https://github.com/yourusername/credit_card_management.git
cd credit_card_management
```
*(If you have downloaded the source code as a ZIP file, simply extract the ZIP and open its folder in your terminal).*

### 2. Create a Virtual Environment (Recommended but optional)
It is always a good practice to use a virtual environment to manage dependencies securely without interfering with system-wide python packages.
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Dependencies
Install all the required Python libraries (Flask and Werkzeug) found in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask development server by running:
```bash
python app.py
```
*Note: The script automatically initializes the database (`cards.db`) with `cards` and `users` tables if they don't already exist.*

### 5. Open the Application
Once the server is running, you should see output indicating that it is listening on port `3000`. 
Open your favorite web browser and navigate to:
**http://127.0.0.1:3000** or **http://localhost:3000**

### 6. Using The App
1. **Register**: Click on the **Register** link on the login page to create a new user account. Fill in a username and password.
2. **Login**: Go back to the login page and sign in with the newly created credentials.
3. **Manage Cards**: You can now perform CRUD operations (Add, Delete), Search through your mapped cards, and see your cumulative total cards limit.

## Technologies Used
- **Backend:** Python, Flask, Werkzeug (for hashing passwords), SQLite3
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

## Database
An SQLite file named `cards.db` will automatically generate in your project root upon first startup and hold the locally stored data securely.

## License
MIT License
