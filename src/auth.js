'use strict';

/**
 * auth.js — RS256 key management and JWT operations
 *
 * Strategy: RSA-SHA256 asymmetric signing.
 * - Private key: signs tokens (server-only, never exposed)
 * - Public key: verifies tokens (can be distributed safely)
 *
 * Key size: 2048-bit. Rationale — 4096-bit doubles signing latency
 * (~2ms vs ~1ms per token) with negligible security gain for JWT
 * lifetimes of 15 minutes. NIST recommends 2048-bit through 2030+.
 *
 * Token expiry: 15 minutes. Short-lived to limit blast radius of
 * token theft. Refresh tokens are out of scope for this demo.
 *
 * bcrypt rounds: 10. Industry standard — balances security and
 * register/login latency (~100ms on modern hardware).
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// ── Configuration ─────────────────────────────────────────────────────────────

const KEYS_DIR = path.resolve(__dirname, '..', 'keys');
const PRIVATE_KEY_PATH = path.join(KEYS_DIR, 'private.pem');
const PUBLIC_KEY_PATH = path.join(KEYS_DIR, 'public.pem');

const JWT_ALGORITHM = 'RS256';
const JWT_EXPIRY = '15m';
const JWT_ISSUER = 'cosmos-beta';
const JWT_AUDIENCE = 'cosmos-beta-api';
const BCRYPT_ROUNDS = 10;

// ── Key Management ────────────────────────────────────────────────────────────

/**
 * Generate a 2048-bit RSA key pair and persist to disk.
 * Returns { privateKey, publicKey } as PEM strings.
 */
function generateKeyPair() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem',
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem',
    },
  });

  fs.mkdirSync(KEYS_DIR, { recursive: true });
  fs.writeFileSync(PRIVATE_KEY_PATH, privateKey, { mode: 0o600 });
  fs.writeFileSync(PUBLIC_KEY_PATH, publicKey, { mode: 0o644 });

  console.log('[auth] Generated new RSA-2048 key pair → keys/');
  return { privateKey, publicKey };
}

/**
 * Derive a stable key-ID from the public key (SHA-256, first 16 hex chars).
 * Used as the `kid` header in JWTs for future key rotation support.
 */
function deriveKid(publicKeyPem) {
  return crypto.createHash('sha256').update(publicKeyPem).digest('hex').slice(0, 16);
}

/**
 * Load keys from disk; auto-generate if they don't exist.
 * Returns { privateKey, publicKey, kid }.
 */
function loadOrGenerateKeys() {
  let privateKey, publicKey;

  const privateExists = fs.existsSync(PRIVATE_KEY_PATH);
  const publicExists = fs.existsSync(PUBLIC_KEY_PATH);

  if (privateExists && publicExists) {
    privateKey = fs.readFileSync(PRIVATE_KEY_PATH, 'utf8');
    publicKey = fs.readFileSync(PUBLIC_KEY_PATH, 'utf8');
    console.log('[auth] Loaded existing RSA key pair from keys/');
  } else {
    if (privateExists !== publicExists) {
      console.warn('[auth] WARNING: Key pair is incomplete — regenerating both keys.');
    }
    ({ privateKey, publicKey } = generateKeyPair());
  }

  const kid = deriveKid(publicKey);
  console.log(`[auth] Key ID (kid): ${kid}`);
  return { privateKey, publicKey, kid };
}

// ── Module State ──────────────────────────────────────────────────────────────

// Loaded once at startup; mutated only on explicit key rotation.
let keys = null;

function getKeys() {
  if (!keys) {
    throw new Error('Keys not initialized — call initKeys() first');
  }
  return keys;
}

/**
 * Initialize key state. Must be called before any sign/verify operation.
 */
function initKeys() {
  keys = loadOrGenerateKeys();
  return keys;
}

// ── JWT Operations ────────────────────────────────────────────────────────────

/**
 * Sign a JWT for the given user.
 *
 * Payload structure:
 *   sub   — user ID (opaque string)
 *   email — user email (convenience claim; avoids extra DB lookup in many flows)
 *   iss   — issuer (cosmos-beta)
 *   aud   — audience (cosmos-beta-api)
 *   iat   — issued-at (set by jsonwebtoken)
 *   exp   — expiry (set by jsonwebtoken via expiresIn)
 *
 * The kid header enables future key rotation without breaking existing tokens.
 */
function signToken(user) {
  const { privateKey, kid } = getKeys();

  const payload = {
    sub: user.id,
    email: user.email,
  };

  const token = jwt.sign(payload, privateKey, {
    algorithm: JWT_ALGORITHM,
    expiresIn: JWT_EXPIRY,
    issuer: JWT_ISSUER,
    audience: JWT_AUDIENCE,
    keyid: kid,
  });

  return token;
}

/**
 * Verify a JWT. Returns the decoded payload on success.
 * Throws a JsonWebTokenError (or subclass) on any failure.
 */
function verifyToken(token) {
  const { publicKey } = getKeys();

  return jwt.verify(token, publicKey, {
    algorithms: [JWT_ALGORITHM],
    issuer: JWT_ISSUER,
    audience: JWT_AUDIENCE,
  });
}

// ── Password Hashing ──────────────────────────────────────────────────────────

/**
 * Hash a plaintext password.
 * bcrypt rounds = 10 (NIST SP 800-63b aligned; ~100ms on modern hardware).
 */
async function hashPassword(plaintext) {
  return bcrypt.hash(plaintext, BCRYPT_ROUNDS);
}

/**
 * Compare a plaintext password against a stored bcrypt hash.
 * Constant-time comparison is handled internally by bcrypt.
 */
async function verifyPassword(plaintext, hash) {
  return bcrypt.compare(plaintext, hash);
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = {
  initKeys,
  getKeys,
  signToken,
  verifyToken,
  hashPassword,
  verifyPassword,
};
