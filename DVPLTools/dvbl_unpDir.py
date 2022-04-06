import os
import struct
import zlib
from _block import compress, decompress, LZ4BlockError

FOOTER_STRUCTURE = '4I4s'
FOOTER_SIZE = struct.calcsize(FOOTER_STRUCTURE)

inPath = '.\\1_packed'
filesIn = []
for (dirpath, dirnames, filenames) in os.walk(inPath):
    filesIn.extend(filenames)
    break

for fileIn in filesIn:
    infile = inPath + '\\' + fileIn
    outPath = '.\\2_unpacked\\'
    with open(infile, 'rb') as f, open(outPath + fileIn, 'wb') as out:
        f.seek(-FOOTER_SIZE, os.SEEK_END)
        unpacked, packed, crc, ptype, marker = struct.unpack(FOOTER_STRUCTURE, f.read(FOOTER_SIZE))
        f.seek(0)
        result = decompress(f.read(packed), uncompressed_size=unpacked)
        out.write(result)
        out.close()
        f.close()

if filesIn == []:
    print '!!! No files to pack !!!'
else:
    print '_Unpacked_'
