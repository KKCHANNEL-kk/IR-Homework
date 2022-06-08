# 单个数字的VB编码结果，每8位用一个ascii字符表示，返回字符列表
def VBEncodeNumber(n):
    bytes = []
    while True:
        temp = n % 128
        bytes.insert(0, chr(temp))
        if n < 128:
            break
        n = n//128
    bytes[-1] = chr(ord(bytes[-1])+128)
    return bytes


# 合并每个数字的VB编码结果得到的字符列表
def VBEncode(numbers):
    bytestream = []
    for n in numbers:
        bytes = VBEncodeNumber(n)
        bytestream += (bytes)
    return bytestream


# 将每个ascii字符转化为0-255的对应数字，解析出数字列表
def VBDecode(bytestream):
    numbers = []
    n = 0
    for byte in bytestream:
        bin_num = ord(byte)
        if bin_num < 128:
            n = 128*n+bin_num
        else:
            n = 128*n+(bin_num-128)
            numbers.append(n)
            n = 0
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


# 将编码后的ascii字符列表转化为8位补齐的二进制编码
def encode2bin(encode):
    ret = []
    for i in encode:
        ret.append('{:08b}'.format(ord(i)))
    return ret


index = [113, 309, 720]
print('普通倒排索引：', index)
dis = normal2dis(index)
print('保存间隔倒排索引：', dis)
encode = VBEncode(dis)
print('编码为ascii字符列表的间隔索引：', encode)
print('对应的二进制流：', encode2bin(encode))
decode = VBDecode(encode)
print('解码获得的间隔索引：', decode)
normal = dis2normal(decode)
print('间隔索引还原为正常的倒排索引：', normal)
