# Cryptography Analysis: Token-Based Authentication (Tokenization)

## Overview
This project analyses **tokenization** as a next-generation cryptographic
technique for protecting user credentials and session data, completed as
part of the Applied Cryptography & Trust module of my MSc. It implements
a JWT (JSON Web Token) based authentication system in Flask to
demonstrate the core security properties of token-based auth: short-lived
access tokens, refresh tokens, and token revocation.

The written analysis compares JWTs against alternative approaches (OAuth
2.0, Fernet tokens) and argues JWT sits in the middle ground: lighter
and more scalable than OAuth 2.0's full authorization framework, but
more flexible than Fernet's simple symmetric encryption — which is why
JWT was chosen for this implementation. It also argues tokenization can
replace traditional session-based authentication, since it removes the
server's need to store session state, improving scalability and
resistance to server-side session hijacking.

## What's in this repo
- `app.py` — a Flask API implementing token-based authentication:
  - `/login` — verifies credentials (passwords hashed with bcrypt) and
    issues a short-lived JWT access token (5 min) plus a longer-lived
    refresh token (30 min)
  - `/protected` — a route that only responds if a valid, non-revoked
    Bearer token is supplied
  - `/refresh` — issues a new access token from a valid refresh token
    without requiring the user to log in again
  - `/logout` — revokes a token by adding it to a blacklist
- `requirements.txt` — Python dependencies (Flask, PyJWT, bcrypt)
- Written analysis of tokenization as a cryptographic approach (see the
  included `.docx` write-ups)

## How to run
```bash
pip install -r requirements.txt
python app.py
```
Then POST to `/login` with a username/password to receive tokens, and use
the returned access token as a `Bearer` header to call `/protected`.

## Key findings
- **Stateless auth improves scalability**: embedding user data directly
  in the token removes the need for server-side session storage,
  reducing server load and making the system easier to scale across
  distributed applications.
- **Short-lived access tokens + refresh tokens balance security and UX**:
  short expiry limits the damage of a stolen token, while the refresh
  token avoids forcing the user to log in repeatedly.
- **JWTs have a real revocation weakness**: once issued, a JWT is valid
  until it expires and there is no built-in way to revoke it early —
  this project's token blacklist on logout is a practical mitigation for
  that gap.
- **Implementation quality matters more than the technology choice**:
  weak secret keys, poor validation, and algorithm-confusion attacks are
  the main real-world risks with JWT-based systems, not the JWT
  approach itself.

## Security note
An earlier version of this app hardcoded its signing secret directly in
the source file. This has since been [FILL IN once fixed: "moved to an
environment variable"] — a hardcoded secret is a common real-world
vulnerability and worth calling out explicitly here.

## Tech
Python, Flask, PyJWT, bcrypt
