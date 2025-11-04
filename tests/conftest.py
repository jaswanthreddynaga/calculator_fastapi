# tests/conftest.py

import subprocess
import time
import pytest
import requests
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    # Start FastAPI app using uvicorn for better compatibility
    fastapi_process = subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Define the URL to check if the server is up
    server_url = 'http://127.0.0.1:8000/'
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    print("Starting FastAPI server...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url, timeout=2)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up and running.")
                break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        fastapi_process.wait()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    # Terminate FastAPI server
    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    try:
        fastapi_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        fastapi_process.kill()
    print("FastAPI server has been terminated.")

# Playwright fixtures - only import when needed for e2e tests
try:
    from playwright.sync_api import sync_playwright
    
    @pytest.fixture(scope="session")
    def playwright_instance_fixture():
        """
        Fixture to manage Playwright's lifecycle.
        """
        with sync_playwright() as p:
            yield p
    
    @pytest.fixture(scope="session")
    def browser(playwright_instance_fixture):
        """
        Fixture to launch a browser instance.
        """
        browser = playwright_instance_fixture.chromium.launch(headless=True)
        yield browser
        browser.close()
    
    @pytest.fixture(scope="function")
    def page(browser):
        """
        Fixture to create a new page for each test.
        """
        page = browser.new_page()
        yield page
        page.close()
except ImportError:
    # Playwright not installed, skip these fixtures
    pass
