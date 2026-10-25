---
title: "Dangerzone"
slug: dangerzone
type: deep-dive
pillars: [endpoint]
readiness: usable
description: "Dangerzone rebuilds untrusted documents as PDFs through an isolated conversion process. What the sandbox removes, what it trusts, and its limits."
dek: "Turn an attachment into pages you can read, without handing its original structure to your everyday document viewer."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [sanitizing-documents, tails-qubes-whonix, threat-modeling, suspected-device-compromise]
tags: [documents, sandboxing, metadata]
---

## Summary

[Dangerzone](https://dangerzone.rocks/) is a Freedom of the Press Foundation project for converting potentially dangerous PDFs, office documents and images into PDFs built from their rendered pages. It runs locally and provides installers for Windows, macOS and Linux. It is useful when reading documents from unfamiliar sources is part of your work.

Its purpose is to reduce the risk of opening a malicious document. Removing visible sensitive information is a separate task; follow [Sanitizing Documents](/guides/sanitizing-documents/) before publishing the result.

## How it works

Dangerzone sends the original document into an isolated converter. The converter renders its pages into raw RGB pixels. The host receives page dimensions and pixels, then builds a new PDF. Optional optical character recognition (OCR) adds a searchable text layer.

The [documented container path](https://dangerzone.rocks/about/) runs the parsers inside a **gVisor sandbox within a Linux container**. Both have networking disabled, and the original document is passed through standard input rather than a shared host directory. On Windows and macOS, Podman supplies the Linux virtual machine beneath the containers. The [security model](https://docs.dangerzone.rocks/latest/explanation/security-model/) describes a different Qubes OS path using an offline disposable qube.

The original document's macros, scripts, embedded objects and metadata are not copied into the rebuilt PDF as those objects. What survives is their visible rendering, with optional text recognized from it. This also means that editable structure and interactive features are not preserved.

## Trust model

Dangerzone assumes the document parser might be exploitable. Its defenses therefore rely on isolation and the narrow pixels-only output channel, rather than deciding that an attachment has no known malware signature.

You still trust the host operating system, Dangerzone, the sandbox and container machinery, and the code that rebuilds and displays the PDF. Keep both the application and its sandbox updated. The project explicitly acknowledges that vulnerabilities in multiple layers could be combined to escape containment.

## Readiness

**Usable.** The project distributes the application and documents its supported platforms and conversion workflow. It is a practical tool for reading supported document formats, with the compatibility and security limits below.

## Limits

- **Visible content remains.** A name, face, watermark or deceptive instruction that appears on the page will appear in the output. Conversion is not redaction or verification of a document's claims.
- **The host must already be trustworthy.** Dangerzone cannot repair an infected computer. Operating-system previews and thumbnails can also process an original outside Dangerzone; the project calls out this risk.
- **Conversion can fail or lose useful structure.** Check page completeness, legibility and OCR before using the result. Keep originals separately when they are needed as evidence, and share only the reviewed output.
- **The original remains dangerous.** Treat an archived original as untrusted. A successful conversion does not certify the original as safe to open in an office application.

For a broader compartmentalized workflow, compare [Tails, Qubes OS and Whonix](/guides/tails-qubes-whonix/).

## Primary sources

- [Dangerzone project and downloads](https://dangerzone.rocks/).
- [Dangerzone: how conversion and isolation work](https://dangerzone.rocks/about/).
- [Dangerzone security model and limits](https://docs.dangerzone.rocks/latest/explanation/security-model/).
- [Canonical source repository and documentation](https://github.com/freedomofpress/dangerzone).
