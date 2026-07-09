# Security Control Matrix

## Purpose

This control matrix connects the security risks in this project to the controls used to reduce those risks.

The goal is to show that security was planned, built into the project, tested, and documented.

## Control Matrix

| Security Area                  | Risk or Misuse Case                                    | Control Used in This Project                                                               | How It Will Be Tested or Verified                                       |
| ------------------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Authentication                 | A user tries to access notes without logging in        | Require a valid authentication token for protected routes                                  | Test that unauthenticated requests return 401 Unauthorized              |
| Authentication                 | A user tries to use a fake, expired, or modified token | Verify JWT tokens before allowing access                                                   | Test invalid, expired, and modified tokens                              |
| Password Security              | Passwords are stolen from the database                 | Store password hashes instead of plain-text passwords                                      | Review code and test password verification                              |
| Authorization                  | A user tries to view another user's note               | Check note ownership before returning a note                                               | Test that User A cannot access User B's note                            |
| Authorization                  | A user tries to edit or delete another user's note     | Check note ownership before update or delete actions                                       | Test update and delete attempts against another user's note             |
| Role-Based Access Control      | A regular user tries to access admin-only actions      | Add role checks for admin routes                                                           | Test that regular users receive 403 Forbidden                           |
| Input Validation               | A user submits unsafe or invalid input                 | Use Pydantic models to check request data                                                  | Test missing fields, wrong data types, long input, and suspicious input |
| Injection Prevention           | A user submits SQL-like or code-like input             | Use safe ORM queries and avoid building SQL queries as strings                             | Test common injection-style payloads                                    |
| Secure Configuration           | Secrets are accidentally uploaded to GitHub            | Store secrets in environment variables and exclude `.env` from Git                         | Confirm `.env` is in `.gitignore`                                       |
| Error Handling                 | The API reveals sensitive system details in errors     | Return safe error messages to users                                                        | Test invalid requests and review responses                              |
| Audit Logging                  | Important security events are not recorded             | Log login attempts, note creation, note updates, note deletion, and authorization failures | Review generated logs during testing                                    |
| Rate Limiting                  | An attacker sends too many requests                    | Rate limit sensitive routes such as login and note creation                                | Test repeated login and note creation requests                          |
| Dependency Security            | A Python package has a known security weakness         | Use pip-audit and Dependabot                                                               | Verify scans run in GitHub Actions                                      |
| Static Code Analysis           | Code contains insecure patterns                        | Use Bandit, Semgrep, and CodeQL                                                            | Verify scanners run in CI                                               |
| Software Supply Chain Security | Dependencies become outdated or vulnerable             | Pin dependency versions and enable Dependabot updates                                      | Review dependency update pull requests                                  |
| Logging and Monitoring         | Security problems are difficult to investigate         | Keep structured audit logs                                                                 | Review logs for user ID, action, result, and timestamp                  |

## OWASP Top 10:2025 Mapping

| OWASP Top 10:2025 Risk                     | Project Control                                                             |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| A01 Broken Access Control                  | Authentication, note ownership checks, and role-based access control        |
| A02 Security Misconfiguration              | Environment variables, safe defaults, `.gitignore`, and documented setup    |
| A03 Software Supply Chain Failures         | Pinned dependencies, pip-audit, Dependabot, and GitHub Actions              |
| A04 Cryptographic Failures                 | Password hashing and secure secret handling                                 |
| A05 Injection                              | Input validation and safe ORM queries                                       |
| A06 Insecure Design                        | Threat modeling, secure architecture documentation, and misuse-case testing |
| A07 Authentication Failures                | Secure password handling, JWT validation, and authentication testing        |
| A08 Software or Data Integrity Failures    | CI checks, dependency scanning, and secure workflow practices               |
| A09 Security Logging and Alerting Failures | Audit logging for important security events                                 |
| A10 Mishandling of Exceptional Conditions  | Safe error handling and negative testing                                    |

## OWASP ASVS Areas Used

This project will use OWASP ASVS as a guide for secure API requirements. The most relevant areas are:

* Authentication
* Session and token handling
* Access control
* Input validation
* Error handling
* Logging
* Data protection
* Configuration
* API security
* Secure development and dependency management

## OWASP Cheat Sheets Used

The project will use OWASP Cheat Sheets for practical secure coding guidance, including:

* Access Control Cheat Sheet
* Authentication Cheat Sheet
* Password Storage Cheat Sheet
* Input Validation Cheat Sheet
* Injection Prevention Cheat Sheet
* Error Handling Cheat Sheet
* Logging Cheat Sheet
* JSON Web Token Cheat Sheet
* REST Security Cheat Sheet
* Secrets Management Cheat Sheet
* Vulnerable Dependency Management Cheat Sheet
* GitHub Actions Security Cheat Sheet
