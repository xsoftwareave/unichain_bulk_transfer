# unichain_bulk_transfer
## 介绍
1. 该脚本主要用于参与 UniPony 项目 2025.04.23 推出的转账活动 [https://x.com/Uni_Pony_/status/1914702042041606162]
2. 该脚本会自动从钱包主账户分配少量 Unichain ETH 给其他 999 个账户做 Gas，然后自动 transfer 0 个 Unichain ETH 给 UniPony 项目地址。
## 使用方法
1. 先创建一个全新的 OKX 钱包，OKX 会自动创建一个「Account 01」，记下钱包助记词。
2. 从中心化交易所或者其他钱包转一点 Unichain 上的 ETH 到第一步默认创建的「Account 01」。
3. 修改 unichain.py 脚本里的「wallet_mnemonic」，填入第一步记录的钱包助记词，一共 12 个单词，用空格分隔。
4. 执行 pip install -r requirements.txt 安装脚本用到的 Python Module。
5. 最后执行 python3 unichain.py 即可。
## 注意事项
1. 本脚本仅供技术研究，请勿滥用。
2. 建议创建新钱包使用该脚本。
3. 目前默认分配其他账户的 Unichain ETH 数量是 0.000002 个，如果随着 Gas 费升高不足以覆盖转账消耗，可以自行提高。
