# Security Notes

This project connects to an email account and therefore must keep authentication material outside source control.

## Repository hygiene

- Credentials and application passwords must never be committed.
- Use environment variables or a local secrets file excluded by `.gitignore`.
- Rotate any credential that has previously appeared in repository history.

## Scope

The project is an email-reading utility and should not be treated as a production mail-security system without additional authentication, authorization, error handling, logging, and dependency review.