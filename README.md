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
