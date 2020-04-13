from common import *
import base64


####file encrypt part
def encrpty_file(file_path, pubkey):
    log.debug("-------")
    cipher_text = b''
    max_length = int(get_max_length(pubkey))
    if pubkey:
        cipher_public = Crypto.Cipher.PKCS1_v1_5.new(pubkey)
        with open(file_path, 'r') as f:
            while True:
                message = f.read(max_length)
                print(message)
                if message != "":
                    #cipher_text = cipher_text + base64.b64encode(cipher_public.encrypt(message.encode('utf-8')))
                    cipher_text = cipher_text + cipher_public.encrypt(message.encode(encoding='utf-8'))
                else:
                    break
                

        # update file
        with open(file_path, 'wb') as f:
            f.write(base64.b64encode(cipher_text))

        with open(file_path, 'rb') as f:
            message = f.read()
        #log.log_raw(message)
    else:
        win32api.MessageBox(0, "error", "Error",win32con.MB_ICONWARNING)
        return False
    return True

###start
# Create the blockchain and add the genesis block
def block_chain_flow():
    #private_key = get_key.get_private_key_bytes()
    private_key = get_key.get_private_key_strs()
    ## store key @ block 0
    blockchain = [create_genesis_block(private_key)]
    previous_block = blockchain[0]
    blockchain_len = 1

    a = input("are you want to add another device? y :yes  n :No:")
    while True:
        if (a == 'y'):
            mac_id = input("input your mac_id, please input numbers only")
            block_to_add = next_block(previous_block, mac_id)
            blockchain.append(block_to_add)
            previous_block = block_to_add
            blockchain_len = blockchain_len + 1
            a = input("are you want to add another device? y :yes  n :No:")
        else:
            log.log_out("add done，blocks below:")
            for i in range(0, blockchain_len):
                log.debug("Block %s has been added to the blockchain!" %format(blockchain[i].index))
                log.debug("previous hash:")
                log.debug(blockchain[i].previous_hash)
                log.debug("Hash: %s\n" %format(blockchain[i].hash))
            break

    save_blockchain(blockchain, blockchain_len)
    ## block chain check
    check = block_chain_check(blockchain, blockchain_len)

    if check:
        pubkey = get_key.get_public_key()
        if pubkey:
            encrpty_file(file_need_encrpty_test, pubkey)
            log.log_out("file encrpty done! file:" + file_need_encrpty_test)
    else:
        log.debug("check fail")
        return False

if __name__ == "__main__":
    block_chain_flow()
