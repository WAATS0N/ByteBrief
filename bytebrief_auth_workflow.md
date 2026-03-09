# ByteBrief Authentication Workflow Guide

This document explains a **real-world authentication system** for a web
platform that supports:

-   Email + Password Login
-   Google OAuth Login
-   Account Registration
-   Secure Password Storage
-   Password Reset
-   Session Handling

The goal is to provide a **production-style authentication
architecture**.

------------------------------------------------------------------------

# 1. System Architecture

Frontend communicates with a backend API which handles authentication
logic.

    Frontend (Next.js / React)
            |
            | HTTPS Requests
            v
    Backend API (Node.js / Express)
            |
            |-- Auth Controller
            |-- Password Hashing (bcrypt)
            |-- JWT / Session Manager
            v
    Database (PostgreSQL / MySQL)
            |
            └── Users Table

Optional services:

    Google OAuth Server
    Email Service (for verification / reset)
    Redis (session cache)

------------------------------------------------------------------------

# 2. Database Structure

## Users Table

    users
    -------------------------------------
    id (UUID / INT)
    name
    email (UNIQUE)
    password_hash
    auth_provider
    google_id
    email_verified
    profile_picture
    created_at
    updated_at

Example:

  id   email            password_hash   auth_provider
  ---- ---------------- --------------- ---------------
  1    user@mail.com    bcrypt hash     local
  2    user@gmail.com   NULL            google

`auth_provider` indicates how the user authenticated.

Values: - local - google

------------------------------------------------------------------------

# 3. Account Creation Workflow

### Step 1 -- User enters details

    name
    email
    password

### Step 2 -- Frontend request

    POST /api/auth/signup

### Step 3 -- Backend validation

-   Validate email format
-   Check password strength
-   Check if email already exists

### Step 4 -- Password hashing

Use bcrypt.

    password_hash = bcrypt(password)

### Step 5 -- Store user

    INSERT INTO users
    (name,email,password_hash,auth_provider)
    VALUES
    ("John","john@mail.com","hashed","local")

### Step 6 -- Optional email verification

Send verification link to user.

### Step 7 -- Create authentication token

Return JWT token.

------------------------------------------------------------------------

# 4. Email Login Workflow

### Step 1 -- User enters

    email
    password

### Step 2 -- API request

    POST /api/auth/login

### Step 3 -- Fetch user

    SELECT * FROM users WHERE email=?

### Step 4 -- Compare password

    bcrypt.compare(password, password_hash)

### Step 5 -- Generate session

Create:

-   Access Token
-   Refresh Token

Example response:

    {
     access_token,
     refresh_token,
     user
    }

------------------------------------------------------------------------

# 5. Google OAuth Login Workflow

### Step 1

User clicks **Continue with Google**.

### Step 2

Frontend redirects to Google OAuth.

### Step 3

User approves permissions.

### Step 4

Google returns:

    ID Token
    Email
    Google ID
    Profile Picture

### Step 5

Backend verifies token using Google API.

### Step 6

Check database.

If user exists → Login

If user does not exist → Create account

    INSERT INTO users
    (email,google_id,auth_provider)
    VALUES
    ("user@gmail.com","google-id","google")

### Step 7

Generate JWT session token.

------------------------------------------------------------------------

# 6. Password Storage Security

Passwords must never be stored as plain text.

Recommended hashing algorithms:

-   bcrypt
-   argon2
-   scrypt

Example hash:

    $2b$12$T8D9rK3QYk9n....

Properties:

-   One-way encryption
-   Salted hashes
-   Resistant to brute force

------------------------------------------------------------------------

# 7. Session Management

Two common approaches.

## JWT Authentication

    Access Token (15 minutes)
    Refresh Token (7 days)

Flow:

    Login → issue tokens
    Access token expires → use refresh token

## Cookie Sessions

Backend stores session in:

-   Redis
-   Database

Browser stores:

    session_id cookie

------------------------------------------------------------------------

# 8. Password Reset Workflow

### Step 1

User clicks **Forgot Password**.

### Step 2

Backend generates reset token.

### Step 3

Send email with link.

Example:

    /reset-password?token=abc123

### Step 4

User sets new password.

Backend verifies token and updates password.

------------------------------------------------------------------------

# 9. API Endpoints

    POST /api/auth/signup
    POST /api/auth/login
    POST /api/auth/google
    POST /api/auth/logout
    POST /api/auth/refresh

    POST /api/auth/forgot-password
    POST /api/auth/reset-password

    GET /api/auth/me

------------------------------------------------------------------------

# 10. Security Best Practices

Always implement:

-   HTTPS
-   Password hashing
-   Rate limiting
-   Email verification
-   CSRF protection
-   Token expiration
-   OAuth token verification

Optional improvements:

-   Two-factor authentication
-   Device tracking
-   Login alerts

------------------------------------------------------------------------

# 11. Implementation Instructions

## Step 1 -- Setup Backend

Install dependencies:

    npm init -y

    npm install express cors dotenv bcrypt jsonwebtoken mysql2
    npm install passport passport-google-oauth20

Create project structure:

    backend
    │
    ├── controllers
    │   └── authController.js
    │
    ├── routes
    │   └── authRoutes.js
    │
    ├── middleware
    │   └── authMiddleware.js
    │
    ├── config
    │   └── googleAuth.js
    │
    ├── models
    │   └── userModel.js
    │
    └── server.js

------------------------------------------------------------------------

## Step 2 -- Setup Database

Create users table.

Example (MySQL):

    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password_hash TEXT,
    google_id VARCHAR(255),
    auth_provider VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

------------------------------------------------------------------------

## Step 3 -- Setup Google OAuth

1.  Go to Google Cloud Console
2.  Create project
3.  Enable Google OAuth API
4.  Create OAuth Client ID
5.  Add redirect URL

Example:

    http://localhost:5000/auth/google/callback

Store credentials in `.env`

    GOOGLE_CLIENT_ID=xxxx
    GOOGLE_CLIENT_SECRET=xxxx
    JWT_SECRET=xxxx

------------------------------------------------------------------------

## Step 4 -- Connect Frontend

Frontend calls backend APIs.

Examples:

Signup:

    POST /api/auth/signup

Login:

    POST /api/auth/login

Google login:

    /auth/google

------------------------------------------------------------------------

# 12. Recommended Stack for ByteBrief

    Frontend  → Next.js
    Backend   → Node.js + Express
    Database  → PostgreSQL / MySQL
    Auth      → JWT
    OAuth     → Google OAuth
    Password  → bcrypt
    Session   → HTTP-only cookies

------------------------------------------------------------------------

# End of Document
