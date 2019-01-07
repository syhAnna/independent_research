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

if __name__ == "__main__":
    filename = "f2fs_memoryAndDisk_sx-stackoverflow_3600"
    read_blktrace(filename)
    block_lst = [[item[0], item[1]] for item in block_freq.items()]
    block_lst = sorted(block_lst, key=lambda kv: kv[1])
    block_lst.reverse()
    num = np.array(block_lst)
    max_access = num[..., 1][0]


    x = np.linspace(0, num.shape[0], num=num.shape[0])
    plt.plot(x, num[..., 1])

    plt.xlabel("block")
    plt.ylabel("access times")

    plt.title("Frequency distribution")
    plt.legend()
    plt.savefig('png/{}.png'.format(filename), dpi=1200)

    np.savetxt('csv/{}.csv'.format(filename), num)
    print("finished")




    # x = np.linspace(0, 250, num=250)
    # plt.plot(x, num[..., 1][:250])
    #
    # plt.xlabel("block")
    # plt.ylabel("access times")
    #
    # plt.title("Frequency distribution")
    # plt.legend()
    # plt.savefig('png/{}_focus.png'.format(filename), dpi=1200)
    #
    # np.savetxt('csv/{}_focus.csv'.format(filename), num)
    # print("finished")