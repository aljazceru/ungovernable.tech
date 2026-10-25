---
title: "Sanitizing Documents Before Sharing"
slug: sanitizing-documents
type: guide
pillars: [endpoint]
readiness: usable
description: "Prepare documents for sharing by checking metadata, removing sensitive content with real redaction, and reviewing filenames and the final output."
dek: "Metadata cleanup, safe rendering and redaction solve different problems. Use the right step for each, then inspect the actual file you will send."
updated: 2026-10-25
created: 2026-10-25
origin: original
level: intermediate
related: [dangerzone, encrypting-files-and-backups, threat-modeling, tails-qubes-whonix, metadata-resistance]
tags: [documents, metadata, redaction, mat2, exiftool]
---

## Summary

A document can reveal information through its visible contents and through metadata. The [mat2 documentation](https://github.com/jvoisin/mat2) gives examples such as camera details and capture times in images, and author or company information in office files. [LibreOffice's security options](https://help.libreoffice.org/latest/en-US/text/shared/optionen/securityoptionsdialog.html) also identify comments, recorded changes and stored versions as information to check before sharing.

Use a release copy. Keep the original separately if it is needed for evidence, editing or verification. Decide which information must remain and which must be removed before starting.

## 1. Decide what you need to remove

| Risk | Appropriate step | What that step does not establish |
|---|---|---|
| A malicious attachment | Convert with [Dangerzone](/kb/dangerzone/) before ordinary viewing | The content is true, harmless or anonymous. |
| EXIF, author details or other embedded metadata | Clean supported formats with mat2 or a format-appropriate tool | Every identifying detail in the content is gone. |
| Names, faces, addresses or confidential passages | Apply actual redaction and export the finished result | The original or an intermediate editing file is safe to share. |
| Identifying filename or visible marks | Review and rename the release copy; inspect its pages | The sending account and delivery channel reveal nothing. |

If the document came from an untrusted source, start with Dangerzone. Do not open the original in an office suite just to inspect its properties. Its [security model](https://docs.dangerzone.rocks/latest/explanation/security-model/) explains why it isolates document parsing and rebuilds a PDF from pixels.

## 2. Remove metadata from the release copy

**mat2** supports metadata cleanup for a range of document, image, audio and archive formats. Its maintained [repository](https://github.com/jvoisin/mat2) documents the supported formats and command-line options. By default, it writes a separate file with `.cleaned` added to the filename:

```sh
mat2 --show release.pdf
mat2 release.pdf
mat2 --show release.cleaned.pdf
```

Run this on the working copy you intend to publish. Keep the source and output distinguishable. Avoid `--inplace` when you need to preserve the original. Avoid `--lightweight` when your aim is the most thorough cleanup: it deliberately trades some metadata removal for preserving file data.

The project warns that an empty `--show` result is **not proof that no metadata exists**. Complex formats cannot be exhaustively checked that way. Cleanup can also change rendering or remove selectable text, so inspect the result.

**ExifTool** reads and edits metadata across many formats, including EXIF information in images. Use its [format support and documentation](https://exiftool.org/) to decide what it can change in your file. Do not assume that a command which removes tags from a JPEG safely sanitizes every other format.

**PDF trap:** ExifTool uses incremental updates for PDF metadata edits. Its [PDF documentation](https://exiftool.org/TagNames/PDF.html) explicitly warns that the old information remains recoverable. Clearing the displayed PDF author with ExifTool alone is not secure removal of that information. Use a rebuilding workflow such as Dangerzone for the copy you intend to release, then inspect the output.

## 3. Redact the contents, not just their appearance

Drawing a black rectangle over text is not evidence that the text underneath was deleted. Use a redaction function that removes the underlying content when you finalize the document.

For a documented local workflow, [LibreOffice redaction](https://help.libreoffice.org/latest/en-US/text/shared/guide/redaction.html) sends the document to Draw, where you mark regions for removal. Finish with **Redacted Export (Black)** or **Redacted Export (White)**. The documentation distinguishes those final exports, which replace redacted content with pixels, from a PDF exported for intermediate review. Share the finalized export, not the editable drawing or the review copy.

Review comments, tracked changes and version information in editable documents too. Removing an author's name is not the same as removing a confidential passage from revision history. If recipients do not need editable history, prepare a final rendered copy and check what it displays.

## 4. Check the actual outgoing file

Reopen the final export. Inspect every page for missed text, faces, watermarks, headers and footers. Try searching for removed words and copying text from redacted regions into a plain-text editor. These are useful checks, not a proof against every form of disclosure. Check the metadata again after your last edit or export.

Choose a neutral filename: mat2's `.cleaned` suffix preserves the original basename. A filename containing a person's name or internal case identifier needs separate attention. Share only the final reviewed file, not the original, an editor backup or an archive containing both.

**Printed and scanned pages need another check.** [EFF's research on printer tracking dots](https://www.eff.org/deeplinks/2017/06/printer-tracking-dots-back-news) documents identifying marks in color laser output that can appear in scans. Removing file metadata does not remove identifying content in the page image. Do not assume printing and scanning makes a document anonymous, or that a metadata cleaner removes printer marks.

## Trust model and limits

The tools run on your computer and parse files; keep them and the operating system updated. Prefer local processing for confidential material. Dangerzone's sandbox reduces document-exploit risk, but it cannot protect a host that is already compromised, and it deliberately preserves visible page content.

Sanitization does not hide which account sent a file or who had access to the original. For that wider plan, use [Threat Modeling](/guides/threat-modeling/) and [Metadata Resistance](/kb/metadata-resistance/). Protect retained originals with [file and backup encryption](/guides/encrypting-files-and-backups/).

## Readiness

**Usable, with manual review.** The tools have documented workflows, but no single button establishes that a document is safe, anonymous and correctly redacted. A second trusted reviewer is useful when publication could expose someone.

## Primary sources

- [mat2: metadata examples, supported formats, commands and limitations](https://github.com/jvoisin/mat2).
- [ExifTool documentation](https://exiftool.org/) and [reversible PDF metadata edits](https://exiftool.org/TagNames/PDF.html).
- [Dangerzone security model](https://docs.dangerzone.rocks/latest/explanation/security-model/).
- [LibreOffice redaction and final export](https://help.libreoffice.org/latest/en-US/text/shared/guide/redaction.html).
- [LibreOffice warnings about personal data, comments and tracked changes](https://help.libreoffice.org/latest/en-US/text/shared/optionen/securityoptionsdialog.html).
- [EFF's printer tracking research and its limits](https://www.eff.org/deeplinks/2017/06/printer-tracking-dots-back-news).
