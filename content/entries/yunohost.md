---
title: "YunoHost"
slug: yunohost
type: deep-dive
pillars: [endpoint, compute]
readiness: usable
description: "YunoHost simplifies running a Debian server with packaged apps, users and backups. Learn what it manages and what the administrator still trusts."
dek: "Self-hosting with a web administration panel, while keeping responsibility for the apps, accounts and server underneath."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [startos, openwrt, running-freedom-infrastructure, encrypting-files-and-backups, threat-modeling]
tags: [self-hosting, servers, yunohost, debian]
---

## Summary

[YunoHost](https://yunohost.org/) is a Debian-based server operating system intended to simplify self-hosting. It provides web and command-line administration for applications, users, domains, certificates and backups. It can run on a machine at home or a remote server.

The benefit is control of the server and its services. The trade-off is taking on their maintenance. Compare [StartOS](/kb/startos/) and decide what you can realistically operate before moving services away from an existing provider.

## How it works

YunoHost's [application catalog workflow](https://doc.yunohost.org/admin/apps/) installs packaged applications through the web administration panel or command line. Packages integrate application setup and may support upgrades, backup and restore, and the shared login system. Integration varies: the documentation explicitly notes that some apps do not support LDAP or single sign-on.

The project also manages domain names and TLS certificates and includes a mail stack. Those capabilities do not make every deployment configuration equally suitable; start with a small set of applications and their documented requirements.

## Updates, backups and remote access

**Maintain both the system and applications.** The [security guidance](https://doc.yunohost.org/admin/security) asks administrators to keep both updated, watch for security notices, and remove unused applications. An application appearing in the catalog does not remove that responsibility. Package quality checks can also cause an app to be hidden or its upgrades put on hold.

**Back up what each package supports.** The [backup system](https://doc.yunohost.org/admin/backups) can archive system configuration, data and supported applications from the web panel or command line. Its default archive format is `.tar`. Treat those archives as sensitive, arrange appropriate encryption and storage away from the server, and practice restoration. An application must support the backup mechanism; do not assume all of its data is covered without checking.

**Choose who can reach an application.** Apps can be placed at a domain, subdomain or supported subpath. Installation commonly offers a public or authenticated-access choice, and permissions can be changed in the administration panel. Remote availability depends on how you host and expose the server. Check access from outside your own network before relying on it, and check that a private app actually requires authentication.

## Trust model

You trust Debian, YunoHost, application packagers, the applications themselves, the server hardware and its administrator. On rented infrastructure, the hosting operator remains part of that model.

The [project overview](https://doc.yunohost.org/admin/what_is_yunohost) is explicit that applications share a system and environment. They normally run under separate user accounts with restricted permissions, but YunoHost is not a system for strong isolation between mutually distrustful tenants. Avoid putting unrelated high-risk services together merely because installation is convenient.

## Readiness

**Usable for a modest server that someone actively maintains.** The project supplies application management, backups and security guidance. Verify the maturity and maintenance of each chosen package separately from the operating system's capabilities.

## Limits

Self-hosting does not automatically make data end-to-end encrypted or eliminate the server administrator's access. Public services need ongoing attention to credentials, updates, exposure and recovery. The project does not promise strict isolation between applications or provide a guarantee that an administrator cannot lose data.

Plan recovery with [Encrypting Files, Disks and Backups](/guides/encrypting-files-and-backups/), and use [Threat Modeling](/guides/threat-modeling/) to decide whether home hosting, rented hosting or a managed service best fits the risks.

## Primary sources

- [YunoHost project](https://yunohost.org/).
- [What YunoHost provides and its isolation limits](https://doc.yunohost.org/admin/what_is_yunohost).
- [Applications, permissions and package integration](https://doc.yunohost.org/admin/apps/).
- [Creating, storing and restoring backups](https://doc.yunohost.org/admin/backups).
- [YunoHost security guidance and update responsibilities](https://doc.yunohost.org/admin/security).
