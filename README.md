# Project
This is a backend learning project in Django. There is an associated frontend project [GitHub Page](https://github.com/AlexLeitermann/kanban_frontend). The frontend is currently hosted at: (https://link.leitermann.online/)

# Install
This guide explains how to set up the `kanban_backend` Django project locally using Visual Studio Code on Windows. Python must already be installed on your system.

## 1. Prerequisites
**Python:** Ensure Python is installed and added to your system's PATH. Verify with:
```
python --version
```
**Git:** Install Git if it's not already installed. Download it [here](https://git-scm.com/downloads).
**VS Code:** Install Visual Studio Code from [here](https://code.visualstudio.com/).

## 2. Clone the Repository
    1. Open Command Prompt or PowerShell.
    2. Navigate to the directory where you want to store the project:
```
cd path\to\your\directory
```
    3. Clone the repository:
```
git clone https://github.com/AlexLeitermann/kanban_backend.git
```
    4. Navigate into the project directory:
```
cd kanban_backend
```

## 3. Set Up a Virtual Environment
    1. Create a virtual environment:
```
python -m venv env
```
    This will create a folder named `env` in the project directory.

    2. Activate the virtual environment:
```
env\Scripts\activate
```
    3. Confirm that the virtual environment is active. The command prompt should display `(env)`.

## 4. Install Dependencies
Install the required packages listed in `requirements.txt`:
```
pip install -r requirements.txt
```

## 5. Configure VS Code
    1. Open the project in VS Code:
```
code .
```
    2. Ensure the Python extension is installed. Open the Extensions view (Ctrl+Shift+X) and search for `Python`.
    3. Select the Python interpreter for the virtual environment:
       - Press `Ctrl+Shift+P` to open the Command Palette.
       - Search for `Python: Select Interpreter`.
       - Choose the interpreter with `env` in its path (e.g., `...\kanban_backend\env\Scripts\python.exe`).

## 6. Run the Project
    1. Apply database migrations:
```
python manage.py migrate
```
    2. Start the development server:
```
python manage.py runserver
```
    3. Open your browser and navigate to `http://127.0.0.1:8000/` to verify that the server is running.

## 7. Deactivating the Virtual Environment
After you're done, deactivate the virtual environment:
```
deactivate
```

