
class InputsConfig:

    """ Seclect the model to be simulated.
    0 : The base model
    1 : Bitcoin model
    2 : Ethereum model
    3 : Trias model
    """
    model=3

    ''' Input configurations for the base model '''
    if model==0:

      ''' Block Parameters '''
      Binterval = 600 # Average time (in seconds)for creating a block in the blockchain
      Bsize = 1.0 # The block size in MB
      Bdelay = 0.42 # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
      Breward = 12.5 # Reward for mining a block

      ''' Transaction Parameters '''
      hasTrans = True  # True/False to enable/disable transactions in the simulator
      Ttechnique = "Light" # Full/Light to specify the way of modelling transactions
      Tn= 10 # The rate of the number of transactions to be created per second
      Tdelay = 5.1 # The average transaction propagation delay in seconds (Only if Full technique is used)
      Tfee = 0.000062 # The average transaction fee
      Tsize = 0.000546 # The average transaction size  in MB

      ''' Node Parameters '''
      Nn = 3 # the total number of nodes in the network
      NODES = []
      from Models.Node import Node
      NODES = [Node(id=0), Node(id=1)] # here as an example we define three nodes by assigning a unique id for each one

      ''' Simulation Parameters '''
      simTime= 1000 # the simulation length (in seconds)
      Runs=2 # Number of simulation runs



    ''' Input configurations for Bitcoin model '''
    if model==1:
        ''' Block Parameters '''
        Binterval = 600 # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0 # The block size in MB
        Bdelay = 0.42 # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5 # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light" # Full/Light to specify the way of modelling transactions
        Tn= 10 # The rate of the number of transactions to be created per second
        Tdelay = 5.1 # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tfee = 0.000062 # The average transaction fee
        Tsize = 0.000546 # The average transaction size  in MB

        ''' Node Parameters '''
        Nn = 3 # the total number of nodes in the network
        NODES = []
        from Models.Bitcoin.Node import Node
        NODES = [Node(id=0,hashPower=50), Node(id=1,hashPower=20), Node(id=2,hashPower=30)] # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power

        ''' Simulation Parameters '''
        simTime= 10000 # the simulation length (in seconds)
        Runs=2 # Number of simulation runs



    ''' Input configurations for Ethereum model '''
    if model==2:

        ''' Block Parameters '''
        Binterval = 12.42 # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0 # The block size in MB
        Blimit= 8000000 # The block gas limit
        Bdelay =6 # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 2 # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light" # Full/Light to specify the way of modelling transactions
        Tn= 20 # The rate of the number of transactions to be created per second
        Tdelay = 3 # The average transaction propagation delay in seconds (Only if Full technique is used)
        # The transaction fee in Ethereum is calculated as: UsedGas X GasPrice
        Tsize = 0.000546 # The average transaction size  in MB

        ''' Drawing the values for gas related attributes (UsedGas and GasPrice, CPUTime) from fitted distributions '''

        ''' Uncles Parameters '''
        hasUncles = True # boolean variable to indicate use of uncle mechansim or not
        Buncles=2 # maximum number of uncle blocks allowed per block
        Ugenerations = 7 # the depth in which an uncle can be included in a block
        Ureward =0
        UIreward = Breward / 32 # Reward for including an uncle

        ''' Node Parameters '''
        Nn = 3 # the total number of nodes in the network
        NODES = []
        from Models.Ethereum.Node import Node
        NODES = [Node(id=0,hashPower=50), Node(id=1,hashPower=20), Node(id=2,hashPower=30)] # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power

        ''' Simulation Parameters '''
        simTime= 500 # the simulation length (in seconds)
        Runs=2 # Number of simulation runs


    ''' Input configurations for Trias model '''
    if model==3:
        ''' Block Parameters '''
        Binterval = 600 # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0 # The block size in MB
        # Bdelay = 0.42 # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        # Bdelay = [
        #     [ float("inf")     , 21.62 , 24.42 , 0.57  , 7.74  , 9.18  , 1.01  , 0.76  , 18.44 , 21.14 , 26.56 , 19.78 , 23.61 , 16.76 , 23.34 , 21.5  , 24.11 , 23.54 ],
        #     [ 21.62 , float("inf")     , 19.31 , 21.47 , 28.97 , 21.35 , 21.12 , 20.89 , 3.63  , 0.68  , 6.12  , 8.61  , 3.84  , 13.02 , 17.38 , 23.68 , 13.5  , 18.4  ],
        #     [ 24.42 , 19.31 , float("inf")     , 24.4  , 27.85 , 30.31 , 23.88 , 25.03 , 17.9  , 19.61 , 23.9  , 17.96 , 19.91 , 9.17  , 2.22  , 9.85  , 8.51  , 1.12  ],
        #     [ 0.57  , 21.47 , 24.4  , float("inf")     , 7.2   , 8.98  , 1.47  , 0.49  , 18.79 , 22.33 , 28.24 , 20.79 , 23.4  , 18.78 , 25.77 , 25.47 , 15.34 , 26.08 ],
        #     [ 7.74  , 28.97 , 27.85 , 7.2   , float("inf")     , 16    , 7.99  , 7.57  , 10.47 , 19.58 , 11.97 , 17.15 , 12.21 , 11.71 , 32.15 , 16.72 , 40.13 , 26.01 ],
        #     [ 9.18  , 21.35 , 30.31 , 8.98  , 16    , float("inf")     , 9.38  , 9.21  , 16.17 , 25.17 , 6.62  , 37.8  , 15.45 , 11.66 , 26.84 , 12.99 , 34.76 , 30.03 ],
        #     [ 1.01  , 21.12 , 23.88 , 1.47  , 7.99  , 9.38  , float("inf")     , 0.52  , 25.82 , 20.5  , 15.36 , 21.77 , 21.49 , 29.29 , 23.51 , 19.49 , 19.35 , 24.02 ],
        #     [ 0.76  , 20.89 , 25.03 , 0.49  , 7.57  , 9.21  , 0.52  , float("inf")     , 19.21 , 22.96 , 18.89 , 22.72 , 20.42 , 31.77 , 22.22 , 26.9  , 28.28 , 26.02 ],
        #     [ 18.44 , 3.63  , 17.9  , 18.79 , 10.47 , 16.17 , 25.82 , 19.21 , float("inf")     , 3.47  , 6.08  , 7.5   , 7.39  , 18.24 , 22.64 , 19.38 , 27.24 , 14.79 ],
        #     [ 21.14 , 0.68  , 19.61 , 22.33 , 19.58 , 25.17 , 20.5  , 22.96 , 3.47  , float("inf")     , 5.55  , 8.7   , 3.93  , 10.25 , 16.57 , 28.24 , 10.8  , 20.63 ],
        #     [ 26.56 , 6.12  , 23.9  , 28.24 , 11.97 , 6.62  , 15.36 , 18.89 , 6.08  , 5.55  , float("inf")     , 3.35  , 5.76  , 4.48  , 16.02 , 14.44 , 26.07 , 25.23 ],
        #     [ 19.78 , 8.61  , 17.96 , 20.79 , 17.15 , 37.8  , 21.77 , 22.72 , 7.5   , 8.7   , 3.35  , float("inf")     , 9.07  , 9.9   , 24.59 , 37.7  , 6.67  , 13.57 ],
        #     [ 23.61 , 3.84  , 19.91 , 23.4  , 12.21 , 15.45 , 21.49 , 20.42 , 7.39  , 3.93  , 5.76  , 9.07  , float("inf")     , 32.04 , 24.7  , 16.57 , 19.08 , 19.81 ],
        #     [ 16.76 , 13.02 , 9.17  , 18.78 , 11.71 , 11.66 , 29.29 , 31.77 , 18.24 , 10.25 , 4.48  , 9.9   , 32.04 , float("inf")     , 8.48  , 15.94 , 13.06 , 8.33  ],
        #     [ 23.34 , 17.38 , 2.22  , 25.77 , 32.15 , 26.84 , 23.51 , 22.22 , 22.64 , 16.57 , 16.02 , 24.59 , 24.7  , 8.48  , float("inf")     , 7.77  , 9.45  , 1.52  ],
        #     [ 21.5  , 23.68 , 9.85  , 25.47 , 16.72 , 12.99 , 19.49 , 26.9  , 19.38 , 28.24 , 14.44 , 37.7  , 16.57 , 15.94 , 7.77  , float("inf")     , 5.75  , 10.64 ],
        #     [ 24.11 , 13.5  , 8.51  , 15.34 , 40.13 , 34.76 , 19.35 , 28.28 , 27.24 , 10.8  , 26.07 , 6.67  , 19.08 , 13.06 , 9.45  , 5.75  , float("inf")     , 8.49  ],
        #     [ 23.54 , 18.4  , 1.12  , 26.08 , 26.01 , 30.03 , 24.02 , 26.02 , 14.79 , 20.63 , 25.23 , 13.57 , 19.81 , 8.33  , 1.52  , 10.64 , 8.49  , float("inf")     ]
        # ]

        # def do_pre_job(delay_matrix):
        #     pass
        
        # def calc_delay(delay_matrix):
        #     node_num = len(delay_matrix)
        #     delay_result = [[0 for _ in range(node_num)] for __ in range(node_num)]
        #     path_result = []
        #     for i in range(node_num):
        #         distance = delay_matrix[i][:]
        #         path = [None for _ in range(node_num)]
        #         while min(distance) != float("inf"):
        #             distance_min = min(distance)
        #             j = distance.index(distance_min)
        #             if distance[j] == delay_matrix[i][j]:
        #                 path[j] = i
        #             delay_result[i][j] = distance[j]
        #             distance[j] = float("inf")
        #             for k in range(node_num):
        #                 if distance[k] != float("inf") and distance_min + delay_matrix[j][k] < distance[k]:
        #                     distance[k] = distance_min + delay_matrix[j][k]
        #                     path[k] = j
        #         path_result.append(path)
        #     return delay_result, path_result      
        
        # Bdelay, _ = calc_delay(Bdelay)
        Breward = 12.5 # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light" # Full/Light to specify the way of modelling transactions
        Tn= 10 # The rate of the number of transactions to be created per second
        Tdelay = 5.1 # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tfee = 0.000062 # The average transaction fee
        Tsize = 0.000546 # The average transaction size  in MB

        ''' Node Parameters '''
        Nn = 1000 # the total number of nodes in the network
        NODES = []

        ''' Network Parameters'''
        BoardcastType = "DBDC" # Gossip / DBDC

        ''' Simulation Parameters '''
        simTime= 10000 # the simulation length (in seconds)
        Runs=1 # Number of simulation runs
