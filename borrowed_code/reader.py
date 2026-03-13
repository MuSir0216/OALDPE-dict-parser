# MIT License

# Copyright (c) 2019 Yugang LIU

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import struct
import zlib

from .readmdict import MDX


def get_record(md, offset, length):
    f = open(md._fname, "rb")
    f.seek(md._record_block_offset)

    num_record_blocks = md._read_number(f)
    num_entries = md._read_number(f)
    assert num_entries == md._num_entries
    record_block_info_size = md._read_number(f)
    md._read_number(f)

    compressed_offset = f.tell() + record_block_info_size
    decompressed_offset = 0
    for i in range(num_record_blocks):
        compressed_size = md._read_number(f)
        decompressed_size = md._read_number(f)
        if (decompressed_offset + decompressed_size) > offset:
            break
        decompressed_offset += decompressed_size
        compressed_offset += compressed_size

    f.seek(compressed_offset)
    block_compressed = f.read(compressed_size)
    block_type = block_compressed[:4]
    adler32 = struct.unpack(">I", block_compressed[4:8])[0]

    if block_type == b"\x00\x00\x00\x00":
        record_block = block_compressed[8:]
    elif block_type == b"\x01\x00\x00\x00":
        try:
            from .base import lzo
        except ImportError:
            lzo = None
            print("LZO compression support is not available")
            return
        record_block = lzo.decompress(
            block_compressed[8:], initSize=decompressed_size, blockSize=1308672
        )
    elif block_type == b"\x02\x00\x00\x00":
        record_block = zlib.decompress(block_compressed[8:])
    assert adler32 == zlib.adler32(record_block) & 0xFFFFFFFF
    assert len(record_block) == decompressed_size

    record_start = offset - decompressed_offset
    if length > 0:
        record_null = record_block[record_start : record_start + length]
    else:
        record_null = record_block[record_start:]
    f.close()

    return record_null.strip().decode(md._encoding)


def query(source, word, substyle=False, passcode=None):
    record = []
    if source.endswith(".mdx"):
        encoding = ""
        md = MDX(source, encoding, substyle, passcode)
    word = word.encode("UTF-8")
    for x in range(len(md._key_list)):
        offset, key = md._key_list[x]
        if word == key:
            if (x + 1) < len(md._key_list):
                length = md._key_list[x + 1][0] - offset
            else:
                length = -1
            record.append(get_record(md, offset, length))
    return "\n---\n".join(record)
