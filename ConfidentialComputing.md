#### Confidential computing on GPUs
- [continuum](https://docs.edgeless.systems/continuum)
- [confidential AI from GPU enclaves](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves)
- [Nvidia confidential computing deployment guide](https://docs.nvidia.com/confidential-computing-deployment-guide.pdf)
- [Building GPU TEEs using CPU Secure Enclaves with GEVisor](https://dl.acm.org/doi/pdf/10.1145/3620678.3624659)
- [Heterogeneous Isolated Execution for Commodity GPUs](https://insujang.github.io/assets/pdf/hix_slides.pdf)

#### New Projects (Feb 2026)
- [spdm-rs](https://github.com/ccc-spdm-tools/spdm-rs) - Rust implementation of DMTF SPDM, IDE_KM, and TDISP protocols for TEE-I/O in Confidential Computing. Facilitates direct device assignment for Trusted Execution Environment I/O with GPU TEEs and Confidential Virtual Machines.
- [Identra](https://github.com/IdentraHQ/identra) - Confidential AI memory layer and single-sign-on (SSO) platform. Built with Rust, Tauri v2, AWS Nitro Enclaves, and Next.js. Local-first, edge-compute, and privacy-preserving identity and memory vault for AI interactions.
- [ConfidentialML](https://github.com/UnplugCharger/confidential) - Private XGBoost inference service built with EGo (Intel SGX). Solves the dual privacy problem where neither model owner nor data owner wants to trust the other with their sensitive assets.
- [GoShip](https://github.com/guilhermebr/goship) - Go-based, self-hosted VM-centric application control plane designed for Confidential Computing. VM-first isolation with explicit virtualization, built on KVM/QEMU/Libvirt, and ready for SEV-SNP, TDX, and attestation workflows.
- [WeTEE](https://github.com/wetee-dao/contract) - Decentralized application deployment platform integrated with a Trusted Execution Environment (TEE). Consists of blockchain networks and multiple confidential computing clusters for efficient decentralized confidential computing solutions.

#### Confidential computing on CPUs:
- [Trusted Container Extensions for Container-based Confidential Computing](https://arxiv.org/pdf/2205.05747.pdf)
- [Trusted execution environment](https://en.wikipedia.org/wiki/Trusted_execution_environment)
- [Confidential Containers](https://github.com/confidential-containers/)
- [Firecracker-microvm](https://firecracker-microvm.github.io/)
- [Confidential computing](https://en.wikipedia.org/wiki/Confidential_computing)
- [Kata containers](https://katacontainers.io/)
- [awesome-zama](https://github.com/zama-ai/awesome-zama)
- [zama.ai](https://www.zama.ai/)
- [Remote attestation Procedures Architecture](https://ietf-rats-wg.github.io/architecture/draft-ietf-rats-architecture.html)
- [Trusted Execution Environment Provisioning (TEEP) Architecture](https://datatracker.ietf.org/doc/html/draft-ietf-teep-architecture-19)
- [CoCo attestation proposal KBS / AS](https://github.com/confidential-containers/confidential-containers/issues/119)
- [Generic Key Broker System for CoCo](https://github.com/confidential-containers/confidential-containers/issues/68)
- [Constellation - Always encrypted kubernetes](https://github.com/edgelesssys/constellation?tab=readme-ov-file)
- [Garmine Shielded Containers](https://github.com/gramineproject/gsc)
- [Confidential containers in kubernetes](https://archive.is/u1vhR)
- [Garmine library OS - run applications in enclaves](https://github.com/gramineproject/gramine/tree/master?tab=readme-ov-file)
- [COCONUT Secure VM Service Module](https://github.com/coconut-svsm/svsm)
- [enclavie](https://github.com/enclaive)
- [List of SGX supported Intel CPUs](https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html)
- [List of SGX hardware](https://github.com/ayeks/SGX-hardware)
- [Secure Multi-Party Computation Without Agreement](https://eprint.iacr.org/2002/040.pdf)
- [SGX Secure Enclaves in Practice: Security and Crypto Review](https://www.youtube.com/watch?v=0ZVFy4Qsryc)
- [General overview of AMD SEV-SNP and Intel TDX](https://sys.cs.fau.de/extern/lehre/ws22/akss/material/amd-sev-intel-tdx.pdf)
- [Occlum](https://github.com/occlum/occlum)
- [awesome-confidential-computing](https://github.com/bpradipt/awesome-confidential-computing)
- [Fraunhofer-AISEC/cmc](https://github.com/Fraunhofer-AISEC/cmc) - Remote attestation for Trusted and Confidential Computing platforms (TPM, AMD SEV-SNP, Intel SGX/TDX)
- [inclavare-containers/TNG](https://github.com/inclavare-containers/TNG) - Trusted Network Gateway: A tool for establishing secure communication tunnels in confidential computing
- [Phala-Network/phala-cloud](https://github.com/Phala-Network/phala-cloud) - Confidential Computing native cloud platform
- [ultravioletrs/cocos](https://github.com/ultravioletrs/cocos) - Cocos AI - Confidential Computing System for AI
- [NVIDIA/nvtrust](https://github.com/NVIDIA/nvtrust) - Ancillary open source software to support confidential computing on NVIDIA GPUs
- [flashbots/flashbots-images](https://github.com/flashbots/flashbots-images) - Reproducible hardened Linux images for confidential computing and safe MEV

#### Confidential computing in the cloud 
##### Azure 
- how to deploy with cli https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-enclave-nodes-aks-get-started
- gramine aks azure https://github.com/gramineproject/contrib/tree/master/Examples/aks-attestation
- azure confidential providers https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-containers-enclaves

##### AWS
- [Nitro enclaves](https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html)

##### GCP
- [Confidential Computing](https://cloud.google.com/security/products/confidential-computing)

##### Alibaba 
- [Build a confidential computing environment by using Enclave](https://www.alibabacloud.com/help/en/ecs/user-guide/build-a-confidential-computing-environment-by-using-enclave)
- [Confidential Computing" for Everyone: Getting Started with Occlum and Its Related Technologies](https://www.alibabacloud.com/blog/598671)
