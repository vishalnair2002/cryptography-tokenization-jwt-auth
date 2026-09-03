# Cryptography Analysis: Token-Based Authentication (Tokenization)

## Overview
This project analyses **tokenization** as a next-generation cryptographic
technique for protecting user credentials and session data, completed as
part of the Applied Cryptography & Trust module of my MSc. It implements
a JWT (JSON Web Token) based authentication system in Flask to
demonstrate the core security properties of token-based auth: short-lived
access tokens, refresh tokens, and token revocation.

[FILL IN: 1-2 sentences on your written analysis — e.g. how token-based
auth compares to session-based auth, or what security trade-offs you
evaluated in your write-up.]

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
[FILL IN: 1-3 bullet points from your written analysis — e.g. how short
token lifetimes limit the damage of a stolen token, or why refresh tokens
let you balance security against user convenience.]

## Security note
An earlier version of this app hardcoded its signing secret directly in
the source file. This has since been [FILL IN once fixed: "moved to an
environment variable"] — a hardcoded secret is a common real-world
vulnerability and worth calling out explicitly here.

## Tech
Python, Flask, PyJWT, bcrypt
