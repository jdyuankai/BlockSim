import pandas as pd
from InputsConfig import InputsConfig as p

class Output:

    cache = []
    block_create_time = {}
    block_syn_ratio_time = {
        '0.2': {},
        '0.4': {},
        '0.6': {},
        '0.8': {},
        '0.9': {},
    }
    average_time = {
        '0.2': 0,
        '0.4': 0,
        '0.6': 0,
        '0.8': 0,
        '0.9': 0,
    }

    def add(timestamp, block_id, recipient_id, counter, ratio):
        Output.cache.append((timestamp, block_id, recipient_id, counter, ratio))
        
        if counter == 1:
            Output.block_create_time[block_id] = timestamp
        elif ratio in (0.2, 0.4, 0.6, 0.8, 0.9):
            Output.block_syn_ratio_time[str(ratio)][block_id] = timestamp

    def calculate():
        counter = 0
        for block_id in Output.block_create_time:
            if block_id in Output.block_syn_ratio_time['0.9']:
                counter += 1
                r = [(ratio, Output.block_syn_ratio_time[ratio][block_id] - Output.block_create_time[block_id]) for ratio in ('0.2', '0.4', '0.6', '0.8', '0.9')]
                for item in r:
                    Output.average_time[item[0]] += item[1]

        print_result = []
        for ratio in Output.average_time:
            Output.average_time[ratio] /= counter
            print_result.append((Output.average_time[ratio], ratio))

        print_result = sorted(print_result, key=lambda k: k[1])

        with open('result.txt', 'a') as file:
            import sys
            sys.stdout = file
            print(str(p.Nn), 'Nodes,', str(p.simTime)+'s and boardcast type of', p.BoardcastType)
            for item in print_result:
                print(item[0], item[1])
            print()
        
    def output_to_xlsx(file_name):
        df= pd.DataFrame(Output.cache)
        df.columns= ['Timestamp', 'Block ID', 'Recipient ID', 'Counter', 'Ratio']
        df = df.sort_values('Timestamp')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='output')
        writer.save()

    def reset():
        cache = []
        block_create_time = {}
        block_syn_ratio_time = {
            '0.2': {},
            '0.4': {},
            '0.6': {},
            '0.8': {},
            '0.9': {},
        }
        average_time = {
            '0.2': 0,
            '0.4': 0,
            '0.6': 0,
            '0.8': 0,
            '0.9': 0,
        }