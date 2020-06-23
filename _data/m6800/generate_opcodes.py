import json

opcodes = {}

immediate = {
    "d8": {"name": "d8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "#d8": {"name": "#d8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "s8": {"name": "s8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "a8": {"name": "a8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "d16": {"name": "d16", "description": "16-bit immediate value", "bytes": 2, "type": "immediate"},
    "#d16": {"name": "#d16", "description": "16-bit immediate value", "bytes": 2, "type": "immediate"},
    "a16": {"name": "a16", "description": "16-bit immediate address", "bytes": 2, "type": "immediate"}
}

registers = {
    "A": {"name": "A", "description": "Accumulator A", "type": "register"},
    "B": {"name": "B", "description": "Accumulator B", "type": "register"},
    "X": {"name": "X", "description": "Index register", "type": "register"},
}

for opcode in range(0x00, 0x100):
    nibble1 = (opcode & 0xF0) >> 4
    nibble2 = opcode & 0x0F

    foo = {'operands': []}

    # set instruction
    if nibble2 == 0:
        if nibble1 == 0:
            # undefined opcode
            pass
        elif nibble1 == 1:
            foo['instruction'] = 'SBA'
        elif nibble1 == 2:
            foo['instruction'] = 'BRA'
        elif nibble1 == 3:
            foo['instruction'] = 'TSX'
        elif nibble1 < 0x8:
            foo['instruction'] = 'NEG'
        else:
            foo['instruction'] = 'SUB'
    elif nibble2 == 1:
        if nibble1 == 0:
            foo['instruction'] = 'NOP'
        elif nibble1 == 1:
            foo['instruction'] = 'CBA'
        elif nibble1 == 2:
            foo['variant'] = {
                'instruction': 'BRN',
                'group': 'flow'
            }
        elif nibble1 == 3:
            foo['instruction'] = 'INS'
        elif nibble1 == 6 or nibble1 == 7:
            foo['variant'] = {
                'instruction': 'AIM',
                'operands': [ immediate['d8'] ]
            }
        elif nibble1 > 0x7:
            foo['instruction'] = 'CMP'
        else:
            # undefined opcodes
            pass
    elif nibble2 == 2:
        if nibble1 == 2:
            foo['instruction'] = 'BHI'
        elif nibble1 == 3:
            foo['instruction'] = 'PUL'
        elif nibble1 == 6 or nibble1 == 7:
            foo['variant'] = {
                'instruction': 'OIM',
                'operands': [ immediate['d8'] ]
            }
        elif nibble1 > 0x7:
            foo['instruction'] = 'SBC'
        else:
            # undefined opcodes
            pass
    elif nibble2 == 3:
        if nibble1 == 0 or nibble1 == 1:
            # undefined opcodes
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BLS'
        elif nibble1 == 3:
            foo['instruction'] = 'PUL'
        elif nibble1 < 8:
            foo['instruction'] = 'COM'
        elif nibble1 < 0xC:
            foo['variant'] = {
                'instruction': 'SUBD'
            }
        else:
            foo['variant'] = {
                'instruction': 'ADDD'
            }
    elif nibble2 == 4:
        if nibble1 == 0:
            foo['variant'] = {
                'instruction': 'LSRD'
            }
        elif nibble1 == 1:
            foo['instruction'] = 'NBA'
            foo['illegal'] = True
        elif nibble1 == 2:
            foo['instruction'] = 'BCC'
        elif nibble1 == 3:
            foo['instruction'] = 'DES'
        elif nibble1 < 8:
            foo['instruction'] = 'LSR'
        elif nibble1 > 7:
            foo['instruction'] = 'AND'
    elif nibble2 == 5:
        if nibble1 == 0:
            foo['variant'] = {
                'instruction': 'ASLD'
            }
        elif nibble1 == 1:
            foo['instruction'] = 'NOP'
            foo['illegal'] = True
        elif nibble1 == 2:
            foo['instruction'] = 'BCS'
        elif nibble1 == 3:
            foo['instruction'] = 'TXS'
        elif nibble1 == 6 or nibble1 == 7:
            foo['variant'] = {
                'instruction': 'EIM',
                'operands': [ immediate['d8'] ]
            }
        elif nibble1 > 7:
            foo['instruction'] = 'BIT'
    elif nibble2 == 6:
        if nibble1 == 0:
            foo['instruction'] = 'TAP'
        elif nibble1 == 1:
            foo['instruction'] = 'TAB'
        elif nibble1 == 2:
            foo['instruction'] = 'BNE'
        elif nibble1 == 3:
            foo['instruction'] = 'PSH'
        elif nibble1 < 8:
            foo['instruction'] = 'ROR'
        elif nibble1 > 7:
            foo['instruction'] = 'LDA'
    elif nibble2 == 7:
        if nibble1 == 0:
            foo['instruction'] = 'TPA'
        elif nibble1 == 1:
            foo['instruction'] = 'TBA'
        elif nibble1 == 2:
            foo['instruction'] = 'BEQ'
        elif nibble1 == 3:
            foo['instruction'] = 'PSH'
        elif nibble1 < 8:
            foo['instruction'] = 'ASR'
        elif nibble1 > 7:
            foo['instruction'] = 'STA'
            if nibble1 == 8 or nibble1 == 0xC:
                foo['illegal'] = True
    elif nibble2 == 8:
        if nibble1 == 0:
            foo['instruction'] = 'INX'
        elif nibble1 == 1:
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BVC'
        elif nibble1 == 3:
            foo['variant'] = {
                'instruction': 'PULX'
            }
        elif nibble1 < 8:
            foo['instruction'] = 'ASL'
        elif nibble1 > 7:
            foo['instruction'] = 'EOR'
    elif nibble2 == 9:
        if nibble1 == 0:
            foo['instruction'] = 'DEX'
        elif nibble1 == 1:
            foo['instruction'] = 'DAA'
        elif nibble1 == 2:
            foo['instruction'] = 'BVS'
        elif nibble1 == 3:
            foo['instruction'] = 'RTS'
        elif nibble1 < 8:
            foo['instruction'] = 'ROL'
        elif nibble1 > 7:
            foo['instruction'] = 'ADC'
    elif nibble2 == 0xA:
        if nibble1 == 0:
            foo['instruction'] = 'CLV'
        elif nibble1 == 1:
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BPL'
        elif nibble1 == 3:
            foo['variant'] = {
                'instruction': 'ABX'
            }
        elif nibble1 < 8:
            foo['instruction'] = 'DEC'
        elif nibble1 > 7:
            foo['instruction'] = 'ORA'
    elif nibble2 == 0xB:
        if nibble1 == 0:
            foo['instruction'] = 'SEV'
        elif nibble1 == 1:
            foo['instruction'] = 'ABA'
        elif nibble1 == 2:
            foo['instruction'] = 'BMI'
        elif nibble1 == 3:
            foo['instruction'] = 'RTI'
        elif nibble1 == 6 or nibble1 == 7:
            foo['variant'] = {
                'instruction': 'TIM',
                'operands': [ immediate['d8'] ]
            }
        elif nibble1 > 7:
            foo['instruction'] = 'ADD'
    elif nibble2 == 0xC:
        if nibble1 == 0:
            foo['instruction'] = 'CLC'
        elif nibble1 == 1:
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BGE'
        elif nibble1 == 3:
            foo['variant'] = {
                'instruction': 'PUSHX'
            }
        elif nibble1 < 8:
            foo['instruction'] = 'INC'
        elif nibble1 < 0xC:
            foo['instruction'] = 'CPX'
        else:
            foo['variant'] = {
                'instruction': 'LDD'
            }
    elif nibble2 == 0xD:
        if nibble1 == 0:
            foo['instruction'] = 'SEC'
        elif nibble1 == 1:
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BLT'
        elif nibble1 == 3:
            foo['variant'] = {
                'instruction': 'MUL'
            }
        elif nibble1 < 8:
            foo['instruction'] = 'TST'
        elif nibble1 == 8:
            foo['instruction'] = 'BSR'
        elif nibble1 == 0xA or nibble1 == 0xB:
            foo['instruction'] = 'JSR'
        else:
            foo['instruction'] = 'HCF'
            foo['illegal'] = True
            if nibble1 == 0x9:
                foo['variant'] = {
                    'instruction': 'JSR',
                    'operands': [ immediate['d8'] ]
                }
            elif nibble1 > 0xC:
                foo['variant'] = {
                    'instruction': 'STD',
                }
    elif nibble2 == 0xE:
        if nibble1 == 0:
            foo['instruction'] = 'CLI'
        elif nibble1 == 1 or nibble1 == 3:
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BGT'
        elif nibble1 == 3:
            foo['instruction'] = 'WAI'
        elif nibble1 == 6 or nibble1 == 7:
            foo['instruction'] = 'JMP'
        elif nibble1 > 7 and nibble1 < 0xC:
            foo['instruction'] = 'LDS'
        elif nibble1 > 0xB:
            foo['instruction'] = 'LDX'
    elif nibble2 == 0xF:
        if nibble1 == 0:
            foo['instruction'] = 'SEI'
        elif nibble1 == 1: 
            # undefined opcode
            pass
        elif nibble1 == 2:
            foo['instruction'] = 'BLE'
        elif nibble1 == 3:
            foo['instruction'] = 'SWI'
        elif nibble1 < 8:
            foo['instruction'] = 'CLR'
        elif nibble1 > 7 and nibble1 < 0xC:
            foo['instruction'] = 'STS'
            if nibble1 == 8:
                foo['illegal'] = True
        elif nibble1 > 0xB:
            foo['instruction'] = 'STX'
            if nibble1 == 0xC:
                foo['illegal'] = True

    # set accumulator
    if (nibble1 > 0xB and nibble2 < 0xC) or nibble1 == 0x5 or opcode == 0x33 or opcode == 0x37:
        foo['operands'].append(registers['B'])
    elif (nibble1 > 0x7 and nibble2 < 0xC) or nibble1 == 0x4 or opcode == 0x32 or opcode == 0x36:
        foo['operands'].append(registers['A'])
    
    # set addressing mode
    if nibble1 == 0x2 or opcode == 0x8D:
        foo['operands'].append(immediate['s8'])
    elif nibble1 == 0x6 or nibble1 == 0xA or nibble1 == 0xE:
        foo['operands'] += [immediate['d8'], registers['X']]
    elif nibble1 == 0x7 or nibble1 == 0xB or nibble1 == 0xF:
        if nibble1 == 0x7 and nibble2 in (0x1, 0x2, 0x5, 0xB):
            foo['operands'].append(immediate['a8'])
        else:
            foo['operands'].append(immediate['a16'])
    elif nibble1 == 0x8 or nibble1 == 0xC:
        foo['operands'].append(immediate['#d8'])
    elif nibble1 == 0x9 or nibble1 == 0xD:
        foo['operands'].append(immediate['a8'])

    if 'variant' in foo:
        if 'operands' not in foo['variant']:
            foo['variant']['operands'] = []
        foo['variant']['operands'] += foo['operands']

    if 'instruction' not in foo or foo['instruction'] == 'HCF':
        foo['operands'] = []

    opcodes["0x%02X" % opcode] = foo

with open('opcodes.json', 'w') as fp:
    json.dump({'unprefixed': opcodes}, fp, sort_keys=True, indent=4)
