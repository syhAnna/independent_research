import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


block_freq_read = []
block_freq_write = []

#total_time = 154  #ext4_memoryAndDisk_sx-stackoverflow_3600
#total_time = 273  #ext4_diskOnly_sx-stackoverflow_3600
#total_time = 2472  #btrfs_memoryAndDisk_sx-stackoverflow_3600
#total_time = 390  #btrfs_diskOnly_sx-stackoverflow_3600
#total_time = 2727  #f2fs_memoryAndDisk_sx-stackoverflow_3600
total_time = 1696  #f2fs_diskOnly_sx-stackoverflow_3600


#split_time = 7   #ext4_memoryAndDisk_sx-stackoverflow_3600
#split_time = 7  #ext4_diskOnly_sx-stackoverflow_3600
#split_time = 8  #btrfs_memoryAndDisk_sx-stackoverflow_3600
#split_time = 10  #btrfs_diskOnly_sx-stackoverflow_3600
#split_time = 9  #f2fs_memoryAndDisk_sx-stackoverflow_3600
split_time = 8  #f2fs_diskOnly_sx-stackoverflow_3600


def read_blktrace(file):
    f = open(file)
    collection = [] # list of 【timestamp, r/w】
    time_flag = 0

    for line in f:
        line_element = line.split()
        # if len(line_element) > 0 and line_element[0] == "8,0":
        if len(line_element) > 0 and line_element[0] == "259,0":
            timestamp, rw = float(line_element[3]), line_element[6]
            if rw == "R" or rw == "W":
                collection.append([timestamp, rw])
    collection.sort()

    while time_flag < total_time:
        stop_index, read_count, write_count = 0, 0, 0
        for i in range(len(collection)):
            if time_flag <= collection[i][0] < time_flag + split_time:
                if collection[i][1] == 'R':
                    read_count += 1
                elif collection[i][1] == 'W':
                    write_count += 1
            else:
                stop_index = i
                break

        block_freq_read.append(read_count)
        block_freq_write.append(write_count)

        collection = collection[stop_index:]
        time_flag = time_flag + split_time

    f.close()


if __name__ == "__main__":
    # read_blktrace("wiki-Talk")
    filename = "f2fs_diskOnly_sx-stackoverflow_3600"

    read_blktrace(filename)
    num = int(total_time / split_time)
    x = list(np.linspace(0, total_time, num=num))

    plt.plot(x, block_freq_read, label="read")
    plt.plot(x, block_freq_write, label="write")

    #plt.plot(x, block_freq_read, 'bo-', label="read")
    #plt.plot(x, block_freq_write, 'ro-', label="write")

    plt.xlabel("time")
    plt.ylabel("access frequency")

    plt.title("blocktrace analysis")
    plt.legend()
    plt.show()

    np.savetxt('csv/{}_focus.csv'.format(filename), block_freq_write)

    print("finished")
