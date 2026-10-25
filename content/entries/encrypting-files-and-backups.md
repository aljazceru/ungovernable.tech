---
title: "Encrypting Files, Disks and Backups"
slug: encrypting-files-and-backups
type: guide
pillars: [endpoint, cryptography, storage]
description: "A practical guide to protecting files, disks, backups and account credentials, with recovery planning and the limits of encryption at rest."
dek: "Encryption at rest is what stands between a seized or stolen device and everything on it."
updated: 2026-10-25
created: 2026-10-17
origin: original
level: beginner
time: "1 hour"
related: [age-encryption, threat-modeling, tails-qubes-whonix, grapheneos, post-quantum-cryptography]
---

Devices get lost, stolen, seized at borders and taken in raids. Encryption at rest means that whoever holds the device holds only noise, as long as it is switched off (or locked) and your passphrase is strong. It is the cheapest, highest-value security measure most people can take.

## 1. Encrypt the whole disk

| System | Tool | Notes |
|---|---|---|
| Linux | LUKS (dm-crypt) | Offered by most installers. Use a long passphrase. |
| macOS | FileVault | On by default on recent Macs with Apple silicon; check it is on and do not store the recovery key with Apple if your threat model includes legal requests to Apple. |
| Windows | BitLocker / Device Encryption | Often enabled automatically, with the recovery key **uploaded to your Microsoft account** by default. Microsoft can be compelled to hand it over. Store the key yourself instead. |
| Android | File-based encryption | On by default; strength depends on your lock-screen passcode. |
| iOS | Data Protection | On by default when a passcode is set; use an alphanumeric passcode. |

Full-disk encryption protects a device that is **off**. A running, unlocked laptop has its keys in memory. Shut down (do not just sleep) before crossing a border or when a raid is plausible.

## 2. Use a strong passphrase

Encryption is only as strong as the passphrase. Use a long random passphrase: five to seven words chosen randomly (for example with dice and the EFF word list) are memorable and very hard to brute-force. On phones, the hardware limits guessing, but a six-digit PIN is still far weaker than a long alphanumeric passcode.

## 3. Encrypt individual files with age

**age** (<https://age-encryption.org/>) is a small, modern file-encryption tool with no configuration options to get wrong. It is a good replacement for most uses of PGP for files.

```
age-keygen -o key.txt                       # create a key pair
age -r age1yourpublickey... -o secret.tar.age secret.tar   # encrypt to a public key
age -d -i key.txt -o secret.tar secret.tar.age              # decrypt
age -p -o notes.txt.age notes.txt           # encrypt with a passphrase instead
```

It can also encrypt to existing SSH keys. See [age: Modern File Encryption](/kb/age-encryption/).

## 4. Encrypted containers and deniability

**VeraCrypt** (<https://veracrypt.fr/>) creates encrypted containers and volumes, and supports *hidden volumes* inside an outer volume for plausible deniability. Deniability is weaker than it sounds: a forensic examiner may find traces of the hidden volume's use elsewhere on the system, and some jurisdictions punish refusal to decrypt regardless. Know the law where you are; in some countries, refusing to provide a key is a criminal offence.

## 5. Encrypted backups

Backups protect you from loss; encrypted backups protect you from the backup being the weak point. A practical rule is **3-2-1**: three copies, on two different kinds of media, one of them off-site.

- **restic** (<https://restic.net/>) encrypts every backup by default and works with local disks, SFTP servers and many cloud storage services.
- **BorgBackup** (<https://www.borgbackup.org/>) offers deduplicated, authenticated encryption; often paired with a remote server you control.
- **Test restores** regularly. A backup you have never restored is a hope, not a backup.

For a worked synchronization and recovery setup, follow [Private File Sync and Backup](/guides/private-file-sync-and-backup/) and the [Syncthing](/kb/syncthing/) entry.

## 6. Passwords and second factors

- Use a **password manager**. KeePassXC (<https://keepassxc.org/>) stores an encrypted database locally that you can sync however you like; Bitwarden is an open-source hosted option that can also be self-hosted.
- Use **unique passwords** everywhere.
- Use **hardware security keys** (FIDO2/WebAuthn) or passkeys for important accounts. They resist phishing in a way that SMS and app codes do not.

## 7. Look ahead to quantum computers

Data encrypted today with classical public-key encryption could be decrypted later by a sufficiently large quantum computer ("harvest now, decrypt later"). Symmetric encryption such as AES-256 is not seriously threatened. For long-lived secrets encrypted to public keys, prefer tools that support post-quantum or hybrid key exchange as they become available. See [Post-Quantum Cryptography](/kb/post-quantum-cryptography/).

For account authentication and spare-key planning, see [Passkeys and Security Keys](/kb/passkeys-and-security-keys/). Before sharing decrypted files, use [Sanitizing Documents](/guides/sanitizing-documents/).

## Sources

- age specification and reference implementation: <https://age-encryption.org/v1>, <https://github.com/FiloSottile/age>
- cryptsetup / LUKS: <https://gitlab.com/cryptsetup/cryptsetup>
- Apple Platform Security, *FileVault*: <https://support.apple.com/guide/security/welcome/web>
- Microsoft, *BitLocker recovery overview*: <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview>
- EFF, *Dice-generated passphrases* and word lists: <https://www.eff.org/dice>
- VeraCrypt documentation, *Hidden volume*: <https://veracrypt.fr/en/Hidden%20Volume.html>
- restic documentation: <https://restic.readthedocs.io/>

Continue with [Magic Wormhole](/kb/magic-wormhole/).
