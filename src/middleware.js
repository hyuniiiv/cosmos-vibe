'use strict';

/**
 * middleware.js — Express authentication middleware
 *
 * Extracts the Bearer token from the Authorization header,
 * verifies it with the RS256 public key, and attaches the
 * decoded payload to req.user.
 *
 * Error responses use the consistent shape:
 *   { error: { code: string, message: string } }
 */

const { verifyToken } = require('./auth');

/**
 * Authenticate middleware.
 *
 * On success: sets req.user = decoded JWT payload and calls next().
 * On failure: returns 401 with a structured error.
 */
function authenticate(req, res, next) {
  const authHeader = req.headers['authorization'];

  if (!authHeader) {
    return res.status(401).json({
      error: {
        code: 'MISSING_TOKEN',
        message: 'Authorization header is required.',
      },
    });
  }

  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0].toLowerCase() !== 'bearer') {
    return res.status(401).json({
      error: {
        code: 'MALFORMED_TOKEN',
        message: 'Authorization header must be in the format: Bearer <token>',
      },
    });
  }

  const token = parts[1];

  try {
    const payload = verifyToken(token);
    req.user = payload;
    next();
  } catch (err) {
    // Distinguish between expired tokens and other invalid tokens
    // so clients can act appropriately (e.g., try refresh vs. re-login).
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({
        error: {
          code: 'TOKEN_EXPIRED',
          message: 'Your session has expired. Please log in again.',
        },
      });
    }

    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'The provided token is invalid.',
      },
    });
  }
}

module.exports = { authenticate };
