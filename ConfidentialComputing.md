#### GPU Confidential Computing
- [Stealth Cloud Confidential Computing Deep Dive](https://stealthcloud.ai/cloud-paradigms/confidential-computing-deep-dive/) - Technical overview of Intel TDX, AMD SEV-SNP, ARM CCA, attestation protocols, and hardware root of trust
- [Benchmarking Confidential Computing: TDX v/s SEV-SNP](https://www.computer.org/csdl/proceedings-article/hpcc/2025/687400a178/2bggrnRwZws) - 2025 IEEE HPCC paper comparing TDX and SEV-SNP performance on Azure
- [Confidential Computing in VMware Cloud Foundation 9.0](https://blogs.vmware.com/cloud-foundation/2025/08/06/confidential-computing-vmware-cloud-foundation-9-0/) - AMD SEV-SNP & Intel TDX workload isolation in VMware

#### Confidential computing on GPUs
- [TEE.Fail Side-Channel Attack](https://thehackernews.com/2025/10/new-teefail-side-channel-attack.html) - Extracts secrets from Intel SGX/TDX and AMD SEV-SNP with Ciphertext Hiding (October 2025)
- [Phala Confidential Computing Trends 2025](https://phala.com/learn/confidential-computing-trends-2025) - Gartner predicts 60% of enterprises will evaluate TEE by year-end, GPU TEE for AI workloads matures (2025)
- [continuum](https://docs.edgeless.systems/continuum)
- [confidential AI from GPU enclaves](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves)
- [Nvidia confidential computing deployment guide](https://docs.nvidia.com/confidential-computing-deployment-guide.pdf)
- [Building GPU TEEs using CPU Secure Enclaves with GEVisor](https://dl.acm.org/doi/pdf/10.1145/3620678.3624659)
- [Heterogeneous Isolated Execution for Commodity GPUs](https://insujang.github.io/assets/pdf/hix_slides.pdf)
- [Evaluating DeepSeek in Confidential Computing](https://arxiv.org/html/2502.11347v1) - Analyzing TEE impact on LLM inference efficiency
- [GPU Travelling for Confidential Collaborative Training](https://dl.acm.org/doi/10.1145/3719027.3765029) - Using confidential GPUs for privacy-preserving ML training
- [Red Hat: Enhancing AI inference security with confidential computing](https://next.redhat.com/2025/10/23/enhancing-ai-inference-security-with-confidential-computing-a-path-to-private-data-inference-with-proprietary-llms/) - Extending TEE boundary to GPUs
- [GPU-TEE-Papers](https://github.com/ConfidentialComputing/GPU-TEE-Papers) - Curated paper collection on CPU/GPU TEEs, NVIDIA H100 confidential computing, and GPU memory security

#### Confidential AI & Private Inference
- [Tinfoil](https://tinfoil.sh/) - Verifiably private AI inference platform using NVIDIA confidential computing GPUs and remote attestation
- [tinfoilsh/coco-inferencing](https://github.com/tinfoilsh/coco-inferencing) - Open-source confidential AI inference stack developed with Red Hat
- [mithril-security/blindai](https://github.com/mithril-security/blindai) - Confidential AI deployment framework for serving models inside secure enclaves
- [intel/confidential-computing-zoo](https://github.com/intel/confidential-computing-zoo) - Intel examples for confidential AI inference, SGX, TDX, HE, and remote attestation
- [microsoft/onnx-server-openenclave](https://github.com/microsoft/onnx-server-openenclave) - Open Enclave ONNX inference server with encryption and attestation support
- [NVIDIA Confidential Computing TDX Deployment Guide](https://docs.nvidia.com/cc-deployment-guide-tdx.pdf) - NVIDIA guide for deploying H100 confidential computing with Intel TDX

#### Confidential computing on CPUs:
- [confidential-containers/trustee](https://github.com/confidential-containers/trustee) - Attestation and secret-management components for Confidential Containers
- [krunvm](https://github.com/containers/krunvm) - CLI for creating microVMs with libkrun, including confidential virtualization workflows
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
- [edgelesssys/marblerun](https://github.com/edgelesssys/marblerun) - Control plane for confidential computing: deploy, scale, and verify confidential microservices on vanilla Kubernetes
- [ccc-spdm-tools/spdm-rs](https://github.com/ccc-spdm-tools/spdm-rs) - Rust implementation of the DMTF SPDM protocol for Confidential Computing device attestation
- [ccc-certifier-framework/certifier-framework-for-confidential-computing](https://github.com/ccc-certifier-framework/certifier-framework-for-confidential-computing) - Multi-vendor confidential computing certifier framework with policy-driven trust management
- [automata-network/amd-sev-snp-attestation-sdk](https://github.com/automata-network/amd-sev-snp-attestation-sdk) - AMD SEV-SNP attestation SDK: generate attestation reports and ZK proofs verifiable on-chain
- [automata-network/tdx-attestation-sdk](https://github.com/automata-network/tdx-attestation-sdk) - Intel TDX attestation SDK: generate TDX quotes and ZK proofs verifiable on-chain
- [gramineproject/gramine-tdx](https://github.com/gramineproject/gramine-tdx) - Gramine library OS with experimental Intel TDX support for multi-process applications
- [riscv/riscv-smmtt](https://github.com/riscv/riscv-smmtt) - RISC-V privilege ISA extensions for Supervisor Domain isolation (confidential computing, fault isolation)
- [google/cc-device-plugin](https://github.com/google/cc-device-plugin) - Kubernetes device plugin exposing Confidential Computing devices in GKE clusters
- [IntelLabs/tdx-workload-attestation](https://github.com/IntelLabs/tdx-workload-attestation) - Library for attesting VM workloads inside Intel TDX environments
- [Keystone Enclave](https://github.com/keystone-enclave/keystone) - Open-source TEE framework for RISC-V processors with customizable secure enclaves
- [intel/confidential-computing.tee.dcap.qvl](https://github.com/intel/confidential-computing.tee.dcap.qvl) - Intel TEE DCAP Quote Verification Library for ECDSA-based attestation
- [Intel TDX on IBM Cloud Frankfurt](https://community.ibm.com/community/user/blogs/meryl-veramonti/2025/10/14/intel-tdx-frankfurt) - Intel TDX now available on IBM Cloud in Frankfurt (October 2025)
- [Google Cloud Confidential Computing TDX](https://cloud.google.com/blog/products/identity-security/from-clicks-to-clusters-confidential-computing-expands-with-intel-tdx) - GKE nodes, Confidential Space, and GPU support for TDX
- [Intel SGX/TDX URL Migration (Nov 2025)](https://github.com/intel/confidential-computing.sgx/discussions/1093) - SGX repositories moving to intel/confidential-computing prefix

#### Oblivious RAM & Encrypted Storage
- [Oblivious Labs](https://www.obliviouslabs.com/) - Open source ORAM implementations used by Signal for private contact discovery
- [obliviouslabs/oram](https://github.com/obliviouslabs/oram) - Oblivious key-value store based on Circuit ORAM
- [obliviouslabs/benchmarks](https://github.com/obliviouslabs/benchmarks) - ORAM benchmarks comparing Signal and Meta implementations
- [mobilecoinfoundation/mc-oblivious](https://github.com/mobilecoinfoundation/mc-oblivious) - ORAM libraries for secure enclave applications
- [facebook/oram](https://github.com/facebook/oram) - Oblivious RAM implementation for secure enclave applications
- [Signal faster ORAM layer](https://signal.org/blog/building-faster-oram/) - Technical deep dive on Path ORAM for private contact discovery inside enclaves
- [Signal Contact Discovery Service](https://github.com/signalapp/ContactDiscoveryService) - Private contact discovery microservice that hides users' contact graphs from the server

#### Confidential computing in the cloud
##### Azure 
- [Onidel Cloud AMD SEV-SNP vs Intel TDX](https://onidel.com/blog/amd-sev-snp-vs-intel-tdx-vps) - 2025 comparison guide for VPS isolation and performance
- [Azure confidential enclave nodes on AKS](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-enclave-nodes-aks-get-started) - CLI guide for deploying confidential enclave nodes on AKS
- [Gramine AKS attestation example](https://github.com/gramineproject/contrib/tree/master/Examples/aks-attestation) - Example for running Gramine workloads with Azure Kubernetes attestation
- [Azure confidential containers enclaves](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-containers-enclaves) - Azure documentation for confidential containers with enclave-aware providers

##### AWS
- [Nitro enclaves](https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html)

##### GCP
- [Confidential Computing](https://cloud.google.com/security/products/confidential-computing)

##### Alibaba 
- [Build a confidential computing environment by using Enclave](https://www.alibabacloud.com/help/en/ecs/user-guide/build-a-confidential-computing-environment-by-using-enclave)
- [Confidential Computing" for Everyone: Getting Started with Occlum and Its Related Technologies](https://www.alibabacloud.com/blog/598671)
