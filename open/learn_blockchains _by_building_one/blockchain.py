import hashlib
import json
from time import time


"""
每个区块存储的信息像这样：
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
"""


class Blockchain(object):

    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # 创建创世块
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # 创建新的区块，添加到链
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 重制交易链
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # 添加一个交易到交易链
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # 返回链上的最后一个区块
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # 对区块进行哈希，创建一个区块的SHA-256哈希
        # 提示：在 Python 中（特别是 3.7 之前），普通字典（dict）的键值对顺序是不确定的。如果
        # 对同一个数据但不同顺序的字典进行哈希计算，会得到不同的哈希结果。
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        简单的工作量证明算法
        - 找到一个数字p‘，使得hash(pp')包含4个前导0，p是前一个证明，p‘是一个新的证明
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        验证这个证明，hash(pp')是否包含4个前导0
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
