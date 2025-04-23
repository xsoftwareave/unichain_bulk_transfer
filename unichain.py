# -*- coding: utf-8 -*-
# @Author: xsoftwareave
import random
import time
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from web3 import Web3


def generate_private_key(mnemonic, address_index):
    # 生成种子
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    # 初始化 BIP44 钱包对象
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    # 派生地址和私钥
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(address_index)
    address = bip44_acc.PublicKey().ToAddress()
    private_key = bip44_acc.PrivateKey().Raw().ToHex()
    private_key = '0x' + private_key
    return address, private_key


def transfer(from_pvk, to_addr, amount):
    unichain_rpc = "https://unichain.drpc.org"
    w3 = Web3(Web3.HTTPProvider(unichain_rpc))
    account = w3.eth.account.from_key(from_pvk)
    from_address = account.address
    # 获取 nonce
    nonce = w3.eth.get_transaction_count(from_address)
    # 获取当前 gas price（单位是 wei）
    gas_price = w3.eth.gas_price
    # 标准转账
    gas_limit = 21000
    # 构造交易
    tx = {
        "from": from_address,
        "to": to_addr,
        "value": w3.to_wei(amount, "ether"),
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
    }
    # 签名
    signed_tx = w3.eth.account.sign_transaction(tx, from_pvk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"[+] Sent from {from_address} to {to_addr} | tx hash: 0x{tx_hash.hex()}")
    # 可选：等待确认
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[✓] Confirmed: 0x{receipt.transactionHash.hex()} | Block: {receipt.blockNumber}\n")


if __name__ == "__main__":
    wallet_mnemonic = "这里换成你的钱包助记词，空格分隔"
    transfer_to_address = '0xA3EB2b5d7A550a838000e498a31329be295113ca'
    transfer_amount = 0
    main_account_address, main_account_private_key = generate_private_key(wallet_mnemonic, 0)
    # 默认使用钱包的第一个地址作为主账户，用于分配 unichain_eth 给其他 999 个账户
    distribute_amount = 0.000002
    for i in range(1, 1000):
        slave_account_address, slave_account_private_key = generate_private_key(wallet_mnemonic, i)
        try:
            # 从主账户 transfer 0.000002 个 unichain_eth 给其他账户做 gas 用
            transfer(main_account_private_key, slave_account_address, distribute_amount)
            # random sleep to avoid sybil
            time.sleep(random.randint(1, 10))
            # 从其他账户 transfer 0 个 unichain_eth 给 UniPony 项目地址
            transfer(slave_account_private_key, transfer_to_address, transfer_amount)
        except Exception as e:
            print(f"[!] Error: {e}")
