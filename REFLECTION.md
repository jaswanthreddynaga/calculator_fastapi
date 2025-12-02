# Reflection: User & Calculation Routes + Integration Testing

This assignment focused on completing the backend logic by implementing user authentication, calculation management endpoints, and robust integration testing, culminating in a continuous deployment pipeline to Docker Hub.

## 1. User Authentication Implementation

I implemented secure user registration and login endpoints.
- **Registration (`POST /users/register`)**: I ensured that passwords are hashed before storage using `passlib` with `pbkdf2_sha256`. This is critical for security so that plain-text passwords are never stored in the database.
- **Login (`POST /users/login`)**: I created an endpoint that verifies provided credentials against the stored hash. If successful, it returns the user ID, laying the groundwork for session management.

## 2. Calculation BREAD Endpoints

I built the full set of BREAD (Browse, Read, Edit, Add, Delete) operations for the `Calculation` resource.
- **Design**: I used Pydantic schemas (`CalculationCreate`, `CalculationRead`) to validate input and output, ensuring that the API contract is strictly followed.
- **Logic**: The `Add` and `Edit` endpoints automatically compute the result based on the operation type (Add, Subtract, Multiply, Divide) and the operands. This keeps the business logic encapsulated within the API layer.
- **Error Handling**: I implemented checks for division by zero and 404 errors for non-existent resources, providing clear feedback to API consumers.

## 3. Integration Testing Strategy

A major part of this assignment was ensuring correctness through integration tests.
- **Database Isolation**: I used a separate SQLite database for testing to avoid polluting the development database.
- **Test Coverage**:
    - `test_user_routes.py`: Verifies that users can register and login, and that duplicate emails/usernames are rejected.
    - `test_calculation_routes.py`: Tests the entire lifecycle of a calculation. It ensures that a user can create a calculation, retrieve it, update it, and delete it.
- **CI/CD Integration**: These tests run automatically in GitHub Actions, ensuring that no broken code is deployed.

## 4. CI/CD and Docker Hub

I configured the GitHub Actions workflow to automate the deployment process.
- **Automated Testing**: Every commit triggers the test suite.
- **Continuous Deployment**: Upon successful testing, the workflow builds a production-ready Docker image and pushes it to Docker Hub (`jaswanth465/calculator_fastapi`). This ensures that the latest working version is always available for deployment.

## 5. Challenges and Solutions

- **Database Connections in Tests**: I initially faced issues with database connections persisting between tests. I solved this by using `pytest` fixtures to create and drop tables for each test module, ensuring a clean state.
- **Async Database Events**: I updated `main.py` to use the `lifespan` context manager for database initialization. This prevented race conditions where tests might try to access the DB before tables were created.

Overall, this module solidified my understanding of building secure, testable, and deployable REST APIs with FastAPI.
