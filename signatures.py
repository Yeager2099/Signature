from web3 import Web3
import eth_account
from eth_account.messages import encode_defunct

def sign(m):
    w3 = Web3()
    
    # 创建一个新的以太坊账户
    account = eth_account.Account.create()
    public_key = account.address  # 账户地址作为公钥
    private_key = account.key     # 账户私钥
    
    # 对消息进行编码以便签名
    message = encode_defunct(text=m)
    # 使用私钥对消息进行签名
    signed_message = eth_account.Account.sign_message(message, private_key=private_key)

    """You can save the account public/private keypair that prints in the next section
     for use in future assignments. You will need a funded account to pay gas fees for 
     several upcoming assignments and the first step of funding an account is having 
     an account to send the funds too.
    """
    print('Account created:\n'
          f'private key={w3.to_hex(private_key)}\naccount={public_key}\n')
    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)
    # print(f"signed message {signed_message}\nr= {signed_message.r}\ns= {signed_message.s}")

    return public_key, signed_message

def verify(m, public_key, signed_message):
    w3 = Web3()
    
    # 对消息进行编码以便验证
    message = encode_defunct(text=m)
    # 从签名中恢复出签名者的地址
    signer = eth_account.Account.recover_message(
        signable_message=message,
        signature=signed_message.signature
    )
    # 检查恢复的地址是否与提供的公钥(地址)匹配
    valid_signature = signer == public_key

    assert isinstance(valid_signature, bool), "verify should return a boolean value"
    return valid_signature

if __name__ == "__main__":
    import random
    import string

    for i in range(10):
        m = "".join([random.choice(string.ascii_letters) for _ in range(20)])

        pub_key, signature = sign(m)

        # Modifies every other message so that the signature fails to verify
        if i % 2 == 0:
            m = m + 'a'

        if verify(m, pub_key, signature):
            print("Signed Message Verified")
        else:
            print("Signed Message Failed to Verify")
