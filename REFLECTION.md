# Reflection

This assignment took my simple FastAPI calculator project and turned it into
a more realistic web application with a database, secure user handling,
automated tests, and a full CI/CD pipeline. Working through each piece helped
me connect concepts from Python, databases, security, testing, and DevOps.

## 1. Secure User Model and Database

I learned how to design a `User` table with SQLAlchemy instead of just working
with in-memory data. Defining the `User` model with fields like `id`,
`username`, `email`, `password_hash`, and `created_at` made me think about how
data should be stored long term. I added uniqueness constraints on the
`username` and `email` columns so that the database itself enforces that no two
users can share the same identifier.

To verify that the model behaved correctly, I wrote integration tests that use
an actual PostgreSQL database. These tests create users, check that the
`created_at` timestamp is automatically set, and confirm that trying to insert
a second user with the same username triggers an integrity error. Using a real
database in tests gave me confidence that my application code and schema match
what the database actually does, not just what I expect in theory.

## 2. Pydantic Validation and Schemas

Pydantic played a big role in validating and serializing user data. I created
`UserCreate` and `UserRead` schemas so that request and response bodies are
clearly defined. Using `EmailStr` for the `email` field gave me built-in
validation for email addresses instead of having to write custom regex logic.

During development, I ran into validation errors when the `email-validator`
dependency was missing, which caused tests to fail. Fixing this by adding the
missing package and seeing Pydantic immediately enforce correct email formats
showed me how nice it is to have strict models at the API boundary. Overall,
Pydantic helped keep the shapes of my data consistent across the database
models, request bodies, and responses.

## 3. Password Hashing and Security

Before this assignment, it was easy to think of passwords as just strings. Here
I had to store them safely using a one-way hash instead of saving plain-text
values. I used `passlib` with a strong hashing scheme (`pbkdf2_sha256`) and
created helper functions to hash a password before inserting it into the
database and to verify a plain-text password against a stored hash.

Writing unit tests around these helpers helped confirm that hashing and
verification behaved as expected: the hash is different from the raw password,
the correct password verifies successfully, and a wrong password fails. This
reinforced why storing plain-text passwords is dangerous. If the database were
ever exposed, attackers would still have to break the hashes instead of reading
passwords directly.

## 4. Testing Strategy (Unit + Integration + E2E)

I ended up with three layers of tests. Unit tests focus on small pieces of
logic like arithmetic operations, password hashing, and Pydantic schema
validation. These are fast and give quick feedback when I change code.

Integration tests check how components work together. For example, they verify
that the FastAPI `/users` endpoints talk to the database correctly and that the
SQLAlchemy model constraints actually behave as intended. They also cover the
existing calculator API endpoints. End-to-end tests, using Playwright, drive
the browser UI and make sure the full stack (frontend + backend) behaves like a
user expects. The new database-backed tests, in particular, catch issues like
missing constraints, incorrect database URLs, or mismatch between schemas and
models that unit tests alone would not see.

## 5. CI/CD with GitHub Actions and Docker Hub

Configuring GitHub Actions turned this project into a more realistic CI/CD
pipeline. On every push or pull request, the workflow sets up Python, installs
dependencies, and runs unit, integration, and end-to-end tests. I also added a
PostgreSQL service to the workflow so that the same database-backed tests that
run locally also run in CI.

After the tests pass, a second job builds a Docker image for the application
and pushes it to Docker Hub under `jaswanth465/calculator_fastapi`. This means
there is always a fresh, tested image available that I can pull and run with a
single Docker command. Having this automated CI/CD pipeline reduces manual
steps, makes it easier to catch regressions early, and provides a clear,
repeatable path from code to a running container.

## 6. Challenges and Lessons Learned

One of the main challenges was getting all of the moving parts to work
together: FastAPI, SQLAlchemy, Pydantic v2, Postgres, passlib, and GitHub
Actions. I ran into dependency issues (like missing `email-validator` and
bcrypt backend warnings) that caused tests to fail unexpectedly. I also had to
debug database connection problems when Postgres was not running locally or not
configured correctly in CI.

I solved these issues by reading error messages carefully, checking the
documentation for each library, and adjusting configurations step by step. For
example, switching to a more reliable hashing scheme and aligning test
expectations with my custom error handlers made the tests stable. If I had more
time, I would add more thorough authentication and authorization flows,
introduce environment-specific settings for production, and expand the test
suite with more edge cases. Overall, this assignment gave me hands-on practice
with building a small but realistic backend service and automating its testing
and deployment.
