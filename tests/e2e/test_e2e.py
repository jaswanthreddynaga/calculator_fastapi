# tests/e2e/test_e2e.py

import pytest
from playwright.sync_api import expect

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage redirects to login or displays dashboard if logged in.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # It should redirect to login if not authenticated
    if "login" in page.url:
        expect(page.locator("h1")).to_have_text("Login")
    else:
        # If somehow authenticated (shouldn't be in fresh context), it shows dashboard
        expect(page.locator('h1')).to_have_text('Calculator Dashboard')

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.
    """
    # Register and Login first
    page.goto("http://localhost:8000/register")
    page.fill("#username", "calc_add_user")
    page.fill("#email", "add@example.com")
    page.fill("#password", "password123")
    page.fill("#confirmPassword", "password123")
    page.click("button[type='submit']")
    expect(page.locator("#successMessage")).to_be_visible()
    
    page.goto("http://localhost:8000/login")
    page.fill("#email", "add@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    expect(page.locator("h1")).to_have_text("Calculator Dashboard")

    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '5'.
    page.fill('#b', '5')
    
    # Select Add operation (default, but good to be explicit if needed, though default is Add)
    # page.select_option("#type", "Add")

    # Click the button that has the exact text "Calculate".
    page.click('#calculateBtn')
    
    # Use an assertion to check that the result appears in the table
    # The previous test checked a #result div, but the new UI uses a table.
    # We need to check the table.
    page.wait_for_selector("#calculationsTable tbody tr")
    rows = page.locator("#calculationsTable tbody tr")
    expect(rows.first.locator("td").nth(4)).to_have_text("15")

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test the divide by zero functionality of the calculator.
    """
    # Register and Login first
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.goto("http://localhost:8000/register")
    page.fill("#username", "calc_div_user")
    page.fill("#email", "div@example.com")
    page.fill("#password", "password123")
    page.fill("#confirmPassword", "password123")
    page.click("button[type='submit']")
    expect(page.locator("#successMessage")).to_be_visible()
    
    page.goto("http://localhost:8000/login")
    page.fill("#email", "div@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    expect(page.locator("h1")).to_have_text("Calculator Dashboard")

    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')
    
    # Select Divide operation
    page.select_option("#type", "Divide")

    # Click the button that has the exact text "Calculate".
    page.click('#calculateBtn')
    
    # Use an assertion to check that the error message is displayed
    # The new UI displays error in #message div
    expect(page.locator('#message')).to_contain_text('Error: Cannot divide by zero')
