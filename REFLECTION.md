# Reflection

Use this document to briefly describe your experience building and deploying
this FastAPI application.

## 1. Secure User Model and Database
- What did you learn about designing a `User` table with SQLAlchemy?
- How did you enforce uniqueness on `username` and `email`?
- How did you verify that data was stored correctly using integration tests?

## 2. Pydantic Validation and Schemas
- How did Pydantic (especially `EmailStr` and response models) help you
  validate and serialize user data?
- Were there any validation errors you had to debug and fix?

## 3. Password Hashing and Security
- What did you learn about hashing passwords with `passlib` and `bcrypt`?
- How did you verify that hashes work correctly (unit tests, manual checks)?
- Why is it important **not** to store plain-text passwords?

## 4. Testing Strategy (Unit + Integration + E2E)
- How did you split responsibilities between unit tests, integration tests,
  and end-to-end tests?
- What did the new database-backed tests help you catch that unit tests
  alone would not?

## 5. CI/CD with GitHub Actions and Docker Hub
- How did you configure GitHub Actions to run tests automatically?
- How does the workflow build and push your Docker image to Docker Hub?
- What benefits do you see from having an automated CI/CD pipeline?

## 6. Challenges and Lessons Learned
- What were the main challenges you faced during this assignment?
- How did you debug and solve those issues?
- If you had more time, what improvements would you make?

Write a short paragraph or two under each heading. Aim for clear,
concise reflections that show what you learned and how you approached
problems.
