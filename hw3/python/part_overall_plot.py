import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


#total_time1 = 154  #ext4_memoryAndDisk_sx-stackoverflow_3600
#total_time2 = 273  #ext4_diskOnly_sx-stackoverflow_3600
#total_time3 = 2472  #btrfs_memoryAndDisk_sx-stackoverflow_3600
#total_time4 = 390  #btrfs_diskOnly_sx-stackoverflow_3600
total_time5 = 2727  #f2fs_memoryAndDisk_sx-stackoverflow_3600
total_time6 = 1696  #f2fs_diskOnly_sx-stackoverflow_3600

#split_time1 = 7   #ext4_memoryAndDisk_sx-stackoverflow_3600
#split_time2 = 7  #ext4_diskOnly_sx-stackoverflow_3600
#split_time3 = 8  #btrfs_memoryAndDisk_sx-stackoverflow_3600
#split_time4 = 10  #btrfs_diskOnly_sx-stackoverflow_3600
split_time5 = 9  #f2fs_memoryAndDisk_sx-stackoverflow_3600
split_time6 = 8  #f2fs_diskOnly_sx-stackoverflow_3600


def read_blktrace(file, total_time, split_time):
    f = open(file)
    w_collection = [] # list of 【timestamp, r/w】
    time_flag = 0
    block_freq_write = []

    for line in f:
        line_element = line.split()
        # if len(line_element) > 0 and line_element[0] == "8,0":
        if len(line_element) > 0 and line_element[0] == "259,0":
            timestamp, rw = float(line_element[3]), line_element[6]
            if rw == "W":
                w_collection.append(float(timestamp))
    w_collection.sort()

    while time_flag < total_time:
        stop_index, read_count, write_count = 0, 0, 0
        for i in range(len(w_collection)):
            if time_flag <= w_collection[i] < time_flag + split_time:
                write_count += 1
            else:
                stop_index = i
                break

        block_freq_write.append(write_count)

        w_collection = w_collection[stop_index:]
        time_flag = time_flag + split_time

    f.close()

    return block_freq_write


def remove_trailing_zero(l):
    index = 0
    for i in range(len(l)):
        if l[index:] == [0] * (len(l) - i):
            break
        else:
            index += 1
    return index


if __name__ == "__main__":
    # read_blktrace("wiki-Talk")
    #ext4_blk0 = read_blktrace("ext4_memoryAndDisk_sx-stackoverflow_3600", total_time1, split_time1)
    #ext4_blk1 = read_blktrace("ext4_diskOnly_sx-stackoverflow_3600", total_time2, split_time2)

    #btrfs_blk0 = read_blktrace("btrfs_memoryAndDisk_sx-stackoverflow_3600", total_time3, split_time3)
    #btrfs_blk1 = read_blktrace ( "btrfs_diskOnly_sx-stackoverflow_3600", total_time4, split_time4)

    f2fs_blk0 = read_blktrace("btrfs_diskOnly_sx-stackoverflow_3600", total_time5, split_time5)
    f2fs_blk1 = read_blktrace("btrfs_memoryAndDisk_sx-stackoverflow_3600", total_time6, split_time6)

    index0 = remove_trailing_zero(f2fs_blk0)
    blk0 = f2fs_blk0[:index0]

    index1 = remove_trailing_zero(f2fs_blk1)
    blk1 = f2fs_blk1[:index1]

    num1 = len(blk0)
    num2 = len(blk1)

    x1 = list(np.linspace(0, total_time5, num=num1))
    x2 = list(np.linspace(0, total_time6, num=num2))

    plt.plot(x1, blk0, label="diskOnly")
    plt.plot(x2, blk1, label="memoryAndDisk")

    plt.xlabel("time")
    plt.ylabel("access frequency")

    plt.title("blocktrace analysis - Memory and Disk")
    plt.legend()
    plt.show()

    print("finished")
