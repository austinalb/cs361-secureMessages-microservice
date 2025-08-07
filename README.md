Sprint 2 Microservice: Communication Contract Microservice: Key Generator for Secure Messenger This microservice provides cryptographic key generation and management functionalities for the "Secure Messenger" desktop application my groupmate Tristan is working on. It operates independently and communicates over a ZeroMQ messaging pipe.

Dependencies Before running this microservice or attempting to communicate with it, you must install the required Python libraries using the following command:

pip install pyzmq rsa cryptography

Communication Contract This section outlines the established protocol for programmatic interaction with the microservice. This contract is considered stable and should not be altered, as the main client application depends on this specific implementation.

Communication Protocol: ZeroMQ REQ/REP Socket Pattern

Network Address: tcp://localhost:5555

Data Serialization Format: All data exchanged between the client and the microservice must be serialized into single JSON objects.

Programmatic Data Requests A client application initiates a transaction by sending a structured JSON object to the microservice. The type field within this object dictates the operation to be performed.

Generate Keys This operation instructs the microservice to generate a complete set of cryptographic keys for a new secure session. This includes a 2048-bit RSA asymmetric key pair (public and private) and a Fernet symmetric key.
Example Call:

{ "type": "generate_keys" }

Encrypt Fernet Key This operation is used to securely prepare the symmetric Fernet key for transmission. It encrypts the Fernet key using the recipient's public RSA key, ensuring that only the recipient (who holds the corresponding private key) can decrypt it.
Example Call:

{ "type": "encrypt_fernet", "fernet": "", "rsa_public": "" }

Decrypt Fernet Key This operation recovers the original Fernet key from a ciphertext. The client provides the encrypted Fernet key and its private RSA key, and the microservice performs the decryption.
Example Call:

{ "type": "decrypt_fernet", "encrypted_fernet": "", "rsa_private": "" }

Programmatic Data Reception Upon successfully processing a request, the microservice returns a single JSON object containing the results of the operation.

Response for generate_keys The response contains the newly generated RSA public key, RSA private key, and the Fernet key, all formatted for immediate use or storage.
Example Response:

{ "rsa": { "public": "-----BEGIN RSA PUBLIC KEY-----\n...\n-----END RSA PUBLIC KEY-----", "private": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----" }, "fernet": "b64_encoded_string_of_fernet_key" }

Response for encrypt_fernet The response payload consists of the base64-encoded ciphertext, which is the result of encrypting the Fernet key.
Example Response:

{ "encrypted_fernet": "b64_encoded_string_of_encrypted_fernet_key" }

Response for decrypt_fernet The response contains the original Fernet key after it has been successfully decrypted from the provided ciphertext.
Example Response:

{ "fernet": "b64_encoded_string_of_fernet_key" }

![UML Sequence Diagram](1Capture.PNG)
