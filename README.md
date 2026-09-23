# File Integrity Monitor

A Python-based cybersecurity tool that monitors files for unauthorized changes using SHA-256 hashing.

## Features

- SHA-256 file hashing
- Trusted file baseline creation
- Detects modified files
- Detects new files
- Detects deleted files
- Security event logging
- Records old and new hashes for modified files
- Error handling for missing files and directories
- Automated tests using pytest
- Modular Python architecture

## Project Architecture

```text
Protected Files
      |
      v
  SHA-256 Hashing
      |
      v
 Trusted Baseline
      |
      v
   File Scanner
      |
      +---------> NEW
      |
      +---------> MODIFIED
      |
      +---------> DELETED
      |
      v
 Security Event Log