import json

immediate = {
    'd8': {'name': 'd8', 'bytes': 1, 'type': 'immediate'},
    'd16': {'name': 'd16', 'bytes': 2, 'type': 'immediate'}
}

registers = []
for i in range(0,16):
    registers.append(
        {
            'name': "R%X" % i,
            'description': "Scratchpad Register %X" % i,
            'type': 'register'
        }
    )

inherent = []
for i in range(0,16):
    inherent.append({'name': "%d" % i, 'type': 'inherent'})

opcodes = {}

for opcode in range(0x00, 0x100):
    I = opcode >> 4
    N = opcode & 0xF

    foo = {}

    if I == 0x0:
        if N == 0x0:
            foo['instruction'] = "IDL"
        else:
            foo['instruction'] = "LDN"
            foo['operands'] = [ registers[N] ]
    elif I == 0x1:
        foo['instruction'] = "INC"
        foo['operands'] = [ registers[N] ]
    elif I == 0x2:
        foo['instruction'] = "DEC"
        foo['operands'] = [ registers[N] ]
    elif I == 0x3:
        foo['operands'] = [ immediate['d8'] ]
        if N == 0x0:
            foo['instruction'] = "BR"
        elif N == 0x1:
            foo['instruction'] = "BQ"
        elif N == 0x2:
            foo['instruction'] = "BZ"
        elif N == 0x3:
            foo['instruction'] = "BDF"
        elif N >= 0x4 and N <= 0x7:
            foo['instruction'] = "B%d" % (N - 3)
        elif N == 0x8:
            foo['instruction'] = "SKP"
            foo['operands'] = [ ]
        elif N == 0x9:
            foo['instruction'] = "BNQ"
        elif N == 0xA:
            foo['instruction'] = "BNZ"
        elif N == 0xB:
            foo['instruction'] = "BNF"
        elif N >= 0xC:
            foo['instruction'] = "BN%d" % (N - 0xB)
    elif I == 0x4:
        foo['instruction'] = "LDA"
        foo['operands'] = [ registers[N] ]
    elif I == 0x5:
        foo['instruction'] = "STR"
        foo['operands'] = [ registers[N] ]
    elif I == 0x6:
        if N == 0x0:
            foo['instruction'] = "IRX"
        elif N < 0x8:
            foo['instruction'] = "OUT"
            foo['operands'] = [ inherent[N] ]
        else:
            foo['instruction'] = "INP"
            foo['operands'] = [ inherent[N - 0x8] ]
            if N == 0x8:
                foo['illegal'] = True
                foo['variants'] = [ { 'instruction': "PREFIX" } ]
    elif I == 0x7:
        if N == 0x0:
            foo['instruction'] = "RET"
        elif N == 0x1:
            foo['instruction'] = "DIS"
        elif N == 0x2:
            foo['instruction'] = "LDXA"
        elif N == 0x3:
            foo['instruction'] = "STXD"
        elif N == 0x4:
            foo['instruction'] = "ADC"
        elif N == 0x5:
            foo['instruction'] = "SDB"
        elif N == 0x6:
            foo['instruction'] = "SHRC"
        elif N == 0x7:
            foo['instruction'] = "SMB"
        elif N == 0x8:
            foo['instruction'] = "SAV"
        elif N == 0x9:
            foo['instruction'] = "MARK"
        elif N == 0xA:
            foo['instruction'] = "REQ"
        elif N == 0xB:
            foo['instruction'] = "SEQ"
        elif N == 0xC:
            foo['instruction'] = "ADCI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xD:
            foo['instruction'] = "SDBI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xE:
            foo['instruction'] = "SHLC"
        elif N == 0xF:
            foo['instruction'] = "SMBI"
            foo['operands'] = [ immediate['d8'] ]
    elif I == 0x8:
        foo['instruction'] = "GLO"
        foo['operands'] = [ registers[N] ]
    elif I == 0x9:
        foo['instruction'] = "GHI"
        foo['operands'] = [ registers[N] ]
    elif I == 0xA:
        foo['instruction'] = "PLO"
        foo['operands'] = [ registers[N] ]
    elif I == 0xB:
        foo['instruction'] = "PHI"
        foo['operands'] = [ registers[N] ]
    elif I == 0xC:
        foo['timing'] = { 'cycles': 3 }
        if N == 0x0:
            foo['instruction'] = "LBR"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0x1:
            foo['instruction'] = "LBQ"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0x2:
            foo['instruction'] = "LBZ"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0x3:
            foo['instruction'] = "LBDF"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0x4:
            foo['instruction'] = "NOP"
        elif N == 0x5:
            foo['instruction'] = "LSNQ"
        elif N == 0x6:
            foo['instruction'] = "LSNZ"
        elif N == 0x7:
            foo['instruction'] = "LSNF"
        elif N == 0x8:
            foo['instruction'] = "LSKP"
        elif N == 0x9:
            foo['instruction'] = "LBNQ"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0xA:
            foo['instruction'] = "LBNZ"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0xB:
            foo['instruction'] = "LBNF"
            foo['operands'] = [ immediate['d16'] ]
        elif N == 0xC:
            foo['instruction'] = "LSIE"
        elif N == 0xD:
            foo['instruction'] = "LSQ"
        elif N == 0xE:
            foo['instruction'] = "LSZ"
        elif N == 0xF:
            foo['instruction'] = "LSDF"
    elif I == 0xD:
        foo['instruction'] = "SEP"
        foo['operands'] = [ registers[N] ]
    elif I == 0xE:
        foo['instruction'] = "SEX"
        foo['operands'] = [ registers[N] ]
    elif I == 0xF:
        if N == 0x0:
            foo['instruction'] = "LDX"
        elif N == 0x1:
            foo['instruction'] = "OR"
        elif N == 0x2:
            foo['instruction'] = "AND"
        elif N == 0x3:
            foo['instruction'] = "XOR"
        elif N == 0x4:
            foo['instruction'] = "ADD"
        elif N == 0x5:
            foo['instruction'] = "SD"
        elif N == 0x6:
            foo['instruction'] = "SHR"
        elif N == 0x7:
            foo['instruction'] = "SM"
        elif N == 0x8:
            foo['instruction'] = "LDI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0x9:
            foo['instruction'] = "ORI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xA:
            foo['instruction'] = "ANI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xB:
            foo['instruction'] = "XRI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xC:
            foo['instruction'] = "ADI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xD:
            foo['instruction'] = "SDI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xE:
            foo['instruction'] = "SHL"
        elif N == 0xF:
            foo['instruction'] = "SMI"
            foo['operands'] = [ immediate['d8'] ]
    if not 'timing' in foo:
        foo['timing'] = { 'cycles': 2 }
    opcodes["0x%02X" % opcode] = foo

prefixed = {}

for opcode in range(0x00, 0x100):
    I = opcode >> 4
    N = opcode & 0xF

    foo = {}
    bar = {}

    if I == 0x0:
        if N == 0x0:
            foo['instruction'] = "STPC"
        elif N == 0x1:
            foo['instruction'] = "DTC"
        elif N == 0x2:
            foo['instruction'] = "SPM2"
        elif N == 0x3:
            foo['instruction'] = "SCM2"
        elif N == 0x4:
            foo['instruction'] = "SPM1"
        elif N == 0x5:
            foo['instruction'] = "SCM1"
        elif N == 0x6:
            foo['instruction'] = "LDC"
        elif N == 0x7:
            foo['instruction'] = "STM"
        elif N == 0x8:
            foo['instruction'] = "GEC"
        elif N == 0x9:
            foo['instruction'] = "ETQ"
        elif N == 0xA:
            foo['instruction'] = "XIE"
        elif N == 0xB:
            foo['instruction'] = "XID"
        elif N == 0xC:
            foo['instruction'] = "CIE"
        elif N == 0xD:
            foo['instruction'] = "CID"
    elif I == 0x1:
        pass
    elif I == 0x2:
        bar['instruction'] = "DBNZ"
        bar['operands'] = [ registers[N] ]
        foo['variants'] = [ bar ]
    elif I == 0x3:
        if N == 0xE:
            foo['instruction'] = "BCI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xF:
            foo['instruction'] = "BXI"
            foo['operands'] = [ immediate['d8'] ]
    elif I == 0x4:
        pass
    elif I == 0x5:
        pass
    elif I == 0x6:
        foo['instruction'] = "RLXA"
        foo['operands'] = [ registers[N] ]
    elif I == 0x7:
        if N == 0x4:
            foo['instruction'] = "DADC"
        elif N == 0x6:
            foo['instruction'] = "DSAV"
        elif N == 0x7:
            foo['instruction'] = "DSMB"
        elif N == 0xC:
            foo['instruction'] = "DACI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xF:
            foo['instruction'] = "DSBI"
            foo['operands'] = [ immediate['d8'] ]
    elif I == 0x8:
        foo['instruction'] = "SCAL"
        foo['operands'] = [ registers[N] ]
    elif I == 0x9:
        foo['instruction'] = "SRET"
        foo['operands'] = [ registers[N] ]
    elif I == 0xA:
        foo['instruction'] = "RSXD"
        foo['operands'] = [ registers[N] ]
    elif I == 0xB:
        foo['instruction'] = "RNX"
        foo['operands'] = [ registers[N] ]
    elif I == 0xC:
        foo['instruction'] = "RLDI"
        foo['operands'] = [ registers[N] ]
    elif I == 0xD:
        pass
    elif I == 0xE:
        pass
    elif I == 0xF:
        if N == 0x4:
            foo['instruction'] = "DADD"
        elif N == 0x7:
            foo['instruction'] = "DSM"
        elif N == 0xC:
            foo['instruction'] = "DADI"
            foo['operands'] = [ immediate['d8'] ]
        elif N == 0xF:
            foo['instruction'] = "DSMI"
            foo['operands'] = [ immediate['d8'] ]

    prefixed["0x%02X" % opcode] = foo

with open('opcodes.json', 'w') as fp:
    json.dump({'unprefixed': opcodes, 'cbprefixed': prefixed}, fp, sort_keys=True, indent=4)
