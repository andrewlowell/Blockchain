import hashlib
import requests
import json
import sys


# TODO: Implement functionality to search for a proof 

def valid_proof(block_string, proof):
  guess = f"{block_string}{proof}".encode()
  guess_hash = hashlib.sha256(guess).hexdigest()
  return guess_hash[:3] == "000"

def proof_of_work(last_block):
  block_string = json.dumps(last_block, sort_keys=True).encode()
  proof = 0
  while not valid_proof(block_string, proof):
    proof += 1
  return proof



if __name__ == '__main__':
    # What node are we interacting with?
    # if len(sys.argv) > 1:
    #     node = sys.argv[1]
    # else:
    #     node = "http://localhost:5000"
    node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        r = requests.get(url=node + "/last_block")
        data = r.json()
        new_proof = proof_of_work(data.get('last_block'))

        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print(f"Mined {coins_mined} coins so far")
        else:
            print(data.get('message'))
