# Reflection: User & Calculation Routes + Integration Testing

This assignment focused on completing the backend logic by implementing user authentication, calculation management endpoints, and robust integration testing, culminating in a continuous deployment pipeline to Docker Hub.

## 1. User Authentication Implementation

I implemented secure user registration and login endpoints using JWT (JSON Web Tokens).
- **Registration (`POST /users/register`)**: I ensured that passwords are hashed before storage using `passlib` with `pbkdf2_sha256`. This is critical for security so that plain-text passwords are never stored in the database.
- **Login (`POST /users/login`)**: I created an endpoint that verifies provided credentials against the stored hash. If successful, it returns a JWT access token, allowing stateless authentication for subsequent requests.
- **JWT Integration**: I used `python-jose` to generate and verify tokens, ensuring that the backend can securely identify authenticated users.

## 2. Frontend Implementation

I created a user-friendly frontend for registration and login.
- **Design**: I used a modern, dark-themed design with "Rich Aesthetics" to provide a premium user experience.
- **Client-Side Validation**: I implemented JavaScript validation to check email formats and password lengths before sending data to the server, improving feedback loops for the user.
- **Integration**: The frontend communicates with the backend APIs via `fetch`, handling success and error states gracefully.

## 3. Calculation BREAD Endpoints

I built the full set of BREAD (Browse, Read, Edit, Add, Delete) operations for the `Calculation` resource.
- **Design**: I used Pydantic schemas (`CalculationCreate`, `CalculationRead`) to validate input and output, ensuring that the API contract is strictly followed.
- **Logic**: The `Add` and `Edit` endpoints automatically compute the result based on the operation type (Add, Subtract, Multiply, Divide) and the operands. This keeps the business logic encapsulated within the API layer.
- **Error Handling**: I implemented checks for division by zero and 404 errors for non-existent resources, providing clear feedback to API consumers.

## 4. Integration and E2E Testing Strategy

A major part of this assignment was ensuring correctness through integration and End-to-End (E2E) tests.
- **Database Isolation**: I used a separate SQLite database for testing to avoid polluting the development database.
- **Playwright E2E Tests**: I implemented E2E tests using Playwright to simulate real user interactions.
    - **Positive Tests**: Verified successful registration and login flows.
    - **Negative Tests**: Verified error handling for invalid inputs (e.g., short passwords, wrong credentials).
- **CI/CD Integration**: These tests run automatically in GitHub Actions, ensuring that no broken code is deployed.

## 5. CI/CD and Docker Hub

I configured the GitHub Actions workflow to automate the deployment process.
- **Automated Testing**: Every commit triggers the test suite, including unit, integration, and E2E tests.
- **Continuous Deployment**: Upon successful testing, the workflow builds a production-ready Docker image and pushes it to Docker Hub (`jaswanth465/calculator_fastapi`). This ensures that the latest working version is always available for deployment.

## 6. Challenges and Solutions

- **Database Connections in Tests**: I initially faced issues with database connections persisting between tests. I solved this by using `pytest` fixtures to create and drop tables for each test module, ensuring a clean state.
- **Frontend-Backend Integration**: Ensuring the frontend correctly handled JWT tokens and redirected users required careful coordination between the client-side JavaScript and backend responses.
- **E2E Testing with Auth**: Testing authenticated routes required simulating the login process and managing tokens within the test environment, which I achieved using Playwright's browser context.

Overall, this module solidified my understanding of building secure, testable, and deployable REST APIs with FastAPI, along with a modern frontend and robust CI/CD pipeline.
