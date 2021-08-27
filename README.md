# EVM-PoW
An EVM -> EVM transpiler that adds operations, which compute a hash unique to the executed code of a function.
This hash can be used to incentivize the execution of some code using Proof of Work.

## Installation
Clone with `--recurse-submodules` to download vandal as well:

`git clone https://github.com/alexanderpfefferle/EVM-PoW.git --recurse-submodules`

Install python packages required for vandal:

`python3 -m pip install -r vandal/requirements.txt`

Install python packages required for testing contracts:

`python3 -m pip install -r requirements.txt`

To test the contracts you will need to set the `PRIVKEY` environment variable to a private key which corresponds to an address that has enough Ether to deploy the contracts/execute the transactions. (0.5 ETH should be enough)

You also need to set `WEB3PROVIDER` to a web3 http provider, this could be a local node or a service like infuria/alchemy.

The contracts are already compiled, if you want to recompile them you need to install solc 0.8.7 or newer as well:
```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```

## Example Contracts
There are 4 different example contracts, which got compiled, modified and deployed:
+ [Prime](contracts/Prime.sol) deployed on [Rinkeby](https://rinkeby.etherscan.io/address/0x4fb1081515adb5ac2a2380a44f78998cd0c30d13) with parameter `39`
+ [CoPrime](contracts/CoPrime.sol) deployed on [Rinkeby](https://rinkeby.etherscan.io/address/0x8efa60b96ce2d8a52f5de721ab9e48771f14379c) with parameter `36, 24`
+ [SortedArray](contracts/SortedArray.sol) deployed on [Rinkeby](https://rinkeby.etherscan.io/address/0xd854ebd94333d6b53827f9e6ab80b4d6b749710d) with parameter `[1, 2, 3, 4, 5, 6, 8, 7, 20, 24, 22, 34, 55]`
+ [SymmetricMatrix](contracts/SymmetricMatrix.sol) deployed on [Rinkeby](https://rinkeby.etherscan.io/address/0x6d185fb1f48f594480c256be4b8237ed7cc8fbf2) with parameter 

```
[[1, 4, 5, 2],
 [2, 1, 0, 2],
 [3, 0, 1, 0],
 [2, 2, 0, 1]]
```
All of these have `0x2000000000000000000000000000000000000000000000000000000000000000` as target and it's possible to find counterexamples for the given parameters.

You will find 2 transactions to each of these contracts, one to get the PoW reward and one to get the bounty for the counterexample.
