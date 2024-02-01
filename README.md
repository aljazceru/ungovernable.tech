# Confidential DVM
The goal of this research is to create [Data Vending Machines](https://www.data-vending-machines.org/) that are capable of interacting with confidential data, preventing the provider to ever see what is being worked on and at the same time giving the user the ability to provide the DVM with contextual information or sensitive data for processing. 

Currently the only way to process confidential data is to either:
- give up the privacy
- run it locally

One is potentially viable but you need access to the hardware and models, the other is just nuts. While you can process a lot of things locally on consumer hardware your needs might be bigger or just occasional where you can't build a cluster at home. The other issue is that you can't rent an algorithm (model) for one run. Confidential computing is the third way. Both parties provide their part (model & data) to an encrypted blob called a virtual machine and the owner of the data gets the encrypted result. There are still some trust assumptions to solve. 

Ideally for maximum privacy you'd push the entire VM to the provider but that can be a bit heavy on the overhead, hence the exploration of solving this with confidential containers and DVMs. 

## Use cases
- providing sensitive data as RAG to an LLM
- analyzing confidential data

## Currnet high level thinking
1) Deploy a new confidential container for each job
2) Establish secure communication channel with the user
   - create a one time nsec within the container and contact the user with
   - TO-DO: you can't trust it if it can't be verifyably secure
   - TO-DO: can we do attestation this way?
3) Gather the data
   - DM route:
     - user can send information to the container via DMs
     - user can interact with the container via DMs
   - Other route that is more DVM appropriate
     - DVM needs to pass the secure channel to the user
5) Execute the job
   - deliver the result to the user over secure channel
6) Destroy the VM

## Potential issues
- [confidential containers](https://github.com/confidential-containers/confidential-containers/) don't (fully) support attestation yet
- you need an attestation service running in a trusted env to be able to ensure confidentiality
- GCP doesn't support Confidential nodes with GPUs
- GPU enclaves only possible on H100 + AMD SEV 

## Reading materials:
- [Trusted Container Extensions for Container-based Confidential Computing](https://arxiv.org/pdf/2205.05747.pdf)
- [Trusted execution environment](https://en.wikipedia.org/wiki/Trusted_execution_environment)
- [Confidential Containers](https://github.com/confidential-containers/)
- [Firecracker-microvm](https://firecracker-microvm.github.io/)
- [Confidential computing](https://en.wikipedia.org/wiki/Confidential_computing)
- [Kata containers](https://katacontainers.io/)
- [awesome-zama](https://github.com/zama-ai/awesome-zama)
- [zama.ai](https://www.zama.ai/)
- [confidential AI from GPU enclaves](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves)
- [Remote attestation Procedures Architecture](https://ietf-rats-wg.github.io/architecture/draft-ietf-rats-architecture.html)
- [Trusted Execution Environment Provisioning (TEEP) Architecture](https://datatracker.ietf.org/doc/html/draft-ietf-teep-architecture-19)
- [CoCo attestation proposal KBS / AS](https://github.com/confidential-containers/confidential-containers/issues/119)
- [Generic Key Broker System for CoCo](https://github.com/confidential-containers/confidential-containers/issues/68)
- [Nvidia confidential computing deployment guide](https://docs.nvidia.com/confidential-computing-deployment-guide.pdf)
- [Building GPU TEEs using CPU Secure Enclaves with GEVisor](https://dl.acm.org/doi/pdf/10.1145/3620678.3624659)
- [Constellation - Always encrypted kubernetes](https://github.com/edgelesssys/constellation?tab=readme-ov-file)
- [Garmine Shielded Containers](https://github.com/gramineproject/gsc)
- [Confidential containers in kubernetes](https://archive.is/u1vhR)
- [Garmine library OS - run applications in enclaves](https://github.com/gramineproject/gramine/tree/master?tab=readme-ov-file)
- [Heterogeneous Isolated Execution for Commodity GPUs](https://insujang.github.io/assets/pdf/hix_slides.pdf)
- [COCONUT Secure VM Service Module](https://github.com/coconut-svsm/svsm)
- [enclavie](https://github.com/enclaive)
- [List of SGX supported Intel CPUs](https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html)
