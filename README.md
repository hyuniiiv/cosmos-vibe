# JWT Auth - Universe beta (RS256 / RSA-SHA256)

A working JWT authentication API built with Express 4, `jsonwebtoken`, and `bcrypt`.

**Strategy:** RS256 asymmetric signing - the private key signs tokens, the public key verifies them. The public key can be shared safely (e.g., with downstream services); the private key stays server-side only.

## Quick Start

```bash
npm install
npm start
# Server listens on http://127.0.0.1:3000
```

Keys are **auto-generated** on first startup (`keys/private.pem`, `keys/public.pem`). They are gitignored by `keys/.gitignore`.

## Routes

| Method | Path           | Auth required | Description                   |
|--------|----------------|:-------------:|-------------------------------|
| GET    | /health        | No            | Liveness check                |
| POST   | /auth/register | No            | Create account; returns token |
| POST   | /auth/login    | No            | Authenticate; returns token   |
| GET    | /me            | Yes           | Return current user from JWT  |

## Usage Examples

### Register

```bash
curl -s -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"correct-horse-battery"}'
```

Response 201:
```json
{
  "data": {
    "token": "<jwt>",
    "user": { "id": "1", "email": "alice@example.com", "createdAt": "..." }
  }
}
```

### Login

```bash
curl -s -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"correct-horse-battery"}'
```

### Protected Route

```bash
TOKEN="<paste token here>"
curl -s http://localhost:3000/me \
  -H "Authorization: Bearer $TOKEN"
```

Response 200:
```json
{
  "data": {
    "id": "1",
    "email": "alice@example.com",
    "tokenIssuedAt": "2026-05-12T01:00:00.000Z",
    "tokenExpiresAt": "2026-05-12T01:15:00.000Z"
  }
}
```

## Design Decisions

### RSA Key Size: 2048-bit

Chose 2048-bit over 4096-bit. 4096-bit roughly doubles signing latency (~2ms vs ~1ms) with negligible security gain for 15-minute JWT lifetimes. NIST approves 2048-bit RSA through at least 2030.

### Token Expiry: 15 minutes

Short-lived tokens limit blast radius if a token is stolen. Refresh tokens are out of scope for this demo; a production system should add them.

### bcrypt Rounds: 10

Industry standard, aligned with NIST SP 800-63b. Approximately 100ms on modern hardware - secure without making demo interactions sluggish.

### JWT Payload

```json
{
  "sub": "<userId>",
  "email": "alice@example.com",
  "iss": "cosmos-beta",
  "aud": "cosmos-beta-api",
  "iat": 1747008000,
  "exp": 1747008900
}
```

- `sub` is the stable user identifier
- `email` included for convenience - avoids an extra DB lookup in most flows
- `iss` / `aud` verified on every request (defense in depth, free with jsonwebtoken)
- `kid` header derived from SHA-256 of public key for future key rotation support

### Error Response Format

All errors use a consistent shape to eliminate client-side branching:

```json
{ "error": { "code": "INVALID_CREDENTIALS", "message": "..." } }
```

All successes wrap payloads in `data`:

```json
{ "data": { ... } }
```

HTTP status codes: 400 validation, 401 auth failures, 409 email conflict, 500 internal.

### Anti-Enumeration

The login route runs bcrypt even when the email does not exist, preventing timing-based user discovery.

## File Structure

```
keys/
  .gitignore      - *.pem (keys never committed)
  private.pem     - generated on first run (RS256 private key)
  public.pem      - generated on first run (RS256 public key)
src/
  app.js          - Express app + routes
  auth.js         - Key management + JWT sign/verify + bcrypt
  middleware.js   - Bearer token extraction + verification
package.json
```

## Production Notes

- **User store:** In-memory Map - intentionally simple for the demo. Swap in PostgreSQL/MongoDB by replacing the users Map operations in app.js.
- **Key rotation:** The `kid` header is already embedded in every token. On rotation, keep the old public key available until existing tokens expire (max 15 min).
- **HTTPS:** Required in production. RS256 does not encrypt the payload; it only signs it.
- **Refresh tokens:** Add a /auth/refresh route with a longer-lived, single-use token stored in a database. Consider refresh token rotation with family-based theft detection (see Universe gamma's approach).
- **bcrypt rounds:** This demo uses 10 (NIST baseline, ~100ms). For production security-first deployments, consider 12 (~250ms) - the additional latency is acceptable for normal login volume.
- **Helmet:** Add the `helmet` npm package to set HTTP security headers (HSTS, X-Frame-Options, CSP, etc.) before exposing to web clients.
