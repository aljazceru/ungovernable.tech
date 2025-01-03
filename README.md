Welcome to Ungovernable Tech. This started as a landing page for [my](https://nostr.at/aljaz@nostr.si) notes about research I was doing during the [Sovereing Engineering Cohort](https://sovereignengineering.io/) but I've decided to make it more structured and make it a bookmark page for all my research into freedom enabling technology.  Most topics are far from comprehensively covered, sadly I've decided to do this rather late so my notes and bookmarks are all over the place and in a need of free time to structure. Stay tuned. 


## Confidential computing

### [ConfidentialDVM](./ConfidentialDVM.md)
I wanted to create a PoC of confidential computing over nostr, I didn't end up finishing it but the notes about that experiment are [here](ConfidentailDVM.md). 

### [Confidential Computing in the Cloud](./ConfidentialComputingOnCloud.md)

#### Confidential computing on GPUs
- [continuum](https://docs.edgeless.systems/continuum)
- [confidential AI from GPU enclaves](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves)
- [Nvidia confidential computing deployment guide](https://docs.nvidia.com/confidential-computing-deployment-guide.pdf)
- [Building GPU TEEs using CPU Secure Enclaves with GEVisor](https://dl.acm.org/doi/pdf/10.1145/3620678.3624659)
- [Heterogeneous Isolated Execution for Commodity GPUs](https://insujang.github.io/assets/pdf/hix_slides.pdf)

### Confidential computing on CPUs:
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


##  [Decentralized  DNS](./DecentralizedDNS.md)
We are building all kinds of cool decentralized systems but keep forgetting that majority of them still relay on DNS which is very prone to seizure and manipulation. 

## [Decentralized compute](./DecentralizedCompute.md)
Most people have spare compute and bandwidth, at least the ones with desktop PCs and routers. Cryptography can remove the issues with trust models and makes every computer plugged into internet and power a productive asset.

## [Full Homomophic Encryption](./FullHomomorphicEncryption.md)
In a world where your private information is not for sale and your attention is not the product data is a liability not an asset. FHE can enable privacy preserving solutions for many/most database applications. 


## [Private Information Retrieval](./PrivateInformationRetrieval.md)
Fighting tyranny with math. Every company or individual is one court order away from needing to decide how long they are willing to spend behind bars for not sharing the data with the government. Designing systems that are default private and cryptographically sound makes sure you have nothing to share with them.



  For any suggestions or comments submit a [PR/open an issue](https://github.com/aljazceru/ungovernable.tech) or send smoke signals over nostr to [aljaz@nostr.si](https://nostr.at/aljaz@nostr.si)
