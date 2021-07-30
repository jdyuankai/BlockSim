import csv
import matplotlib.pyplot as plt

# get timestamps of everyblock at 0.001, 0.1 ... spread percent.
def process_and_draw(filename):
    timestamps = {}
    with open('data_v8.csv.bak', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        line = 0;
        for row in spamreader:
            if line == 0:
                line = 1
                continue
            block_num = int(row[2])

            percent = row[5]
            if block_num not in timestamps:
                timestamps[block_num] = {}
            if percent in ["0.001", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"]:
                timestamps[block_num][percent] = float(row[1])

    # select out the wanted --- whose spread percent all exist
    waned_timestamps = {}
    for k, v in timestamps.items():
        if len(v) == 10:
            waned_timestamps[k] = v
    #print(waned_timestamps)

    sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for k in waned_timestamps.keys():
        #print("k = %d" % k)
        sum[1] = sum[1] + waned_timestamps[k]["0.1"] - waned_timestamps[k]["0.001"]
        sum[2] = sum[2] + waned_timestamps[k]["0.2"] - waned_timestamps[k]["0.001"]
        sum[3] = sum[3] + waned_timestamps[k]["0.3"] - waned_timestamps[k]["0.001"]
        sum[4] = sum[4] + waned_timestamps[k]["0.4"] - waned_timestamps[k]["0.001"]
        sum[5] = sum[5] + waned_timestamps[k]["0.5"] - waned_timestamps[k]["0.001"]
        sum[6] = sum[6] + waned_timestamps[k]["0.6"] - waned_timestamps[k]["0.001"]
        sum[7] = sum[7] + waned_timestamps[k]["0.7"] - waned_timestamps[k]["0.001"]
        sum[8] = sum[8] + waned_timestamps[k]["0.8"] - waned_timestamps[k]["0.001"]
        sum[9] = sum[9] + waned_timestamps[k]["0.9"] - waned_timestamps[k]["0.001"]
    #print(sum)
    average = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(sum)):
        average[i] = sum[i]*1000/len(waned_timestamps)
    print(average)
        
    # draw the picture
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    plt.plot(x, average)
    plt.show()

