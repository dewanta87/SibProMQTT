# SibProMQTT

The SibProMQTT is an approach to protect MQTT communication from any Sybil Attack that can cause invalid message reception from unverified entities.
The SibProMQTT works by
- Checking freshness of the MQTT message
- Checking correctness of the MQTT message
- Concealing private information by means of AES encryption

At current state, this source code is only applied for AES encryption with CBC mode and certain hash functions (SHA1, SHA256, SHA384, SHA512, MD5). 
To run this simulation, the following packages should be installed previously:
- pycryptodome
- base64
- hashlib

After installing those packages, the simulation can be conducted as follows.
```sh
python SibProMQTT_simulation.py
``` 
or
```sh
python3 SibProMQTT_simulation.py
``` 
