import zmq
import json
import base64

def main():
    """Sets up the ZeroMQ client and sends test requests."""
    
    context = zmq.Context()
    print("Connecting to the microservice...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Test 1:
    print("\n--- TEST 1: Requesting new keys ---")
    generate_request = {"type": "generate_keys"}
    print(f"Sending request: {generate_request}")
    socket.send_json(generate_request)

    response = socket.recv_json()
    print(f"Received response: {response}")

    if "error" in response:
        print("Test 1 Failed: Received an error.")
        return
        
    rsa_public_key = response["rsa"]["public"]
    rsa_private_key = response["rsa"]["private"]
    original_fernet_key = response["fernet"]
    print("Test 1 Passed. Keys received.")


    # Test 2:
    print("\n--- TEST 2: Requesting to encrypt the Fernet key ---")
    encrypt_request = {
        "type": "encrypt_fernet",
        "fernet": original_fernet_key,
        "rsa_public": rsa_public_key
    }
    print(f"Sending request: {json.dumps(encrypt_request, indent=2)}")
    socket.send_json(encrypt_request)

    response = socket.recv_json()
    print(f"Received response: {response}")
    
    if "error" in response:
        print("Test 2 Failed: Received an error.")
        return

    encrypted_fernet = response["encrypted_fernet"]
    print("Test 2 Passed. Encrypted key received.")


    # Test 3
    print("\n--- TEST 3: Requesting to decrypt the Fernet key ---")
    decrypt_request = {
        "type": "decrypt_fernet",
        "encrypted_fernet": encrypted_fernet,
        "rsa_private": rsa_private_key
    }
    print(f"Sending request: {json.dumps(decrypt_request, indent=2)}")
    socket.send_json(decrypt_request)

    response = socket.recv_json()
    print(f"Received response: {response}")

    if "error" in response:
        print("Test 3 Failed: Received an error.")
        return
        
    decrypted_fernet_key = response["fernet"]
    print("Test 3 Passed. Decrypted key received.")

    # Verification
    print("\n--- VERIFICATION ---")
    print(f"Original Fernet key:  {original_fernet_key}")
    print(f"Decrypted Fernet key: {decrypted_fernet_key}")
    if original_fernet_key == decrypted_fernet_key:
        print("You Win! Decrypted key matches the original key.")
    else:
        print("You LOSE! You get nothing! (Decrypted key does not match the original.)")


if __name__ == "__main__":
    main()