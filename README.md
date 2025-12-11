# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

## Start the FastAPI Calculator Application

- **Without Docker**:

```bash
python main.py
```

The application will start on `http://127.0.0.1:8000`

Open your browser and navigate to `http://127.0.0.1:8000` to use the calculator.

- **With Docker**:

```bash
docker-compose up
```

## Running Tests

This project includes comprehensive test coverage:

### Unit Tests
Test individual arithmetic operations:
```bash
pytest tests/unit/ -v
```

### Integration Tests
Test API endpoints:
```bash
pytest tests/integration/ -v
```

### End-to-End Tests
Test with Playwright browser automation:
```bash
# First install Playwright browsers
playwright install chromium

# Then run e2e tests
pytest tests/e2e/ -v

# Run specific E2E test for user profile
pytest tests/e2e/test_user_profile_e2e.py -v
```

## Frontend Application

The application includes a frontend for user registration and login.

### Accessing the Frontend
1. Start the server:
   ```bash
   python main.py
   ```
2. Open your browser and navigate to:
   - Registration: `http://127.0.0.1:8000/register`
   - Login: `http://127.0.0.1:8000/login`
   - Calculator: `http://127.0.0.1:8000/`

### Features
- **Client-Side Validation**: Forms check for valid email formats and password length.
- **User Profile Management**: Update username, email, and change password.
- **JWT Authentication**: Successful login stores a JWT token for secure access.
- **Responsive Design**: Modern, dark-themed UI.

### Run All Tests
```bash
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=html
```

## Continuous Integration

This project uses GitHub Actions for CI/CD. The workflow automatically runs:
- Unit tests
- Integration tests
- End-to-end tests
- Coverage reports

View the workflow configuration in `.github/workflows/ci.yml`

---

## 🗄️ Database-Backed Tests

Integration tests for the secure user model use a real PostgreSQL database.

### Start Postgres locally

```bash
docker-compose up
```

This starts:
- The FastAPI app on `http://localhost:8000`
- PostgreSQL on `localhost:5432` (DB: `fastapi_db`, user: `postgres`, password: `mypassword`)

### Run database-backed tests

Run all integration tests (including user + calculator API tests):

```bash
pytest tests/integration/ -v
```

Run only the new user-related integration tests:

```bash
pytest tests/integration/test_user_model_db.py -v
pytest tests/integration/test_users_api.py -v
```

Make sure Docker/Postgres is running before executing these tests.

---

## 🐳 Docker Hub Image

A production-ready Docker image for this application is built and pushed
automatically by GitHub Actions when tests pass.

- Docker Hub repository: `jaswanth465/calculator_fastapi`
- Link: https://hub.docker.com/r/jaswanth465/calculator_fastapi

To pull and run the latest image:

```bash
docker pull jaswanth465/calculator_fastapi:latest
docker run -p 8000:8000 jaswanth465/calculator_fastapi:latest
```

Then open `http://localhost:8000` in your browser.

---

## 📝 Reflection (Summary)

See `REFLECTION.md` for a more detailed write-up. Suggested prompts:

- What did you learn about modeling users securely with SQLAlchemy?
- How did Pydantic help with validating and serializing user data?
- What did you learn about password hashing and verification?
- How did GitHub Actions and Docker Hub help automate testing and deployment?
- What challenges did you face, and how did you resolve them?

Use these bullets as a guide when completing your reflection.

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
