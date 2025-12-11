import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_user_profile_flow(page: Page, fastapi_server):
    
    # 1. Register and Login
    page.goto("http://127.0.0.1:8000/register")
    page.fill("#username", "e2e_profile_user")
    page.fill("#email", "e2e_profile@example.com")
    page.fill("#password", "password123")
    page.fill("#confirmPassword", "password123")
    page.click("button[type='submit']")
    expect(page.locator("#successMessage")).to_have_text("Registration successful! Redirecting...")

    # Manually go to login to avoid flaky redirect wait
    page.goto("http://127.0.0.1:8000/login")
    page.fill("#email", "e2e_profile@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    
    # Wait for navigation to dashboard
    try:
        page.wait_for_url("http://127.0.0.1:8000/", timeout=10000)
    except Exception:
        # Check if we are on dashboard but URL is different (e.g. trailing slash)
        if page.title() != "Calculator Dashboard":
            raise

    expect(page).to_have_title("Calculator Dashboard")

    # 2. Open Profile
    page.click("button:text-is('Profile')")
    expect(page.locator("#profileSection")).to_be_visible()
    
    # Check token exists
    token = page.evaluate("localStorage.getItem('access_token')")
    assert token, "Token is missing from localStorage"
    
    # Verify pre-filled data
    expect(page.locator("#profileUsername")).to_have_value("e2e_profile_user")
    expect(page.locator("#profileEmail")).to_have_value("e2e_profile@example.com")

    # 3. Update Profile
    page.fill("#profileUsername", "updated_user")
    page.click("button:text-is('Update Profile')")
    expect(page.locator("#profileMessage")).to_have_text("Profile updated successfully!")
    expect(page.locator("#userInfo")).to_have_text("Logged in as: updated_user")

    # 4. Change Password
    page.fill("#currentPassword", "password123")
    page.fill("#newPassword", "newpassword456")
    page.click("button:text-is('Change Password')")
    expect(page.locator("#profileMessage")).to_have_text("Password changed successfully!")

    # 5. Logout and Login with new password
    page.click("button:text-is('Logout')")
    expect(page).to_have_title("Login - Calculator App")

    page.fill("#email", "e2e_profile@example.com") # Email didn't change
    page.fill("#password", "newpassword456")
    page.click("button[type='submit']")
    expect(page).to_have_title("Calculator Dashboard")
    expect(page.locator("#userInfo")).to_have_text("Logged in as: updated_user")
