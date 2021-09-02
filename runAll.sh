# compile all
solc contracts/*.sol --bin --abi --hashes --metadata-hash none --optimize -o contracts/out --overwrite
# manipulate all bytecodes
python3 POC.py contracts/out/Prime.bin contracts/out/Prime.bin.patched 45b43a84
python3 POC.py contracts/out/CoPrime.bin contracts/out/CoPrime.bin.patched 45b43a84
python3 POC.py contracts/out/SortedArray.bin contracts/out/SortedArray.bin.patched 45b43a84
python3 POC.py contracts/out/SymmetricMatrix.bin contracts/out/SymmetricMatrix.bin.patched 45b43a84
echo ""
echo "Modified the bytecode of all example contracts."
echo ""
echo "Run tests:"
# test all
# parameters always need to be given as a list that contains no spaces (via -p)
echo ""
echo " === Prime ==="
python3 TestContract.py contracts/out/Prime -p "[39]" -s -i 32 -t 0x2000000000000000000000000000000000000000000000000000000000000000
echo ""
echo " === CoPrime ==="
python3 TestContract.py contracts/out/CoPrime -p "[36, 24]" -s -i 32 -t 0x2000000000000000000000000000000000000000000000000000000000000000
echo ""
echo " === SortedArray ==="
python3 TestContract.py contracts/out/SortedArray -p "[[1, 2, 3, 4, 5, 6, 8, 7, 20, 24, 22, 34, 55]]" -s -i 32 -t 0x2000000000000000000000000000000000000000000000000000000000000000
echo ""
echo " === SymmetricMatrix ==="
python3 TestContract.py contracts/out/SymmetricMatrix -s -i 32 -t 0x2000000000000000000000000000000000000000000000000000000000000000 -p "[[\
[1, 4, 5, 2],\
[2, 1, 0, 2],\
[3, 0, 1, 0],\
[2, 2, 0, 1]\
]]"
# remove vandal output
rm -rf vo
