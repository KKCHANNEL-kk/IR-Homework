import math

def gammaEncodeNumber(n):
    unary_length = math.floor(math.log(n,2)) 
    offset = n - 2**unary_length
    ret = '1'*unary_length + '0' + bin(offset)[2:].zfill(unary_length)
    return ret

def gammaEncode(numbers):
    bytestream = []
    for n in numbers:
        bytes = gammaEncodeNumber(n)
        bytestream.append(bytes)
    return bytestream

def gammaDecode(bytestream):
    numbers = []
    for byte in bytestream:
        unary_length = 0
        for i in byte:
            if i == '1':
                unary_length += 1
            else:
                break
        offset = int(byte[unary_length+1:],2)
        
        num = 2**unary_length + offset
        numbers.append(num)
    return numbers


# 将普通倒排索引压缩为保存间隔的倒排索引
def normal2dis(index):
    ret = []
    it = iter(index)
    before = next(it)
    ret.append(before)
    for after in it:
        ret.append(after-before)
        before = after
    return ret


# 将保存间隔的倒排索引解压为普通倒排索引
def dis2normal(dis):
    ret = []
    it = iter(dis)
    before = next(it)
    ret.append(before)
    for gap in it:
        ret.append(before+gap)
        before = before+gap
    return ret


index = [113, 309, 720]
print('普通倒排索引：', index)
dis = normal2dis(index)
print('保存间隔倒排索引：', dis)
encode = gammaEncode(dis)
print('gamma编码为二进制流',encode)
decode = gammaDecode(encode)
print('二进制流解码结果：',decode)
normal = dis2normal(decode)
print('间隔索引还原为正常的倒排索引：', normal)