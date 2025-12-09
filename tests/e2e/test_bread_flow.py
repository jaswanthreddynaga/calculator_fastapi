import pytest
from playwright.sync_api import expect
import time

@pytest.mark.e2e
def test_bread_flow(page, fastapi_server):
    """
    Test the full BREAD flow: Browse, Read, Edit, Add, Delete.
    """
    # 1. Register a new user
    page.goto("http://localhost:8000/register")
    page.fill("#username", "bread_user")
    page.fill("#email", "bread@example.com")
    page.fill("#password", "password123")
    page.fill("#confirmPassword", "password123")
    page.click("button[type='submit']")
    
    # Wait for success message
    expect(page.locator("#successMessage")).to_be_visible()
    
    # 2. Login
    # The registration page redirects to login after 2 seconds, but we can go there directly to speed up
    page.goto("http://localhost:8000/login")
    page.fill("#email", "bread@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    
    # Verify we are on the dashboard
    expect(page.locator("h1")).to_have_text("Calculator Dashboard")
    
    # 3. Add Calculation
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "Add")
    page.click("button:text('Calculate')")
    
    # Verify it appears in the table
    # We might need to wait for the table to populate
    page.wait_for_selector("#calculationsTable tbody tr")
    rows = page.locator("#calculationsTable tbody tr")
    expect(rows).to_have_count(1)
    expect(rows.first.locator("td").nth(1)).to_have_text("10") # A
    expect(rows.first.locator("td").nth(2)).to_have_text("5")  # B
    expect(rows.first.locator("td").nth(3)).to_have_text("Add") # Type
    expect(rows.first.locator("td").nth(4)).to_have_text("15") # Result
    
    # 4. Edit Calculation
    page.click("button.edit")
    
    # Verify form is populated
    expect(page.locator("#a")).to_have_value("10")
    expect(page.locator("#b")).to_have_value("5")
    expect(page.locator("#type")).to_have_value("Add")
    
    # Change values
    page.fill("#a", "20")
    page.select_option("#type", "Multiply")
    page.click("#updateBtn")
    
    # Verify update in table
    # Wait for the update to reflect
    time.sleep(1) # Small delay to ensure UI updates
    rows = page.locator("#calculationsTable tbody tr")
    expect(rows.first.locator("td").nth(1)).to_have_text("20") # A
    expect(rows.first.locator("td").nth(2)).to_have_text("5")  # B
    expect(rows.first.locator("td").nth(3)).to_have_text("Multiply") # Type
    expect(rows.first.locator("td").nth(4)).to_have_text("100") # Result
    
    # 5. Delete Calculation
    # Handle confirm dialog
    page.on("dialog", lambda dialog: dialog.accept())
    page.click("button.delete")
    
    # Verify it's gone
    time.sleep(1)
    rows = page.locator("#calculationsTable tbody tr")
    expect(rows).to_have_count(0)
    
    # 6. Logout
    page.click("button:text('Logout')")
    expect(page).to_have_url("http://localhost:8000/login")
