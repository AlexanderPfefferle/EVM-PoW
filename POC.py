import argparse
from opcodes import *

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Modify EVM Bytecode such that it computes a hash unique to the executed code.")
    arg_parser.add_argument("inputfile")
    arg_parser.add_argument("outputfile")
    arg_parser.add_argument("functionhash")
    args = arg_parser.parse_args()

bytecode = open(args.inputfile).read().strip().upper()

funcsighash=args.functionhash.upper()
# assumes solc gets executed with "--metadata-hash none", you would need a CBOR parser,
# to handle arbitrary metadata at the end, https://docs.soliditylang.org/en/v0.8.5/metadata.html
metadata_bytes = "a164736f6c6343".upper()
begin_metadata_bytes = bytecode.find(metadata_bytes,0)

bytecode=bytecode[:begin_metadata_bytes]

set_leading_zeros = lambda x: "{0:0{1}x}".format(x,4).upper()

byte_array = [bytecode[i]+bytecode[i+1] for i in range(0,len(bytecode)-1,2)]

lbl_index=0
jumpdests=[]
pushes=[]


c=0
p=[]
i=0

old_address_to_label=dict()

# disassemble
while c<len(byte_array):
    op=byte_array[c]
    extra=opcodes[op]["extra_in"]
    params=byte_array[c+1:c+1+extra]
    p+=[[op, params, None]]
    c+=extra+1
    i+=1+len(params)

# find index to split code from constructor
i=0
constructor_length=None
constructor_end_index=None
for x in range(len(p)):
    if opcodes[p[x][0]]["name"]=="CODECOPY":
        constructor_length=int(''.join(p[x-2][1]),16)
    i+=1+len(p[x][1])

i=0
for x in range(len(p)):
    if i==constructor_length:
        constructor_end_index=x
        break
    i+=1+len(p[x][1])

p, constructor = p[constructor_end_index:], p[:constructor_end_index]

# move initial FMP
p[0][1]=["C0"]

# reassemble
def reassemble(p):
    new_bytecode=""
    new_jump_dests=dict()
    i=0
    # find new lbl positions
    for x in range(len(p)):
        op,params,lbl=p[x]
        if lbl and opcodes[op]["name"] == "JUMPDEST":
            new_jump_dests[lbl]=i
        i+=1+len(params)
    i=0
    # adjust pushes to the correspd lbl
    for x in range(len(p)):
        op,params,lbl=p[x]
        new_bytecode += op
        if lbl and opcodes[op]["name"] != "JUMPDEST":
            new_bytecode += set_leading_zeros(new_jump_dests[lbl])
        else:
            new_bytecode += ''.join(params)
    return new_bytecode

import os
os.system('(echo "%s" | vandal/bin/decompile -t vo -n -v) > /dev/null 2>&1'%reassemble(p))

# find jump dests, assign them labels
i=0
for x in range(len(p)):
    op,params,_ = p[x]
    if opcodes[op]["name"]=="JUMPDEST":
        p[x][2]="LBL%d"%lbl_index
        old_address_to_label[i]="LBL%d"%lbl_index
        lbl_index+=1
    i+=1+len(params)


unsolved_jump_pcs=[]

# assign labels to static jumps
i=0
for x in range(1,len(p)):
    p_op,p_params,p_lbl = p[x-1]
    op,params,lbl = p[x]
    if (opcodes[op]["name"] in {"JUMP", "JUMPI"}):
        if opcodes[p_op]["name"][:4] == "PUSH":
            p[x-1][2]=old_address_to_label[int(''.join(p_params),16)]
        else:
            unsolved_jump_pcs+=[i+1]
    i+=1+len(p_params)

# fix dynamic jumps
from vandal_parser import *
unsolved_push_pcs=[]
for x in unsolved_jump_pcs:
    unsolved_push_pcs+=jumppc_to_pushpc(x)

i=0
for x in range(0,len(p)):
    op,params,lbl = p[x]
    if i in unsolved_push_pcs:
        unsolved_push_pcs.remove(i)
        if opcodes[op]["name"][:4]=="PUSH" and int(''.join(params),16) in old_address_to_label.keys():
            p[x][2]=old_address_to_label[int(''.join(params),16)]
    i+=1+len(params)

block_ranges=[]
for block in func_to_blocks['0x'+funcsighash.lower()]:
    i = blocks_list.index(block)
    block_ranges.append((block,blocks_list[i+1]-1))
# ---
internal_function_call_returns=[]
i=0
for x in range(len(p)):
    op,params,lbl = p[x]
    current_block_start=None
    current_block_end=None
    for l1,l2 in block_ranges:
        if l1 <= i <= l2:
            current_block_start=l1
            current_block_end=l2
            break
    if current_block_start and current_block_start <= i <= current_block_end \
       and old_address_to_label.get(current_block_end+1,0)==lbl and opcodes[op]["name"][:4]=="PUSH":
        internal_function_call_returns+=[i]
    i+=1+len(params)
# --
from copy import deepcopy

make_hash_of_top=[
    # put value on stack
    ["DUP1"], # [V]
    # store value in memory, after the hash
    ["PUSH1", ['A0']], #[A0, V]
    ['MSTORE'], # []
    # compute next hash
    ["PUSH1", ['40']], # [40]
    ["PUSH1", ['80']], # [80,40]
    ['SHA3'], # [newhash]
    # store new hash
    ['PUSH1', ['80']], # [80, newhash]
    ['MSTORE'], # []
]

make_hash_of_below_top=deepcopy(make_hash_of_top)
make_hash_of_below_top[0][0]="DUP2"

def assemble(op_list):
    nl=[]
    for e in op_list:
        if len(e) == 2:
            op,params = e
            nl+=[[name_to_op[op], params, None]]
        else:
            op = e[0]
            nl+=[[name_to_op[op], [], None]]
    return nl

mht = assemble(make_hash_of_top)
mhbt = assemble(make_hash_of_below_top)

def get_payload_size():
    sz=0
    for instruction in payload:
        _,b,_=instruction
        sz+=1+len(b)
    return sz


def make_pushes_big():
    for x in range(len(p)):
        op,params,lbl=p[x]
        if lbl and opcodes[op]["name"] != "JUMPDEST":
            p[x][0]=name_to_op["PUSH2"]
            cparam=set_leading_zeros(int(''.join(params),16))
            p[x][1]=[cparam[i]+cparam[i+1] for i in range(0,4,2)]


# opcodes where we want to take the hash of the top of the stack,
# after they get executed
post_ops={
    "CALLDATASIZE",
    "CALLDATALOAD",
    "SLOAD",
    "MLOAD",
}
# before they get executed
pre_ops={
    # we can assume that the function is a view and thus no SSTORE appears
    # there anyway, but if it would appear we would like to include the address as well
    "SSTORE",
}

# opcodes where we want to take the hash of the value below the top,
# before they get executed
pre2_ops={
    "JUMPI",
    "SSTORE",
    "MSTORE",
    "MSTORE8",
}

def inject_code():
    new_p=[]
    i=0
    for x in range(len(p)):
        op,params,lbl = p[x]
        if any(l1 <= i <= l2 for l1,l2 in block_ranges):
            # compute hash update before executing the respective opcode
            if opcodes[op]['name'] in pre_ops:
                new_p+=mht
            if opcodes[op]['name'] in pre2_ops:
                new_p+=mhbt
        new_p+=[[op,params,lbl]]
        if any(l1 <= i <= l2 for l1,l2 in block_ranges):
            # compute hash update after executing the respective opcode
            if opcodes[op]['name'] in post_ops:
                new_p+=mht
        # compute hash update after returning from internal function call
        if i in internal_function_call_returns:
            new_p+=mht
        i+=1+len(params)
    return new_p

p=inject_code()
make_pushes_big()

new_bytecode=reassemble(p)

def fix_constructor(new_code_size):
    new_constructor_bytecode=""
    # fixing last CODECOPY
    for x in range(len(constructor)-1,-1,-1):
        op,params,lbl=constructor[x]
        if opcodes[op]["name"] == "CODECOPY":
            constructor[x-2][0]="61"
            constructor[x-2][2]="CL"
            constructor[x-2][1]=["00","00"]
            constructor[x-4][0]="61"
            constructor[x-4][2]="CS"
            constructor[x-4][1]=["00","00"]
            break
    # fixing first CODECOPY
    for x in range(len(constructor)):
        op,params,lbl=constructor[x]
        if opcodes[op]["name"] == "CODECOPY":
            constructor[x-2][0]="61"
            constructor[x-2][2]="CL+CS"
            constructor[x-2][1]=["00","00"]
            constructor[x-6][0]="61"
            constructor[x-6][2]="CL+CS"
            constructor[x-6][1]=["00","00"]
            break

    new_constructor_length = 0
    for x in range(len(constructor)):
        op,params,lbl=constructor[x]
        new_constructor_length += 1 + len(params)

    for x in range(len(constructor)):
        op,params,lbl=constructor[x]
        new_constructor_bytecode += op
        if constructor[x][2] == "CS":
            new_constructor_bytecode += set_leading_zeros(new_code_size)
        elif constructor[x][2] == "CL":
            new_constructor_bytecode += set_leading_zeros(new_constructor_length)
        elif constructor[x][2] == "CL+CS":
            new_constructor_bytecode += set_leading_zeros(new_constructor_length+new_code_size)
        else:
            new_constructor_bytecode += ''.join(params)
    return new_constructor_bytecode

cc=fix_constructor(int(hex(len(new_bytecode)//2)[2:].upper(),16))

with open(args.outputfile, 'w') as f:
    f.write(cc+new_bytecode)