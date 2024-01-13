# Confidential DVM
The goal of this research is to create [Data Vending Machines](https://www.data-vending-machines.org/) that are capable of interacting with confidential data, preventing the provider to ever see what is being worked on and at the same time giving the user the ability to provide the DVM with contextual information or sensitive data for processing. 

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
Reading materials:
- [Trusted Container Extensions for Container-based Confidential Computing ](https://arxiv.org/pdf/2205.05747.pdf)
- [Trusted execution environment](https://en.wikipedia.org/wiki/Trusted_execution_environment)
- [Confidential Containers](https://github.com/confidential-containers/)
- [Firecracker-microvm](https://firecracker-microvm.github.io/)
