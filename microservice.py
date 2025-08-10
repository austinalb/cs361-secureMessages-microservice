import zmq
import json
import rsa
import base64
from cryptography.fernet import Fernet

def main():
    """Sets up the ZeroMQ server and listens for requests."""
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Microservice started. Listening on port 5555...")


    try:
        while True:
            message = socket.recv_json()
            print(f"Received request: {message}")

            request_type = message.get("type")
            response = {}

            # User Story 1: Generate Keys
            if request_type == "generate_keys":
                (public_key, private_key) = rsa.newkeys(2048)
                fernet_key = Fernet.generate_key()

                response = {
                    "rsa": {
                        "public": public_key.save_pkcs1().decode('utf-8'),
                        "private": private_key.save_pkcs1().decode('utf-8')
                    },
                    "fernet": fernet_key.decode('utf-8')
                }
                print("Generated new RSA and Fernet keys.")

            # User Story 2: Encrypt Fernet Key
            elif request_type == "encrypt_fernet":
                fernet_key_b64 = message["fernet"]
                rsa_public_pem = message["rsa_public"]

                fernet_key_bytes = fernet_key_b64.encode('utf-8')
                public_key = rsa.PublicKey.load_pkcs1(rsa_public_pem.encode('utf-8'))
                encrypted_fernet = rsa.encrypt(fernet_key_bytes, public_key)
                
                response = {
                    "encrypted_fernet": base64.b64encode(encrypted_fernet).decode('utf-8')
                }
                print("Encrypted Fernet key.")

            # User Story 3: Decrypt Fernet Key
            elif request_type == "decrypt_fernet":
                encrypted_fernet_b64 = message["encrypted_fernet"]
                rsa_private_pem = message["rsa_private"]
                encrypted_fernet_bytes = base64.b64decode(encrypted_fernet_b64)
                private_key = rsa.PrivateKey.load_pkcs1(rsa_private_pem.encode('utf-8'))
                
                decrypted_fernet = rsa.decrypt(encrypted_fernet_bytes, private_key)

                response = {
                    "fernet": decrypted_fernet.decode('utf-8')
                }
                print("Decrypted Fernet key.")

            else:
                response = {"error": "Invalid request type"}
                print(f"Error: Invalid request type '{request_type}'")
            
            socket.send_json(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        error_response = {"error": str(e)}
        socket.send_json(error_response)
        socket.close()
        context.term()
        exit(1)

    except KeyboardInterrupt:
        print("Keyboard interrupted received. Exiting.")
        socket.close()
        context.term()
        exit(1)


if __name__ == "__main__":
    main()