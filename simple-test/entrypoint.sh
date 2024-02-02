#!/bin/bash
./nak key generate
./nak event --kind 1 --content "enclave test $(date )" wss://relay.nostr.net