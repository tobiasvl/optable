import json

registers = [
    {"name": "B", "description": "8-bit register B", "type": "register"},
    {"name": "C", "description": "8-bit register C", "type": "register"},
    {"name": "D", "description": "8-bit register D", "type": "register"},
    {"name": "E", "description": "8-bit register E", "type": "register"},
    {"name": "H", "description": "8-bit register H", "type": "register"},
    {"name": "L", "description": "8-bit register L", "type": "register"},
    {"name": "M", "description": "Memory location pointed to by register pair HL", "type": "memory"},
    {"name": "A", "description": "8-bit accumulator A", "type": "register"}
]

register_pairs = [
    {"name": "B", "description": "16-bit register pair BC", "type": "register pair" },
    {"name": "D", "description": "16-bit register pair DE", "type": "register pair" },
    {"name": "H", "description": "16-bit register pair HL", "type": "register pair" },
    {"name": "SP", "description": "16-bit Stack Pointer", "type": "register pair" },
    {"name": "PSW", "description": "16-bit register pair constructed from Accumulator A and flags", "type": "register pair" }
]

condition_codes = [
    #{"name": "NZ", "description": "Not Zero"},
    #{"name": "Z", "description": "Zero"},
    #{"name": "NC", "description": "Not Carry"},
    #{"name": "C", "description": "Carry"},
    #{"name": "PO", "description": "Carry"},
    #{"name": "PE", "description": "Carry"},
    #{"name": "P", "description": "Carry"},
    #{"name": "M", "description": "Carry"}
    "NZ",
    "Z", 
    "NC",
    "C", 
    "PO",
    "PE",
    "P", 
    "M", 
]

immediate = {
    "d8": {"name": "d8", "description": "8-bit immediate value", "bytes": 1, "type": "immediate"},
    "d16": {"name": "d16", "description": "16-bit immediate value", "bytes": 2, "type": "immediate"},
    "a16": {"name": "a16", "description": "16-bit immediate address", "bytes": 2, "type": "immediate"}
}
    
inherent = [
    {"name": "0", "type": "inherent", "description": "Restart subroutine 0 at address 0x0000"},
    {"name": "1", "type": "inherent", "description": "Restart subroutine 1 at address 0x0008"},
    {"name": "2", "type": "inherent", "description": "Restart subroutine 2 at address 0x0010"},
    {"name": "3", "type": "inherent", "description": "Restart subroutine 3 at address 0x0018"},
    {"name": "4", "type": "inherent", "description": "Restart subroutine 4 at address 0x0020"},
    {"name": "5", "type": "inherent", "description": "Restart subroutine 5 at address 0x0028"},
    {"name": "6", "type": "inherent", "description": "Restart subroutine 6 at address 0x0030"},
    {"name": "7", "type": "inherent", "description": "Restart subroutine 7 at address 0x0038"}
]

opcodes = {}

for opcode in range(0x00, 0x100):
    d = registers[(opcode & 0x38) >> 3]
    rp = register_pairs[(opcode & 0x30) >> 4]
    s = registers[opcode & 7]

    foo = {}

    if opcode & 0xC0 == 0x00:
        if opcode == 0x00:
            foo['instruction'] = "NOP"
            foo['timing'] = {
                'cycles': 1,
                'states': 4
            }
        elif opcode & 0x07 == 0x06:
            foo['instruction'] = "MVI"
            foo['operands'] = [
                d,
                immediate["d8"]
            ]
            if d['name'] == 'M':
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            else:
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
        elif opcode & 0x07 == 0x01:
            if opcode & 0x08 == 0x00:
                foo['instruction'] = "LXI"
                foo['operands'] = [
                    rp,
                    immediate["d16"]
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10
                }
            else:
                foo['instruction'] = "DAD"
                foo['operands'] = [
                    rp
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10
                }
        elif opcode & 0x07 == 0x02:
            if opcode == 0x22:
                foo['instruction'] = "SHLD"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 5,
                    'states': 16
                }
            elif opcode == 0x2A:
                foo['instruction'] = "LHLD"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 5,
                    'states': 16
                }
            elif opcode == 0x32:
                foo['instruction'] = "STA"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 4,
                    'states': 13
                }
            elif opcode == 0x3A:
                foo['instruction'] = "LDA"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 4,
                    'states': 13
                }
            elif opcode & 0x08 == 0x08:
                foo['instruction'] = "LDAX"
                foo['operands'] = [
                    rp
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
                # TODO only BC and DE are allowed
                assert(rp["name"] == "B" or rp["name"] == "D")
            elif opcode & 0x08 == 0x00:
                foo['instruction'] = "STAX"
                foo['operands'] = [
                    rp
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
                # TODO only BC and DE are allowed
                assert(rp["name"] == "B" or rp["name"] == "D")
        elif opcode & 0x07 == 0x03:
            foo['timing'] = {
                'cycles': 1,
                'states': 5,
                'variant': {
                    'cycles': 1,
                    'states': 6
                }
            }
            if opcode & 0x08 == 0x00:
                foo['instruction'] = "INX"
                foo['operands'] = [
                    rp
                ]
            else:
                foo['instruction'] = "DCX"
                foo['operands'] = [
                    rp
                ]
        elif opcode & 0x07 == 0x04:
            foo['instruction'] = "INR"
            foo['operands'] = [
                d
            ]
            if d['name'] == 'M':
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 5,
                    'variant': {
                        'cycles': 1,
                        'states': 4,
                    }
                }
        elif opcode & 0x07 == 0x05:
            foo['instruction'] = "DCR"
            foo['operands'] = [
                d
            ]
            if d['name'] == 'M':
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 5,
                    'variant': {
                        'cycles': 1,
                        'states': 4
                    }
                }
        elif opcode & 0x07 == 0x06:
            # none?
            pass
        elif opcode & 0x07 == 0x07:
            op = opcode >> 3
            foo['timing'] = {
                'cycles': 1,
                'states': 4
            }
            if op == 0:
                foo['instruction'] = "RLC"
            elif op == 1:
                foo['instruction'] = "RRC"
            elif op == 2:
                foo['instruction'] = "RAL"
            elif op == 3:
                foo['instruction'] = "RAR"
            elif op == 4:
                foo['instruction'] = "DAA"
            elif op == 5:
                foo['instruction'] = "CMA"
            elif op == 6:
                foo['instruction'] = "STC"
            elif op == 7:
                foo['instruction'] = "CMC"
    elif opcode & 0xC0 == 0x40:
        if opcode == 0x76:
            foo['instruction'] = "HLT"
            foo['timing'] = {
                'cycles': 1,
                'states': 7,
                'variant': {
                    'cycles': 1,
                    'states': 5
                }
            }
        else:
            foo['instruction'] = "MOV"
            foo['operands'] = [
                d,
                s
            ]
            if d['name'] == 'M' or s['name'] == 'M':
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7,
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 5,
                    'variant': {
                        'cycles': 1,
                        'states': 4,
                    }
                }
    elif opcode & 0xC0 == 0x80:
        op = (opcode - 0x80) >> 3
        if op == 0:
            foo['instruction'] = "ADD"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 1:
            foo['instruction'] = "ADC"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 2:
            foo['instruction'] = "SUB"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 3:
            foo['instruction'] = "SBB"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 4:
            foo['instruction'] = "ANA"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 5:
            foo['instruction'] = "XRA"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 6:
            foo['instruction'] = "ORA"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif op == 7:
            foo['instruction'] = "CMP"
            foo['operands'] = [
                s
            ]
            if s['name'] == "M":
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            else:
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
    elif opcode & 0xC0 == 0xC0:
        op = (opcode - 0xC0) >> 3
        if opcode & 0x07 == 0x00:
            foo['instruction'] = "R" + condition_codes[op]
            foo['timing'] = {
                'cycles': [1, 3],
                'states': [5, 11],
                'variant': {
                    'cycles': [1, 3],
                    'states': [6, 12],
                }
            }
        elif opcode & 0x07 == 0x01:
            if opcode & 0x08 == 0x00:
                foo['instruction'] = "POP"
                if rp["name"] == "SP":
                    rp = register_pairs[-1]
                    foo["flags"] = {
                        "S": "S",
                        "Z": "Z",
                        "K": "K",
                        "A": "A",
                        "V": "V",
                        "P": "P",
                        "C": "C"
                    }
                foo['operands'] = [
                    rp
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            else:
                if op == 1:
                    foo['instruction'] = "RET"
                    foo['timing'] = {
                        'cycles': 3,
                        'states': 10,
                    }
                elif op == 5:
                    foo['instruction'] = "PCHL"
                    foo['timing'] = {
                        'cycles': 1,
                        'states': 5,
                        'variant': {
                            'cycles': 1,
                            'states': 6
                        }
                    }
                elif op == 7:
                    foo['instruction'] = "SPHL"
                    foo['timing'] = {
                        'cycles': 1,
                        'states': 5,
                        'variant': {
                            'cycles': 1,
                            'states': 6
                        }
                    }
        elif opcode & 0x07 == 0x02:
            foo['instruction'] = "J" + condition_codes[op]
            foo['operands'] = [
                immediate["a16"]
            ]
            foo['timing'] = {
                'cycles': 3,
                'states': 10,
                'variant': {
                    'cycles': [2, 3],
                    'states': [7, 10]
                }
            }
        elif opcode & 0x07 == 0x03:
            if op == 0:
                foo['instruction'] = "JMP"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10
                }
            elif op == 2:
                foo['instruction'] = "OUT"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            elif op == 3:
                foo['instruction'] = "IN"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 10,
                }
            elif op == 4:
                foo['instruction'] = "XTHL"
                foo['timing'] = {
                    'cycles': 5,
                    'states': 17,
                    'variant': {
                        'cycles': 5,
                        'states': 18
                    }
                }
            elif op == 5:
                foo['instruction'] = "XCHG"
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
            elif op == 6:
                foo['instruction'] = "DI"
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
            elif op == 7:
                foo['instruction'] = "EI"
                foo['timing'] = {
                    'cycles': 1,
                    'states': 4
                }
        elif opcode & 0x07 == 0x04:
            foo['instruction'] = "C" + condition_codes[op]
            foo['operands'] = [
                immediate["a16"]
            ]
            foo['timing'] = {
                'cycles': [3, 5],
                'states': [11, 17],
                'variant': {
                    'cycles': [2, 5],
                    'states': [9, 18]
                }
            }
        elif opcode & 0x07 == 0x05:
            if opcode & 0x08 == 0x00:
                foo['instruction'] = "PUSH"
                if rp["name"] == "SP":
                    rp = register_pairs[-1]
                    foo['timing'] = {
                        'cycles': 3,
                        'states': 11,
                        'variant': {
                            'cycles': 3,
                            'states': 12
                        }
                    }
                foo['operands'] = [
                    rp
                ]
                foo['timing'] = {
                    'cycles': 3,
                    'states': 11,
                    'variant': {
                        'cycles': 3,
                        'states': 13
                    }
                }
            else:
                foo['instruction'] = "CALL"
                foo['operands'] = [
                    immediate["a16"]
                ]
                foo['timing'] = {
                    'cycles': 5,
                    'states': 17,
                    'variant': {
                        'cycles': 5,
                        'states': 18
                    }
                }
        elif opcode & 0x07 == 0x06:
            if op == 0:
                foo['instruction'] = "ADI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 1:
                foo['instruction'] = "ACI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 2:
                foo['instruction'] = "SUI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 3:
                foo['instruction'] = "SBI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 4:
                foo['instruction'] = "ANI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 5:
                foo['instruction'] = "XRI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 6:
                foo['instruction'] = "ORI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
            elif op == 7:
                foo['instruction'] = "CPI"
                foo['operands'] = [
                    immediate["d8"]
                ]
                foo['timing'] = {
                    'cycles': 2,
                    'states': 7
                }
        elif opcode & 0x07 == 0x07:
            foo['instruction'] = "RST"
            foo['operands'] = [
                inherent[op]
            ]
            foo['timing'] = {
                'cycles': 3,
                'states': 11,
                'variant': {
                    'cycles': 3,
                    'states': 12
                }
            }

    opcodes["0x%02X" % opcode] = foo

# Undocumented opcodes
opcodes["0x10"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'ARHL',
            'timing': {
                'cycles': 2,
                'states': 7,
            },
            'flags': {
                'C': 'C'
            },
            'illegal': True
        }
    ]
}
opcodes["0x20"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    'timing': {
        'cycles': 1,
        'states': 4,
    },
    "variants": [
        {
            'instruction': 'RIM',
            'timing': {
                'cycles': 3,
                'states': 10,
            }
        }
    ]
}
opcodes["0x30"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    'timing': {
        'cycles': 1,
        'states': 4,
    },
    "variants": [
        {
            'instruction': 'SIM',
            'timing': {
                'cycles': 1,
                'states': 4,
            }
        }
    ]
}
opcodes["0x08"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'DSUB',
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            "flags": {
                "S": "S",
                "Z": "Z",
                "K": "K",
                "A": "A",
                "V": "V",
                "P": "P",
                "C": "C"
            },
            'illegal': True
        }
    ]
}
opcodes["0x18"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'RDEL',
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            'flags': {
                'C': 'C',
                'V': 'V'
            },
            'illegal': True
        }
    ]
}
opcodes["0x28"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'LDHI',
            "operands": [ immediate["d8"] ],
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            'illegal': True
        }
    ]
}
opcodes["0x38"] = {
    'instruction': "NOP",
    'timing': {
        'cycles': 1,
        'states': 4
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'LDSI',
            "operands": [ immediate["d8"] ],
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            'illegal': True
        }
    ]
}
opcodes["0xD9"] = {
    'instruction': "RET",
    'timing': {
        'cycles': 3,
        'states': 10,
    },
    "illegal": True,
    "variants": [
        {
            'instruction': 'SHLX',
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            'illegal': True
        }
    ]
}
opcodes["0xCB"] = {
    'instruction': "JMP",
    'timing': {
        'cycles': 3,
        'states': 10,
    },
    "operands": [ immediate["a16"] ],
    "illegal": True,
    "variants": [
        {
            'instruction': 'RSTV',
            'timing': {
                'cycles': [1, 3],
                'states': [6, 12]
            },
            'illegal': True
        }
    ]
}
opcodes["0xDD"] = {
    'instruction': "CALL",
    'timing': {
        'cycles': 5,
        'states': 17,
    },
    "operands": [ immediate["a16"] ],
    "illegal": True,
    "variants": [
        {
            'instruction': 'JNK',
            "operands": [ immediate["a16"] ],
            'timing': {
                'cycles': [2, 3],
                'states': [7, 10]
            },
            'illegal': True
        }
    ]
}
opcodes["0xED"] = {
    'instruction': "CALL",
    'timing': {
        'cycles': 5,
        'states': 17,
    },
    "operands": [ immediate["a16"] ],
    "illegal": True,
    "variants": [
        {
            'instruction': 'LHLX',
            'timing': {
                'cycles': 3,
                'states': 10,
            },
            'illegal': True
        }
    ]
}
opcodes["0xFD"] = {
    'instruction': "CALL",
    'timing': {
        'cycles': 5,
        'states': 17,
    },
    "operands": [ immediate["a16"] ],
    "illegal": True,
    "variants": [
        {
            'instruction': 'JNK',
            "operands": [ immediate["a16"] ],
            'timing': {
                'cycles': [2, 3],
                'states': [7, 10]
            },
            'illegal': True
        }
    ]
}

with open('opcodes.json', 'w') as fp:
    json.dump({'unprefixed': opcodes}, fp, sort_keys=True, indent=4)
