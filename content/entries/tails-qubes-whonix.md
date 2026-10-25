---
title: "Tails, Qubes OS and Whonix"
slug: tails-qubes-whonix
type: guide
pillars: [endpoint, anonymity]
description: "Compare Tails, Qubes OS and Whonix for different workflows, then plan installation, updates, disk encryption and separation of identities."
dek: "When a single mistake or a single exploit would be catastrophic, the operating system has to enforce the discipline for you."
updated: 2026-10-25
created: 2026-10-17
origin: original
level: intermediate
time: "1-3 hours"
related: [using-tor-safely, threat-modeling, grapheneos, tor, age-encryption]
---

Tor Browser protects one application. If your adversary can trick you into opening a malicious document, exploit your operating system, or simply seize your laptop and read what is on it, you need protection at the level of the whole system. Three projects dominate this space. They solve different problems and combine well.

## Tails: amnesic and portable

**Tails** (The Amnesic Incognito Live System) runs from a USB stick on almost any computer. Every connection goes through Tor; anything that tries to connect directly is blocked. When you shut it down, it forgets everything, because it runs from memory and does not touch the computer's hard disk. Since 2024 Tails has been part of the Tor Project.

- **Use it when** you need to work on a computer you do not fully trust or control, leave no trace on it, or carry your secure environment with you.
- **Persistent Storage** is an optional encrypted partition on the USB stick for files, keys and settings you choose to keep. Keep it as small as you can.
- **Limits:** it cannot protect you from hardware keyloggers or a compromised BIOS/firmware on the host computer, and a stick that is seized can be analysed (Persistent Storage is encrypted; use a strong passphrase).

Get it from <https://tails.net/>, and verify the download as the installation guide explains.

## Whonix: Tor enforced by architecture

**Whonix** runs as two virtual machines. The **Gateway** runs Tor and is the only thing connected to the network. The **Workstation**, where you work, can reach the network only through the Gateway. Even if malware gains root on the Workstation, it cannot learn your real IP address, because the Workstation does not know it.

- **Use it when** you want a persistent, everyday Tor-only environment with installed software, rather than an amnesic one.
- **Runs on** VirtualBox or KVM on an existing OS, or, best, inside Qubes OS as Qubes-Whonix.
- **Limits:** a compromised host OS underneath compromises everything; that is why Qubes is the recommended host.

Get it from <https://www.whonix.org/>.

## Qubes OS: security by compartmentalisation

**Qubes OS** is a desktop operating system built on the Xen hypervisor. Everything runs in separate virtual machines called *qubes*: one for work, one for personal browsing, one for banking, one for opening untrusted files. Networking and USB devices run in their own isolated qubes. Windows are colour-coded by trust level. *Disposable qubes* are created for a single task, such as opening an email attachment, and destroyed afterwards.

- **Use it when** you do a mix of high-risk and ordinary work on one machine and want a compromise in one area to stay there.
- **Hardware:** it needs a CPU with virtualisation and IOMMU support (Intel VT-x and VT-d, or AMD-V and AMD-Vi) and plenty of RAM; 16 GB is a comfortable minimum. Check the Hardware Compatibility List before buying.
- **Limits:** a learning curve, some hardware incompatibility, and it does not protect against firmware-level attacks below the hypervisor.

Get it from <https://www.qubes-os.org/>.

## Which one?

| Need | Choose |
|---|---|
| Use an untrusted or borrowed computer, leave no trace | Tails |
| Anonymous work with persistent installed tools | Whonix (ideally on Qubes) |
| Isolate high-risk tasks from the rest of your digital life | Qubes OS |
| All of the above on your own laptop | Qubes OS with Qubes-Whonix |
| Journalist handling submissions from sources | Tails or Qubes with disposables (SecureDrop's own workstation is built on Qubes) |

## Practices that apply to all three

- **Verify downloads** with the published signatures before installing.
- **Keep them updated;** all three ship security updates frequently.
- **Do not mix identities** in one session or one qube.
- **Encrypt the disk** of any persistent installation, with a long passphrase ([Encrypting Files, Disks and Backups](/guides/encrypting-files-and-backups/)).
- **Remember the human layer:** none of them stops you from logging into a personal account or telling someone who you are.

For untrusted attachments, see [Dangerzone](/kb/dangerzone/). Before releasing a document, follow [Sanitizing Documents](/guides/sanitizing-documents/) to review metadata and redaction.

## Sources

- Tails, *How Tails works* and installation guides: <https://tails.net/about/>
- Tor Project, *Tor and Tails join forces* (2024): <https://blog.torproject.org/tor-tails-join-forces/>
- Whonix, *About Whonix*: <https://www.whonix.org/wiki/About>
- Qubes OS, *Introduction* and *System requirements*: <https://www.qubes-os.org/intro/>, <https://www.qubes-os.org/doc/system-requirements/>
- Freedom of the Press Foundation, *SecureDrop Workstation*: <https://securedrop.org/>
