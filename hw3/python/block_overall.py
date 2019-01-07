import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


block_freq = {}

def read_blktrace(file):
    f = open(file)
    for line in f:
        # print(line)
        line_element = line.split()
        if len(line_element) > 0 and line_element[0] == "259,0":
            # print(line_element)
            block_num= int(line_element[7])
            if block_num not in block_freq:
                block_freq[block_num] = 0
            block_freq[block_num] += 1
    f.close()
    block_lst = [[item[0], item[1]] for item in block_freq.items()]
    block_lst = sorted(block_lst, key=lambda kv: kv[1])
    block_lst.reverse()
    num = np.array(block_lst)
    return num

if __name__ == "__main__":
    filename = "{}_{}_sx-stackoverflow_3600"
    block_freq = {}
    num1 = read_blktrace(filename.format("ext4", "memoryAndDisk"))
    block_freq = {}
    num2 = read_blktrace(filename.format("btrfs", "memoryAndDisk"))
    block_freq = {}
    num3 = read_blktrace(filename.format("f2fs", "memoryAndDisk"))

    max_block = max(num1.shape[0], num2.shape[0], num3.shape[0])

    if num1.shape[0] == max_block:
        _num1 = num1[..., 1]
        _num2 = np.concatenate((num2[..., 1], np.zeros(max_block - num2.shape[0])))
        _num3 = np.concatenate((num3[..., 1], np.zeros(max_block - num3.shape[0])))
    elif num1.shape[0] == max_block:
        _num1 = np.concatenate((num1[..., 1], np.zeros(max_block - num1.shape[0])))
        _num2 = num2[..., 1]
        _num3 = np.concatenate((num3[..., 1], np.zeros(max_block - num3.shape[0])))
    else:
        _num1 = np.concatenate((num1[..., 1], np.zeros(max_block - num1.shape[0])))
        _num2 = np.concatenate((num2[..., 1], np.zeros(max_block - num2.shape[0])))
        _num3 = num3[..., 1]

    # x = np.linspace(0, max_block, num=max_block)
    x = np.linspace(0, max_block, num=max_block)[:250]


    # plt.plot(x, _num1, label="ext4")
    # plt.plot(x, _num2, label="btrfs")
    # plt.plot(x, _num3, label="f2fs")
    plt.plot(x, _num1[:250], label="ext4")
    plt.plot(x, _num2[:250], label="btrfs")
    plt.plot(x, _num3[:250], label="f2fs")

    plt.xlabel("block")
    plt.ylabel("access times")

    plt.title("Frequency distribution")
    plt.legend()

    # plt.savefig('png/{}.png'.format("{} Frequency distribution".format("overall")), dpi=1200)
    plt.savefig('png/{}_focus.png'.format("{} Frequency distribution".format("overall")), dpi=1200)

    print("finished")