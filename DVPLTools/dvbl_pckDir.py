import os
import struct
import zlib
from _block import compress, decompress, LZ4BlockError

FOOTER_STRUCTURE = '4I4s'
FOOTER_SIZE = struct.calcsize(FOOTER_STRUCTURE)

inPath = '.\\3_unpacked_mod'
filesIn = []
for (dirpath, dirnames, filenames) in os.walk(inPath):
    filesIn.extend(filenames)
    break

for fileIn in filesIn:
    infile = inPath + '\\' + fileIn
    outPath = '.\\4_packed_mod\\'
    with open(infile, 'rb') as f, open(outPath + fileIn, 'wb') as out:
        unpacked = os.stat(infile).st_size 
        result = compress(f.read(), mode='high_compression', compression=12, store_size=False)
        packed = len(result)
        crc = zlib.crc32(result) & 0xFFFFFFFF
        ptype = 2
        marker = 'DVPL'
        data = struct.pack(FOOTER_STRUCTURE, unpacked, packed, crc, ptype, marker)
        result += data
        out.write(result)
        out.close()
        f.close()
if filesIn == []:
    print '!!! No files to pack !!!'
else:
    print '_Packed_'
