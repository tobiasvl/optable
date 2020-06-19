import json

scratchpad = [
    { "name": "R0"},
    { "name": "R1"},
    { "name": "R2"},
    { "name": "R3"},
    { "name": "R4"},
    { "name": "R5"},
    { "name": "R6"},
    { "name": "R7"},
    { "name": "R8"},
    { "name": "R9"},
    { "name": "R10"},
    { "name": "R11"},
    { "name": "S"},
    { "name": "I"},
    { "name": "D"},
    { "name": "R15"} 
]

registers = {
    "J": {"name": "J", "description": "Scratchpad register 9", "type": "register"},
    "H": {"name": "H", "description": "Scratchpad registers 10 (HU) and 11 (HL)", "type": "register"},
    "K": {"name": "K", "description": "Scratchpad registers 12 (KU) and 13 (KL)", "type": "register"},
    "KU": {"name": "K", "description": "Scratchpad registers 12 (KU) and 13 (KL)", "type": "register"},
    "KL": {"name": "K", "description": "Scratchpad registers 12 (KU) and 13 (KL)", "type": "register"},
    "Q": {"name": "Q", "description": "Scratchpad registers 14 (QU) and 15 (QL)", "type": "register"},
    "QU": {"name": "Q", "description": "Scratchpad registers 14 (QU) and 15 (QL)", "type": "register"},
    "QL": {"name": "Q", "description": "Scratchpad registers 14 (QU) and 15 (QL)", "type": "register"},
    "P": {"name": "P", "description": "16-bit stack register. Also known as PC1.", "type": "register"},
    "S": {"name": "S", "description": "The scratchpad register currently addressed by ISAR. Also known as IS and 12.", "type": "register"},
    "IS": {"name": "S", "description": "The scratchpad register currently addressed by ISAR. Also known as IS and 12.", "type": "register"},
    "I": {"name": "I", "description": "The scratchpad register currently addressed by ISAR; ISAR is then post-incremented. Also known as 13.", "type": "register"},
    "D": {"name": "D", "description": "The scratchpad register currently addressed by ISAR; ISAR is then post-decremented. Also known as 14.", "type": "register"},
    "P0": {"name": "P0", "description": "Program Counter. Also known as PC0.", "type": "register"},
    "DC": {"name": "DC", "description": "Data Counter. Also known as DC0.", "type": "register"},
    "DC1": {"name": "DC1", "description": "Data Counter storage", "type": "register"},
    "A": {"name": "A", "description": "8-bit accumulator A", "type": "register"},
    "W": {"name": "W", "description": "Status register", "type": "register"},
}

immediate = {
    "d8": {"name": "d8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "d16": {"name": "d16", "description": "16-bit immediate value", "bytes": 2, "type": "immediate"},
    "a16": {"name": "a16", "description": "16-bit immediate address", "bytes": 2, "type": "immediate"}
}

inherent = [None] * 16
for i in range(16):
    inherent[i] = {"name": i}
    
opcodes = {}

for opcode in range(0x00, 0x100):
    r = scratchpad[opcode & 0x0F]
    foo = {}

    if opcode == 0x00:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            registers['KU'],
        ]
    elif opcode == 0x01:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            registers['KL'],
        ]
    elif opcode == 0x02:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            registers['QU'],
        ]
    elif opcode == 0x03:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            registers['QL'],
        ]
    elif opcode == 0x04:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['KU'],
            registers['A'],
        ]
    elif opcode == 0x05:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['KL'],
            registers['A'],
        ]
    elif opcode == 0x06:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['QU'],
            registers['A'],
        ]
    elif opcode == 0x07:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['QL'],
            registers['A'],
        ]
    elif opcode == 0x08:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['K'],
            registers['P'],
        ]
    elif opcode == 0x09:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['P'],
            registers['K'],
        ]
    elif opcode == 0x0A:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            registers['IS'],
        ]
    elif opcode == 0x0B:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['IS'],
            registers['A'],
        ]
    elif opcode == 0x0C:
        foo['instruction'] = 'PK'
    elif opcode == 0x0D:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['P0'],
            registers['Q'],
        ]
    elif opcode == 0x0E:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['H'],
            registers['DC'],
        ]
    elif opcode == 0x0F:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['Q'],
            registers['DC'],
        ]
    elif opcode == 0x10:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['DC'],
            registers['Q'],
        ]
    elif opcode == 0x11:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['H'],
            registers['DC'],
        ]
    elif opcode == 0x12:
        foo['instruction'] = 'SR'
        foo['operands'] = [ inherent[1] ]
    elif opcode == 0x13:
        foo['instruction'] = 'SL'
        foo['operands'] = [ inherent[1] ]
    elif opcode == 0x14:
        foo['instruction'] = 'SR'
        foo['operands'] = [ inherent[4] ]
    elif opcode == 0x15:
        foo['instruction'] = 'SL'
        foo['operands'] = [ inherent[4] ]
    elif opcode == 0x16:
        foo['instruction'] = 'LM'
    elif opcode == 0x17:
        foo['instruction'] = 'ST'
    elif opcode == 0x18:
        foo['instruction'] = 'COM'
    elif opcode == 0x19:
        foo['instruction'] = 'LNK'
    elif opcode == 0x1A:
        foo['instruction'] = 'DI'
    elif opcode == 0x1B:
        foo['instruction'] = 'EI'
    elif opcode == 0x1C:
        foo['instruction'] = 'POP'
    elif opcode == 0x1D:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['W'],
            registers['J'],
        ]
    elif opcode == 0x1E:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['W'],
            registers['J'],
        ]
    elif opcode == 0x1F:
        foo['instruction'] = 'INC'
    elif opcode & 0xF0 == 0x20:
        if opcode & 0xF8 == 0x20:
            foo['operands'] = [
                immediate["d8"]
            ]
        if opcode == 0x20:
            foo['instruction'] = 'LI'
        elif opcode == 0x21:
            foo['instruction'] = 'NI'
        elif opcode == 0x22:
            foo['instruction'] = 'OI'
        elif opcode == 0x23:
            foo['instruction'] = 'XI'
        elif opcode == 0x24:
            foo['instruction'] = 'AI'
        elif opcode == 0x25:
            foo['instruction'] = 'CI'
        elif opcode == 0x26:
            foo['instruction'] = 'IN'
        elif opcode == 0x27:
            foo['instruction'] = 'OUT'
        elif opcode == 0x28:
            foo['instruction'] = 'PI'
            foo['operands'] = [
                immediate["d16"]
            ]
        elif opcode == 0x29:
            foo['instruction'] = 'JMP'
            foo['operands'] = [
                immediate["d16"]
            ]
        elif opcode == 0x2A:
            foo['instruction'] = 'DCI'
            foo['operands'] = [
                immediate["d16"]
            ]
        elif opcode == 0x2B:
            foo['instruction'] = 'NOP'
        elif opcode == 0x2C:
            foo['instruction'] = 'XDC'
    elif opcode & 0xF0 == 0x30:
        foo['instruction'] = 'DS'
        foo['operands'] = [
            r
        ]
    elif opcode & 0xF0 == 0x40:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            registers['A'],
            r
        ]
    elif opcode & 0xF0 == 0x50:
        foo['instruction'] = 'LR'
        foo['operands'] = [
            r,
            registers['A']
        ]
    elif opcode & 0xF0 == 0x60:
        foo['operands'] = [
            inherent[opcode & 0x07]
        ]
        if opcode & 0xF8 == 0x68:
            foo['instruction'] = 'LISL'
        elif opcode & 0xF8 == 0x60:
            foo['instruction'] = 'LISU'
    elif opcode == 0x70:
        foo['instruction'] = 'CLR'
    elif opcode & 0xF0 == 0x70:
        foo['instruction'] = 'LIS'
        foo['operands'] = [
            inherent[opcode & 0x0F]
        ]
    elif opcode & 0xF8 == 0x80:
        condition = inherent[opcode & 0x07]
        foo['operands'] = []
        if condition == 0x01:
            foo['instruction'] = "BP"
        elif condition == 0x02:
            foo['instruction'] = "BC"
        elif condition == 0x04:
            foo['instruction'] = "BZ"
        else:
            foo['instruction'] = "BT"
            foo['operands'].append(condition)
        foo['operands'].append(immediate["d8"])
    elif opcode == 0x88:
        foo['instruction'] = 'AM'
    elif opcode == 0x89:
        foo['instruction'] = 'AMD'
    elif opcode == 0x8A:
        foo['instruction'] = 'NM'
    elif opcode == 0x8B:
        foo['instruction'] = 'OM'
    elif opcode == 0x8C:
        foo['instruction'] = 'XM'
    elif opcode == 0x8D:
        foo['instruction'] = 'CM'
    elif opcode == 0x8E:
        foo['instruction'] = 'ADC'
    elif opcode == 0x8F:
        foo['instruction'] = 'BR7'
        foo['operands'] = [immediate["d8"]]
    elif opcode & 0xF0 == 0x90:
        condition = inherent[opcode & 0x0F]
        foo['operands'] = []
        if condition == 0x00:
            foo['instruction'] = "BR"
        elif condition == 0x01:
            foo['instruction'] = "BM"
        elif condition == 0x02:
            foo['instruction'] = "BNC"
        elif condition == 0x04:
            foo['instruction'] = "BNZ"
        elif condition == 0x08:
            foo['instruction'] = "BNO"
        else:
            foo['instruction'] = "BF"
            foo['operands'].append(condition)
        foo['operands'].append(immediate["d8"])
    elif opcode & 0xF0 == 0xA0:
        foo['instruction'] = 'INS'
        foo['operands'] = [
            inherent[opcode & 0x0F]
        ]
    elif opcode & 0xF0 == 0xB0:
        foo['instruction'] = 'OUTS'
        foo['operands'] = [
            inherent[opcode & 0x0F]
        ]
    elif opcode & 0xF0 == 0xC0:
        foo['instruction'] = 'AS'
        foo['operands'] = [
            r
        ]
    elif opcode & 0xF0 == 0xD0:
        foo['instruction'] = 'ASD'
        foo['operands'] = [
            r
        ]
    elif opcode & 0xF0 == 0xE0:
        foo['instruction'] = 'XS'
        foo['operands'] = [
            r
        ]
    elif opcode & 0xF0 == 0xF0:
        foo['instruction'] = 'NS'
        foo['operands'] = [
            r
        ]

    opcodes["0x%02X" % opcode] = foo

with open('opcodes.json', 'w') as fp:
    json.dump({'unprefixed': opcodes}, fp, sort_keys=True, indent=4)


