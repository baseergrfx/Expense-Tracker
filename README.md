# Expense Tracker

A simple and effective Expense Tracker application built with Python and Tkinter. This application allows you to track your daily expenses, view a history of transactions, and manages data persistence using SQLite.

## Features

*   **Add Expenses:** fast and easy entry of Date, Category, Amount, and Description.
*   **View History:** View all your recorded expenses in a clean table format.
*   **Data Persistence:** All data is stored locally in an SQLite database (`expenses.db`), ensuring your data is saved between sessions.
*   **Delete Entries:** Easily remove incorrect entries.
*   **Dynamic Total:** View your total expenses at a glance.

## Tech Stack

*   **Language:** Python
*   **GUI Framework:** Tkinter (Standard Python interface to the Tcl/Tk GUI toolkit)
*   **Database:** SQLite3

## Installation & Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/baseergrfx/Expense-Tracker.git
    cd Expense-Tracker
    ```

2.  **Run the Application:**
    Ensure you have Python installed. Then run:
    ```bash
    python main.py
    ```

## Usage

1.  **Launch the App:** Run the `main.py` script.
2.  **Add an Expense:** Fill in the details in the "Add New Expense" section and click "Add Expense".
3.  **View List:** The new expense will appear in the "Expense History" list below.
4.  **Delete:** Select an item from the list and press the `Delete` key on your keyboard to remove it.

## License

This project is open source.