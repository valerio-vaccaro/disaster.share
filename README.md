# Disaster.share
Share long messages, file and Bitcoin transactions using [disaster.radio]() mesh
 network.

The idea is to user a standard firmware to broadcast messages using the disaster radio lora mesh and create a layer on top of it able to broadcast multipart messages (bigger than maximum payload) with a check

This is just a prototype

## Protocol
The protocol is very simple, a long binary message will be converted in base64
and split in N chunks of MAX_SIZE (in our implementation 200 bytes).

Every chunk will be transmitted in a package with the following format:
`ID:HASH:M:N:PAYLOAD` where:

| Element| Size          | Description                                               |
|--------|---------------|-----------------------------------------------------------|
| ID     | variable size | is the magic number associated with the service           |
| HASH   | 4 bytes       | are the first 2 bytes in hex of the complete message hash |
| M      | variable size | is the progressive number of the chunk                    |
| N      | variable size | is the total number of chunks present in the message      |

The receiver will wait to receive all packages before print the complete message.

## Usage
Scripts are based on python language.

### Send a message
`python3 da-sender.py`

### Receive a message
`python3 da-receiver.py`
