# Plume Network
## 项目说明
1. Plume 是专为所有现实世界资产 (RWA) 打造的模块化 L2 区块链，将资产代币化和合规提供商直接集成到链中。其使命是简化 RWA 项目部署的复杂流程，并为投资者提供一个区块链生态系统，以相互交流和投资各种 RWA。此外，Plume 通过其蓬勃发展的 DeFi 应用程序实现 RWA 可组合性，并提供优质买家渠道，以增加所有代币化 RWA 的流动性。
2. 明确是激励测试网

## 脚本配置说明
1. wallet.json
撸毛钱包配置。
```json
[
  {
    "env": 1,
    "address": "钱包地址",
    "private_key": "钱包私钥",
    "proxy": "代理地址"
  },
  {
    "env": 2,
    "address": "钱包地址",
    "private_key": "钱包私钥",
    "proxy": "代理地址"
  }
]
```
代理地址的作用：在领水时需要指定代理IP。可以是固定IP，也可以是非固定IP。  
代理网站的话，可以从这里购买：https://app.proxy-cheap.com/r/IAFX8J
注册之后，购买4.99美金 1G的计划，1G够你用很久了。
买了之后，在【My Proxies】的菜单栏内，点击【Credentials Generator】凭证生成器里面，点击【Setup Credentials】，然后复制【Curl Example】内的一串链接，例：http://9xmb93yh:xxxxxxxx@proxy.proxy-cheap.com:31112
然后将这串链接填到 wallet.json 的Proxy中。

## 执行步骤
```python
python3 plume.py
```
plume.py目前可执行的项目如下：
1. 签到
2. 领水
3. ambient
4. arc
5. cultured
6. kuma
7. landshare
8. neststaking

## TODO
1. SolidViolet
2. BukProtocol
3. Silver Koi