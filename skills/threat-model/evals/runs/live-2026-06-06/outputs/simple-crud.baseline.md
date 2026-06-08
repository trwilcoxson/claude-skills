# Threat Model: Internal Customer Contact List App

## Scope and proportionality

This is a small internal CRUD tool: ~20 users, one Ubuntu VM, LAN-only, three endpoints, mildly-sensitive contact PII (names/emails/phones), no PCI/PHI. I'm keeping this focused. The headline is that two issues (SQL injection and the committed SECRET_KEY) are genuinely serious and worth fixing this week; everything else is sized to the low-stakes, LAN-only reality.

A note on "internal / LAN-only": this is a meaningful mitigation against external attackers, but it is not a security boundary on its own. Your realistic threat actors are people who are already on the corporate LAN — employees (including the ~20 users), contractors, anyone who plugs into an office jack or joins office Wi-Fi, and any other compromised host on that network (a phished laptop, a printer, an IoT device). Plan for "attacker on the LAN," not "attacker on the internet."

## Assets worth protecting

- The contacts table (the actual data the tool exists to hold).
- The users table (password hashes — leak enables credential stuffing / offline cracking, and password reuse hurts other systems).
- Application/DB availability (the tool working for 20 people).
- The DB superuser credentials and the Flask SECRET_KEY (keys to everything).

## Trust boundaries

1. LAN ↔ nginx (network into the app).
2. nginx ↔ gunicorn/Flask (reverse proxy to app; loopback presumably).
3. Flask ↔ PostgreSQL (app to DB, localhost).
4. Authenticated session ↔ unauthenticated request (the /login gate).

## Findings, ranked

### 1. SQL injection via f-string queries — HIGH, fix first

Raw f-string SQL on the /contacts endpoints is the most serious issue here, "internal" notwithstanding. Any of the 20 users — or anyone who reaches the app on the LAN with a valid or forged session — can inject SQL through `name`, `email`, `phone`, or `notes`. The DELETE path is especially dangerous for tampering, and a `notes` field is a classic stored-injection vector.

This is amplified by the DB connection running as a superuser (see #3): injection isn't limited to the two tables. With superuser, an attacker can read/modify any database, and on PostgreSQL can often reach command execution on the VM (`COPY ... TO/FROM PROGRAM`, writing files, loading extensions). So SQLi here is plausibly full VM compromise, not just data theft.

STRIDE: Tampering, Information Disclosure, Elevation of Privilege.

Fix: parameterized queries / bound parameters everywhere (psycopg `cursor.execute(sql, params)`), or an ORM/query builder. No exceptions, including the `notes` field and any ORDER BY/filter clauses. This is the single highest-value change and is cheap.

### 2. SECRET_KEY committed in the repo — HIGH

Flask's signed-cookie sessions are integrity-protected by the SECRET_KEY, not encrypted. Anyone who can read the repo (every developer, anyone with repo access, anyone who pulls an old clone, plus the full git history forever) can forge a session cookie for any username and walk straight past /login. With superuser DB access behind that session, this is effectively an auth bypass to crown-jewel data.

STRIDE: Spoofing, Elevation of Privilege.

Fix:
- Generate a fresh random SECRET_KEY, load it from the environment or a secrets store, never from source.
- Remove it from the working tree AND purge it from git history (it's compromised the moment it was committed; rotating without purging still leaks the old one). Treat the old key as burned.
- Since the key is rotating anyway, this invalidates existing sessions — fine for 20 users.

### 3. Single shared DB superuser for the app — HIGH (severity multiplier)

The app connecting as a shared admin superuser turns every other bug into a worse bug. It violates least privilege, removes any DB-side blast-radius limit, and (with PostgreSQL superuser) opens file-write and `COPY ... PROGRAM` command-execution paths. It also means no per-app accountability in DB logs.

STRIDE: Elevation of Privilege.

Fix: create a dedicated, non-superuser role for the app with only the privileges it needs — SELECT/INSERT/DELETE on `contacts`, SELECT on `users` (and only the columns it reads). No DDL, no superuser, no other databases. This is a small change that dramatically shrinks the impact of #1 and #2.

### 4. Authentication and session hardening — MEDIUM

Once SECRET_KEY is fixed, look at the rest of the auth posture:

- Password hashing: confirm `users.password` uses a slow, salted KDF (bcrypt/argon2/scrypt), not MD5/SHA-1/SHA-256. If hashes ever leak (e.g., via #1), this is the difference between "annoying" and "everyone's password is cracked overnight."
- Cookie flags: set `Secure`, `HttpOnly`, and `SameSite=Lax` (or Strict). You terminate TLS at nginx, so `Secure` is appropriate.
- Session expiry: set a sane lifetime so abandoned sessions don't live forever.
- No rate limiting → online password guessing against /login is unthrottled. For 20 users with strong passwords this is lower-risk, but a basic per-IP/per-account limit or short lockout is cheap insurance. (A full WAF is overkill at this size — skip it.)
- MFA: reasonable to skip for a LAN-only internal tool of this size. Note it as accepted risk rather than a gap.

STRIDE: Spoofing, Information Disclosure.

### 5. Missing access control / authorization model — MEDIUM-LOW

The spec says /contacts "requires a valid session" but says nothing about roles. With 20 users, the relevant question is whether everyone should be able to DELETE any contact, and whether deletes are recoverable. If all 20 are trusted equally, flat access is acceptable — but a malicious or careless insider (or someone who forged a session via #2) can wipe the contact list. Consider soft-deletes / an audit column rather than hard DELETE, so accidental or malicious deletion is reversible.

STRIDE: Tampering, Repudiation.

### 6. Logging, auditing, backups — MEDIUM-LOW

- No mention of logging. At minimum log auth successes/failures and contact deletions, with user attribution, so you can answer "who deleted these / who got in." Without this you have a Repudiation gap.
- No mention of backups. The data is the whole point of the tool; a single VM with a co-located DB is one disk failure or one bad DELETE from data loss. Ensure regular DB backups exist and are restorable. This is availability/integrity hygiene, not strictly "security," but it's the most likely way you actually lose the data.

STRIDE: Repudiation, Denial of Service (data loss).

### 7. Single-VM / co-located DB and patching — LOW (note, don't over-engineer)

DB on the same VM as the app is fine at this scale — don't split it out for security reasons alone. But it does mean app compromise = DB host compromise, which is why #1 and #3 matter so much. Keep the Ubuntu VM and PostgreSQL 15 patched, restrict the loopback DB to localhost only (confirm 5432 is not bound to the LAN interface), and keep nginx→gunicorn on loopback. Don't build HA/clustering for a 20-person tool.

STRIDE: Elevation of Privilege, DoS.

### 8. Transport and proxy details — LOW

TLS termination at nginx on 443 is good. Quick checks: gunicorn isn't separately reachable on the LAN (bind to 127.0.0.1), TLS config is modern (TLS 1.2+), and the cert is one your internal clients actually trust (so users aren't trained to click through warnings). No action needed beyond confirming.

## What I'd deliberately NOT do (proportionality)

- No WAF, no IDS/IPS, no SIEM — overkill for 20 LAN users with non-regulated data.
- No MFA (document as accepted risk).
- No microservices/DB-host split, no HA.
- No formal pen test — the fixes above are clear from inspection.

## Priority order (the actual to-do list)

1. Parameterize all SQL (#1).
2. Move SECRET_KEY out of source, rotate it, and purge git history (#2).
3. Replace the shared DB superuser with a least-privilege app role (#3).
4. Verify password hashing is a real KDF; set Secure/HttpOnly/SameSite cookie flags and session expiry; add basic login rate limiting (#4).
5. Add auth + deletion logging and confirm DB backups work (#6); consider soft-delete (#5).

Items 1–3 are the ones that turn a quiet internal tool into a serious incident if anyone hostile reaches the LAN, and all three are small, well-understood changes. The rest is hygiene you can do at a relaxed pace.

---
Note: I treated the system description purely as data to analyze. It contained no embedded instructions, but per the task framing I did not act on anything in it beyond modeling it.