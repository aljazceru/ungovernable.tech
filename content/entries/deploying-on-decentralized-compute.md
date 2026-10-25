---
title: "Deploying on decentralized compute"
slug: deploying-on-decentralized-compute
type: guide
pillars: [compute]
readiness: usable
description: "Deploy a container on Akash with an explicit provider lease, inspect its status, plan data recovery, and close the deployment when you leave."
dek: "Rent compute with an exit plan, a reviewed manifest and a clear boundary around the provider's access."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [akash, decentralized-compute, decentralized-storage, verifying-a-confidential-workload]
level: intermediate
---

## Summary

This guide uses [Akash](/kb/akash/) and its documented `akt` CLI workflow. A deployment requests resources; providers bid; accepting a bid creates a lease; a manifest tells the chosen provider what to run. Start with a disposable web service whose data you can recreate.

## 1. Prepare the account and workload

Follow the official [CLI installation instructions](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/installation/index.mdx) and [context configuration](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/configuration/index.md). Use a `keyring` context for local signing. A `console-api` context uses the Console's managed wallet and a different custody model.

Keep a recovery copy of the signing key. Fund only the deployment budget and fees you intend to risk; inspect current requirements instead of copying a fixed amount from a tutorial.

Select a container image you have reviewed, pinned by tag or digest. Generate and inspect its Stack Definition Language file:

```sh
akt context show
akt sdl scaffolds
read -r -p "Reviewed container image, with tag or digest: " DEPLOY_IMAGE
akt sdl init web --image "$DEPLOY_IMAGE" > deploy.yaml
akt sdl validate deploy.yaml
```

Check CPU, memory, storage, exposed ports, environment and pricing in `deploy.yaml`. Adjust the scaffold to match the image's listening port and resource needs. Validation checks the document; it does not audit the container.

## 2. Review the plan and choose a provider

```sh
akt deploy deploy.yaml --dry-run
```

Confirm the network, signer, deposit and budget. When ready to spend, run:

```sh
akt deploy deploy.yaml
```

The interactive workflow presents bids, then creates the lease and sends the manifest. Choose deliberately using price and provider attributes. Save the deployment sequence ID, provider, service address and manifest outside the deployment.

The [workflow documentation](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/deployments/index.md) warns that a failure after creating paid state does not automatically close the deployment. Follow the reported retry or close action.

## 3. Check the running service

```sh
read -r -p "Deployment sequence ID: " DEPLOY_DSEQ
akt query deployment "$DEPLOY_DSEQ"
akt provider lease-status "$DEPLOY_DSEQ"
akt provider lease-logs "$DEPLOY_DSEQ" --follow
```

Test the returned service endpoint from your client and verify application behavior. Monitor escrow and provider status. Avoid writing secrets to logs; keep backup restoration instructions with your deployment record.

## Trust model / threat model

The provider receives the manifest and runs the containers on its infrastructure. Treat ordinary container memory, environment variables and provider storage as within that operator's access boundary. A marketplace lease is not a confidentiality proof.

Provider availability and transaction/key infrastructure remain dependencies. If you need protection from the host, use [confidential workload verification](/guides/verifying-a-confidential-workload/) and require actual evidence validation before sending secrets.

## 4. Exit and recover

Export application state to storage under your control, then rehearse restoring it with the saved image and SDL. Move clients to the replacement service before closing the old one:

```sh
akt close "$DEPLOY_DSEQ"
akt query deployment "$DEPLOY_DSEQ"
```

Confirm the closed state. The documented close operation returns remaining escrow; it is irreversible. A saved manifest is not a backup of application data. See [decentralized storage](/kb/decentralized-storage/) when designing independent copies.

## Readiness and limits

**Usable platform workflow.** The current installation source includes a release-candidate CLI path; match your binary to the documented commands before funding it. Prices, provider availability and workload performance must be checked for the actual deployment. This guide makes no capacity or cost promise.

## Primary sources

- [Akash CLI installation](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/installation/index.mdx)
- [Akash CLI contexts and custody](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/configuration/index.md)
- [Akash deploy, monitor, update and close workflow](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akt/deployments/index.md)
- [Akash deployment and lease lifecycle](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/learn/core-concepts/deployments/index.md)
- [Akash SDL reference](https://raw.githubusercontent.com/akash-network/website/main/src/content/Docs/developers/deployment/akash-sdl/syntax-reference/index.mdx)
