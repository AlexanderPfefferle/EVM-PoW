# opcode info from:
# https://ethervm.io/
# https://ethereum.github.io/yellowpaper/paper.pdf (includes gas info)

opcodes = {
    '00': {"name": 'STOP', "num_stack_in": 0, "num_stack_out": 0, "extra_in": 0},
    '01': {"name": 'ADD', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '02': {"name": 'MUL', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '03': {"name": 'SUB', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '04': {"name": 'DIV', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '05': {"name": 'SDIV', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '06': {"name": 'MOD', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '07': {"name": 'SMOD', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '08': {"name": 'ADDMOD', "num_stack_in": 3, "num_stack_out": 1, "extra_in": 0},
    '09': {"name": 'MULMOD', "num_stack_in": 3, "num_stack_out": 1, "extra_in": 0},
    '0A': {"name": 'EXP', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '0B': {"name": 'SIGNEXTEND', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},

    '10': {"name": 'LT', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '11': {"name": 'GT', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '12': {"name": 'SLT', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '13': {"name": 'SGT', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '14': {"name": 'EQ', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '15': {"name": 'ISZERO', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '16': {"name": 'AND', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '17': {"name": 'OR', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '18': {"name": 'XOR', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '19': {"name": 'NOT', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '1A': {"name": 'BYTE', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '1B': {"name": 'SHL', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '1C': {"name": 'SHR', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},
    '1D': {"name": 'SAR', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},

    '20': {"name": 'SHA3', "num_stack_in": 2, "num_stack_out": 1, "extra_in": 0},

    '30': {"name": 'ADDRESS', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '31': {"name": 'BALANCE', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '32': {"name": 'ORIGIN', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '33': {"name": 'CALLER', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '34': {"name": 'CALLVALUE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '35': {"name": 'CALLDATALOAD', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '36': {"name": 'CALLDATASIZE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '37': {"name": 'CALLDATACOPY', "num_stack_in": 3, "num_stack_out": 0, "extra_in": 0},
    '38': {"name": 'CODESIZE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '39': {"name": 'CODECOPY', "num_stack_in": 3, "num_stack_out": 0, "extra_in": 0},
    '3A': {"name": 'GASPRICE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '3B': {"name": 'EXTCODESIZE', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '3C': {"name": 'EXTCODECOPY', "num_stack_in": 4, "num_stack_out": 0, "extra_in": 0},
    '3D': {"name": 'RETURNDATASIZE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '3E': {"name": 'RETURNDATACOPY', "num_stack_in": 3, "num_stack_out": 0, "extra_in": 0},
    '3F': {"name": 'EXTCODEHASH', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '40': {"name": 'BLOCKHASH', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '41': {"name": 'COINBASE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '42': {"name": 'TIMESTAMP', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '43': {"name": 'NUMBER', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '44': {"name": 'DIFFICULTY', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '45': {"name": 'GASLIMIT', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    # the 3 new london opcodes
    '46': {"name": 'CHAINID', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '47': {"name": 'SELFBALANCE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '48': {"name": 'BASEFEE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},

    '50': {"name": 'POP', "num_stack_in": 1, "num_stack_out": 0, "extra_in": 0},
    '51': {"name": 'MLOAD', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '52': {"name": 'MSTORE', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},
    '53': {"name": 'MSTORE8', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},
    '54': {"name": 'SLOAD', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    '55': {"name": 'SSTORE', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},
    '56': {"name": 'JUMP', "num_stack_in": 1, "num_stack_out": 0, "extra_in": 0},
    '57': {"name": 'JUMPI', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},
    '58': {"name": 'PC', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '59': {"name": 'MSIZE', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '5A': {"name": 'GAS', "num_stack_in": 0, "num_stack_out": 1, "extra_in": 0},
    '5B': {"name": 'JUMPDEST', "num_stack_in": 0, "num_stack_out": 0, "extra_in": 0},

    'A0': {"name": 'LOG0', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},
    'A1': {"name": 'LOG1', "num_stack_in": 3, "num_stack_out": 0, "extra_in": 0},
    'A2': {"name": 'LOG2', "num_stack_in": 4, "num_stack_out": 0, "extra_in": 0},
    'A3': {"name": 'LOG3', "num_stack_in": 5, "num_stack_out": 0, "extra_in": 0},
    'A4': {"name": 'LOG4', "num_stack_in": 6, "num_stack_out": 0, "extra_in": 0},

    'F0': {"name": 'CREATE', "num_stack_in": 3, "num_stack_out": 1, "extra_in": 0},
    'F1': {"name": 'CALL', "num_stack_in": 7, "num_stack_out": 1, "extra_in": 0},
    'F2': {"name": 'CALLCODE', "num_stack_in": 7, "num_stack_out": 1, "extra_in": 0},
    'F3': {"name": 'RETURN', "num_stack_in": 1, "num_stack_out": 1, "extra_in": 0},
    'F4': {"name": 'DELEGATECALL', "num_stack_in": 6, "num_stack_out": 1, "extra_in": 0},
    'F5': {"name": 'CREATE2', "num_stack_in": 4, "num_stack_out": 1, "extra_in": 0},

    'FA': {"name": 'STATICCALL', "num_stack_in": 6, "num_stack_out": 1, "extra_in": 0},

    'FD': {"name": 'REVERT', "num_stack_in": 2, "num_stack_out": 0, "extra_in": 0},

    'FF': {"name": 'SELFDESTRUCT', "num_stack_in": 1, "num_stack_out": 0, "extra_in": 0},
}

# PUSHs
for i in range(1, 33):
    opcodes[hex(int("5F", 16)+i)[2:].upper()] = {"name": 'PUSH'+str(
        i), "num_stack_in": 0, "num_stack_out": 1, "extra_in": i}
# SWAPs
for i in range(1, 17):
    opcodes[hex(int("7F", 16)+i)[2:].upper()] = {"name": 'DUP'+str(
        i), "num_stack_in": -1, "num_stack_out": 1, "extra_in": 0}
# DUPs
for i in range(1, 17):
    opcodes[hex(int("8F", 16)+i)[2:].upper()] = {"name": 'SWAP'+str(
        i), "num_stack_in": -1, "num_stack_out": -1, "extra_in": 0}

# invalids
for op_index in range(256):
    op_hex = hex(op_index)[2:].upper().zfill(2)
    if op_hex not in opcodes.keys():
        opcodes[op_hex] = {"name": 'INVALID',
                           "num_stack_in": -1, "num_stack_out": -1, "extra_in": 0}

opcodes['-1'] = {"name": 'undefined', "num_stack_in": -
                 1, "num_stack_out": -1, "extra_in": 0}


name_to_op = {opcodes[x]["name"]: x for x in opcodes.keys()}
