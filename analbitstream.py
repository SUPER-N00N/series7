#!/usr/bin/python

import sys
import binascii
import struct

f = open(sys.argv[1]);
data = f.read();

i = 0;
word = 0;
s = '';
opcodes = {
	   0b00000000000000000000000000000000: 'nop',
	   0b00001000000000000000000000000000: 'read',
	   0b00010000000000000000000000000000: 'write',
	   0b00011000000000000000000000000000: 'reserved opcode'};
registers = {
	   0b00000000000000000000000000000000: 'CRC',
	   0b00000000000000000010000000000000: 'FAR',
	   0b00000000000000000100000000000000: 'FDRI',
	   0b00000000000000000110000000000000: 'FDRO',
	   0b00000000000000001000000000000000: 'CMD',
	   0b00000000000000001010000000000000: 'CTL0',
	   0b00000000000000001100000000000000: 'MASK',
	   0b00000000000000001110000000000000: 'STAT',
	   0b00000000000000010000000000000000: 'LOUT',
	   0b00000000000000010010000000000000: 'COR0',
	   0b00000000000000010100000000000000: 'MFWR',
	   0b00000000000000010110000000000000: 'CBC',
	   0b00000000000000011000000000000000: 'IDCODE',
	   0b00000000000000011010000000000000: 'AXSS',
	   0b00000000000000011100000000000000: 'COR1',
	   0b00000000000000100000000000000000: 'WBSTAR',
	   0b00000000000000100010000000000000: 'TIMER',
	   0b00000000000000101100000000000000: 'BOOTST',
	   0b00000000000000110000000000000000: 'CTL1',
	   0b00000000000000111110000000000000: 'BSPI'};


header_types = {0x20000000 : 'Type 1',
		0x40000000 : 'Type 2'};

TYPE1_MASK = 0x20000000;
TYPE2_MASK = 0x40000000;

OPCODE_MASK  =           0b00011000000000000000000000000000;

TYPE_MASK    =           0b11100000000000000000000000000000;

REG_ADD_MASK =           0b00000000000000111110000000000000;
TYPE1_ADD_MASK =         0b00000000000000111110000000000000;
TYPE1_WORD_COUNT_MASK =  0b00000000000000000000011111111111;
TYPE2_WORD_COUNT_MASK =  0b00000111111111111111111111111111;

OP_NOP      = 0b00;
OP_READ     = 0b01;
OP_WRITE    = 0b10;
OP_RESERVED = 0b11; 


word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word):
	w = struct.unpack('>B', data[i + j])[0];
	s += format(w, '02x')
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word):
	w = struct.unpack('>B', data[i + j])[0];
	s += format(w, '02x')
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word - 1):
	s += data[i + j];
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">B", data[i])[0];
print format(i, '08x') + ': ' + format(word, '02x');
i += 1;
s = '';
word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word - 1):
	s += data[i + j];
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">B", data[i])[0];
print format(i, '08x') + ': ' + format(word, '02x');
i += 1;
s = '';
word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word - 1):
	s += data[i + j];
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">B", data[i])[0];
print format(i, '08x') + ': ' + format(word, '02x');
i += 1;
s = '';
word = struct.unpack(">H", data[i]+ data[i+1])[0];
print format(i, '08x') + ': ' + format(word, '04x');
i += 2;
for j in range(0, word - 1):
	s += data[i + j];
print format(i, '08x') + ': ' + s;
i += word;
s = '';
word = struct.unpack(">B", data[i])[0];
print format(i, '08x') + ': ' + format(word, '02x');
i += 1;
word = struct.unpack(">L", data[i]+ data[i+1] + data[i+2] + data[i+3])[0];
print format(i, '08x') + ': ' + format(word, '08x');
check = lambda dictionary, mask, word : dictionary[word & mask] if (word & mask) in dictionary else None
while i < (len(data)):
	i += 4;
	word = struct.unpack(">L", data[i]+ data[i+1] + data[i+2] + data[i+3])[0];
        line = format(i, '08x') + ': ' + format(word, '08x') +  ' ';
        c = check(header_types, TYPE_MASK, word);
        if c != None:
		line += c + ' ';
	else:
		print line;
		continue;
	if c == 'Type 1':
		c = check(opcodes, OPCODE_MASK, word);
		if (c != None):
			line += c + ' ';
			if c == 'nop': print line; continue;
		else:
			print line;
			continue;
		c = check(registers, REG_ADD_MASK, word);
		if c != None:
			line += c + ' ';
		else:
			print line;
			continue;
	print line;
#	print format(i, '08x') + ': ' + format(word, '08x') +  ' ' + \
#			       
#			       check(header_types, TYPE_MASK, word) + ' ' + \
#			       check(opcodes, OPCODE_MASK, word) + ' ' + \
#			       (opcodes[word] if word in opcodes else '');


