### prereqs
```
git clone https://github.com/gramineproject/gsc.
apt install python3-pip
pip install docker
```

### run 
```
./gsc build simple-nak test/generic.manifest
./gsc sign-image simple-nak /root/.config/gramine/enclave-key.pem
./gsc info-image gsc-simple-nak
docker run --device=/dev/sgx_enclave gsc-simple-nak



docker run --device=/dev/sgx_enclave --env GSC_PAL=Linux --security-opt seccomp=docker_seccomp_aug_2022.json gsc-simple-nak

```
