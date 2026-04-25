#### NIST Post-Quantum Standards
- [FIPS 203: ML-KEM](https://csrc.nist.gov/pubs/fips/203/final) - Module-Lattice-Based Key-Encapsulation Mechanism (formerly CRYSTALS-Kyber)
- [FIPS 204: ML-DSA](https://csrc.nist.gov/pubs/fips/204/final) - Module-Lattice-Based Digital Signature Algorithm (formerly CRYSTALS-Dilithium)
- [FIPS 205: SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) - Stateless Hash-Based Digital Signature Algorithm (formerly SPHINCS+)
- [FIPS 206: FN-DSA](https://csrc.nist.gov/pubs/fips/206/final) - FFT over NTRU-Lattice-Based Digital Signature Algorithm (formerly FALCON)
- [NIST PQC Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography) - Official NIST post-quantum cryptography project page

#### Open Source Implementations
- [liboqs](https://github.com/open-quantum-safe/liboqs) - C library for quantum-safe cryptographic algorithms (Open Quantum Safe project)
- [PQClean](https://github.com/pqclean/PQClean) - Clean, portable, reference implementations of post-quantum schemes
- [PQ Code Package](https://github.com/pq-code-package) - Maintained successor to PQClean for NIST-standardized PQC schemes
- [Open Quantum Safe](https://openquantumsafe.org/) - Project integrating PQC into TLS, SSH, and other protocols via liboqs
- [pqcrystals/kyber](https://github.com/pq-crystals/kyber) - Reference implementation of ML-KEM (Kyber)
- [pqcrystals/dilithium](https://github.com/pq-crystals/dilithium) - Reference implementation of ML-DSA (Dilithium)
- [OpenSSL 3.5 PQC](https://cfp.openssl-conference.org/openssl-conference-2025/talk/8X8YTF/) - Post-quantum TLS 1.3 integration in OpenSSL (Kyber, Dilithium)

#### Hybrid Key Exchange
- [X25519Kyber768 in TLS](https://www.ietf.org/archive/id/draft-tls-westerbaan-xyber768d00-02.html) - Hybrid post-quantum key exchange for TLS 1.3 (deployed in Chrome)
- [Chrome PQC Deployment](https://chromestatus.com/feature/5257822742249472) - Chrome's X25519Kyber768 key encapsulation for TLS
- [RFC 9180: HPKE](https://www.rfc-editor.org/rfc/rfc9180) - Hybrid Public Key Encryption (extensible to PQC KEMs)

#### Migration & Compliance
- [NSA CNSA 2.0](https://www.nsa.gov/Press-Room/Cybersecurity-Advisories-Guidance/) - CNSA 2.0 Suite requirements for national security systems (ML-KEM-1024, ML-DSA-87)
- [PQCC International Requirements](https://pqcc.org/international-pqc-requirements/) - Global PQC migration requirements and timelines
- [NIST SP 800-227](https://csrc.nist.gov/pubs/sp/800/227/ipd) - Recommendations for key-encapsulation mechanisms

#### Research & Analysis
- [Inside NIST's PQC](https://postquantum.com/post-quantum/nists-pqc-technical/) - Technical deep-dive into Kyber, Dilithium, and SPHINCS+
- [Meta-analysis of PQC Finalists](https://emerginginvestors.org/articles/23-233/pdf) - Performance and security comparison of NIST-endorsed algorithms
- [Palo Alto PQC Guide](https://www.paloaltonetworks.com/cyberpedia/pqc-standards) - Enterprise guide to PQC standards and migration strategy
