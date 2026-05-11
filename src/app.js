'use strict';

/**
 * app.js — Express application entry point
 *
 * Routes:
 *   POST /auth/register  — create a new user account
 *   POST /auth/login     — authenticate and receive a JWT
 *   GET  /me             — protected route; returns current user info
 *   GET  /health         — liveness check (unprotected)
 *
 * User store: in-memory Map (keyed by email).
 * This is intentionally simple — not production-ready persistence.
 * See README.md for notes on swapping in a real database.
 *
 * Error response shape (consistent throughout):
 *   { error: { code: string, message: string } }
 *
 * Success response shape:
 *   { data: <payload> }
 */

require('dotenv').config();

const express = require('express');
const { initKeys, signToken, hashPassword, verifyPassword } = require('./auth');
const { authenticate } = require('./middleware');

// ── Key Initialization ────────────────────────────────────────────────────────
// Keys are loaded (or generated) synchronously before the server starts.
// This ensures no request can arrive before signing/verification is ready.
initKeys();

// ── In-Memory User Store ──────────────────────────────────────────────────────
// Maps email → { id, email, passwordHash, createdAt }
const users = new Map();

/**
 * Generate a simple unique ID.
 * In production, use a UUID library or database-generated ID.
 */
let nextId = 1;
function generateId() {
  return String(nextId++);
}

// ── Express App ───────────────────────────────────────────────────────────────
const app = express();
app.use(express.json());

// ── Input Validation Helpers ──────────────────────────────────────────────────

/**
 * Validate that email is a plausible address and password meets
 * minimum requirements. Returns an array of error messages (empty = valid).
 */
function validateCredentials(email, password) {
  const errors = [];

  if (!email || typeof email !== 'string') {
    errors.push('email is required.');
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
    errors.push('email must be a valid email address.');
  }

  if (!password || typeof password !== 'string') {
    errors.push('password is required.');
  } else if (password.length < 8) {
    errors.push('password must be at least 8 characters.');
  }

  return errors;
}

// ── Routes ────────────────────────────────────────────────────────────────────

/**
 * GET /health
 * Simple liveness probe — returns 200 when the server is up.
 */
app.get('/health', (req, res) => {
  res.json({ data: { status: 'ok', ts: new Date().toISOString() } });
});

/**
 * POST /auth/register
 * Body: { email: string, password: string }
 *
 * Creates a new user. Fails with 409 if the email is already registered.
 * Returns 201 with the user record (no password hash) and a JWT.
 */
app.post('/auth/register', async (req, res) => {
  try {
    const { email: rawEmail, password } = req.body || {};
    const email = typeof rawEmail === 'string' ? rawEmail.trim().toLowerCase() : rawEmail;

    // Validate input
    const validationErrors = validateCredentials(email, password);
    if (validationErrors.length > 0) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: validationErrors.join(' '),
        },
      });
    }

    // Check for duplicate email
    if (users.has(email)) {
      return res.status(409).json({
        error: {
          code: 'EMAIL_ALREADY_EXISTS',
          message: 'An account with this email address already exists.',
        },
      });
    }

    // Hash password and store user
    const passwordHash = await hashPassword(password);
    const user = {
      id: generateId(),
      email,
      passwordHash,
      createdAt: new Date().toISOString(),
    };
    users.set(email, user);

    // Issue token immediately — eliminates a redundant login round-trip
    const token = signToken(user);

    return res.status(201).json({
      data: {
        token,
        user: {
          id: user.id,
          email: user.email,
          createdAt: user.createdAt,
        },
      },
    });
  } catch (err) {
    console.error('[register] Unexpected error:', err);
    return res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred. Please try again.',
      },
    });
  }
});

/**
 * POST /auth/login
 * Body: { email: string, password: string }
 *
 * Authenticates a user. Returns 401 on invalid credentials.
 * Deliberately uses generic error messages (doesn't reveal whether
 * the email exists) to prevent user enumeration attacks.
 */
app.post('/auth/login', async (req, res) => {
  try {
    const { email: rawEmail, password } = req.body || {};
    const email = typeof rawEmail === 'string' ? rawEmail.trim().toLowerCase() : rawEmail;

    // Validate input shape (not detailed, to avoid enumeration leakage)
    if (!email || !password) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'email and password are required.',
        },
      });
    }

    const user = users.get(email);

    if (!user) {
      // Always run bcrypt even for missing users to prevent timing attacks
      await hashPassword('__dummy_to_prevent_timing_attack__');
      return res.status(401).json({
        error: {
          code: 'INVALID_CREDENTIALS',
          message: 'Invalid email or password.',
        },
      });
    }

    const passwordValid = await verifyPassword(password, user.passwordHash);
    if (!passwordValid) {
      return res.status(401).json({
        error: {
          code: 'INVALID_CREDENTIALS',
          message: 'Invalid email or password.',
        },
      });
    }

    const token = signToken(user);

    return res.json({
      data: {
        token,
        user: {
          id: user.id,
          email: user.email,
          createdAt: user.createdAt,
        },
      },
    });
  } catch (err) {
    console.error('[login] Unexpected error:', err);
    return res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred. Please try again.',
      },
    });
  }
});

/**
 * GET /me  (protected)
 *
 * Returns the current user's information extracted from the JWT.
 * Demonstrates the `authenticate` middleware pattern.
 * In a real app, you'd typically do a DB lookup using req.user.sub.
 */
app.get('/me', authenticate, (req, res) => {
  const { sub: id, email, iat, exp } = req.user;

  return res.json({
    data: {
      id,
      email,
      tokenIssuedAt: new Date(iat * 1000).toISOString(),
      tokenExpiresAt: new Date(exp * 1000).toISOString(),
    },
  });
});

// ── 404 Handler ───────────────────────────────────────────────────────────────

app.use((req, res) => {
  res.status(404).json({
    error: {
      code: 'NOT_FOUND',
      message: `Route ${req.method} ${req.path} not found.`,
    },
  });
});

// ── Error Handler ─────────────────────────────────────────────────────────────

// Catches errors thrown by middleware or route handlers
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, _next) => {
  console.error('[unhandled]', err);
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred.',
    },
  });
});

// ── Server Startup ────────────────────────────────────────────────────────────

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';

app.listen(PORT, HOST, () => {
  console.log(`[server] Listening on http://${HOST}:${PORT}`);
  console.log('[server] Routes: POST /auth/register | POST /auth/login | GET /me | GET /health');
});

module.exports = app; // exported for testing
