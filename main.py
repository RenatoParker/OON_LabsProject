from components import Network
from components import Node
from pathlib import Path
import matplotlib.pyplot as plt

import json

if __name__ == '__main__':
    root = Path(__file__).parent

    with open("Resource/279186/full_network.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            # il transceiver non è specificato nei file; in teoria c'è un default nel costruttore del nodo
            nodeData["transceiver"] = "flex_rate"
            new_node = Node.Node(nodeData)
            nodes_full[nodeKey] = new_node

    with open("Resource/279186/not_full_network.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_not_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            new_node = Node.Node(nodeData)
            nodes_not_full[nodeKey] = new_node

    net = Network.Network(nodes_full)
    net.connect()
    net.draw()
    net.initRouteSpace()
    net.computeWeightedPaths()
    fullTopologyStats = net.returnTopologyStats()
    print(fullTopologyStats)

    net_not_full = Network.Network(nodes_not_full)
    net_not_full.connect()
    net_not_full.initRouteSpace()
    net_not_full.computeWeightedPaths()
    notFullTopologyStats = net_not_full.returnTopologyStats()
    print(notFullTopologyStats)

    # todo confronta in vari transceiver
    for fom in ["latency", "snr"]:
        simulationResultsFull = []
        simulationResultsNotFull = []
        emme = range(1, 100)
        for m in emme:
            traffic_matrix = []
            for indexRow, valueRow in enumerate(nodes_not_full):
                row = []
                for indexCol, valueCol in enumerate(nodes_not_full):
                    if indexRow == indexCol:
                        row.append(0)
                    else:
                        row.append(100 * 5)
                traffic_matrix.append(row)
            simulationResultsFull.append(net.createAndManageConnections(traffic_matrix, fom))
            simulationResultsNotFull.append(net_not_full.createAndManageConnections(traffic_matrix, fom))

        for simulationResults in [simulationResultsFull, simulationResultsNotFull]:
            avgBitrateAllocated = 0
            avgAllocatedConnections = 0
            avgBlockingEvent = 0

            GSNRavgs = []
            bitrateAllocated = []
            allocatedConnections = []
            blockingEvent = []
            netIsSaturated = []
            perLinkBitRateAvg = []
            perLinkBitRateMin = []
            perLinkBitRateMax = []

            for res in simulationResults:
                print(res)
                avgBitrateAllocated += res["bitrateAllocated"]
                avgAllocatedConnections += res["allocatedConnections"]
                avgBlockingEvent += res["blockingEvent"]

                GSNRavgs.append(res["GSNRavg"])
                bitrateAllocated.append(res["bitrateAllocated"])
                allocatedConnections.append(res["allocatedConnections"])
                blockingEvent.append(res["blockingEvent"])
                netIsSaturated.append(res["netIsSaturated"])
                perLinkBitRateAvg.append(res["perLinkBitRateAvg"])
                perLinkBitRateMin.append(res["perLinkBitRateMin"])
                perLinkBitRateMax.append(res["perLinkBitRateMax"])

            avgBitrateAllocated /= len(simulationResults)
            avgAllocatedConnections /= len(simulationResults)
            avgBlockingEvent /= len(simulationResults)

            print("GSNRavgs:")
            print(GSNRavgs)

            print("avgBitrateAllocated")
            print(avgBitrateAllocated)

            print("avgAllocatedConnections")
            print(avgAllocatedConnections)

            print("avgBlockingEvent")
            print(avgBlockingEvent)

            print("bitrateAllocated")
            print(bitrateAllocated)

            plt.hist(GSNRavgs, bins=20)
            plt.gca().set(title='GSNR average Histogram ' + fom , ylabel='Frequency')
            plt.show()

            plt.hist(bitrateAllocated, bins=50)
            plt.gca().set(title='bitrate Allocated Histogram ' + fom, ylabel='Frequency')
            plt.show()

            plt.hist(allocatedConnections, bins=50)
            plt.gca().set(title='allocated Connections  Histogram ' + fom, ylabel='Frequency')
            plt.show()

            plt.hist(blockingEvent, bins=50)
            plt.gca().set(title='blockingEvent average Histogram ' + fom, ylabel='Frequency')
            plt.show()

            plt.hist(perLinkBitRateAvg, bins=20)
            plt.gca().set(title='perLinkBitRate average  Histogram ' + fom, ylabel='Frequency')
            plt.show()

            plt.hist(perLinkBitRateMin, bins=20)
            plt.gca().set(title='perLinkBitRate min  Histogram ' + fom, ylabel='Frequency')
            plt.show()

            plt.hist(perLinkBitRateMax, bins=20)
            plt.gca().set(title='perLinkBitRate max  Histogram ' + fom, ylabel='Frequency')
            plt.show()



            # plt.bar(emme, bitrateAllocated)
            # plt.ylabel("Bitrate Allocated")
            # plt.show()
            # plt.bar(emme, allocatedConnections)
            # plt.ylabel("Allocated Connections")
            # plt.show()
            # plt.bar(emme, blockingEvent)
            # plt.ylabel("Blocking Events")
            # plt.show()
            # plt.bar(emme, GSNRavgs)
            # plt.ylabel("GSNR average")
            # plt.show()
            # plt.bar(emme, netIsSaturated)
            # plt.ylabel("netIsSaturated")
            # plt.show()

    # todo confronta in vari transceiver
    # for fom in ["latency", "snr"]:
    #     simulationResultsFull = []
    #     simulationResultsNotFull = []
    #     emme = range(1, 100)
    #     for m in emme:
    #         traffic_matrix = []
    #         for indexRow, valueRow in enumerate(nodes_not_full):
    #             row = []
    #             for indexCol, valueCol in enumerate(nodes_not_full):
    #                 if indexRow == indexCol:
    #                     row.append(0)
    #                 else:
    #                     row.append(100 * 10)
    #             traffic_matrix.append(row)
    #         simulationResultsFull.append(net.createAndManageConnections(traffic_matrix, fom))
    #         simulationResultsNotFull.append(net_not_full.createAndManageConnections(traffic_matrix, fom))
    #
    #     for simulationResults in [simulationResultsFull, simulationResultsNotFull]:
    #         avgBitrateAllocated = 0
    #         avgAllocatedConnections = 0
    #         avgBlockingEvent = 0
    #
    #         GSNRavgs = []
    #         bitrateAllocated = []
    #         allocatedConnections = []
    #         blockingEvent = []
    #         netIsSaturated = []
    #         perLinkBitRateAvg = []
    #         perLinkBitRateMin = []
    #         perLinkBitRateMax = []
    #
    #         for res in simulationResults:
    #             print(res)
    #             avgBitrateAllocated += res["bitrateAllocated"]
    #             avgAllocatedConnections += res["allocatedConnections"]
    #             avgBlockingEvent += res["blockingEvent"]
    #
    #             GSNRavgs.append(res["GSNRavg"])
    #             bitrateAllocated.append(res["bitrateAllocated"])
    #             allocatedConnections.append(res["allocatedConnections"])
    #             blockingEvent.append(res["blockingEvent"])
    #             netIsSaturated.append(res["netIsSaturated"])
    #             perLinkBitRateAvg.append(res["perLinkBitRateAvg"])
    #             perLinkBitRateMin.append(res["perLinkBitRateMin"])
    #             perLinkBitRateMax.append(res["perLinkBitRateMax"])
    #
    #         print(perLinkBitRateAvg)
    #         print(perLinkBitRateMin)
    #         print(perLinkBitRateMax)
    #
    #         plt.bar(emme, bitrateAllocated)
    #         plt.ylabel("Bitrate Allocated")
    #         plt.show()
    #         plt.bar(emme, allocatedConnections)
    #         plt.ylabel("Allocated Connections")
    #         plt.show()
    #         plt.bar(emme, blockingEvent)
    #         plt.ylabel("Blocking Events")
    #         plt.show()
    #         plt.bar(emme, GSNRavgs)
    #         plt.ylabel("GSNR average")
    #         plt.show()
    #         plt.bar(emme, netIsSaturated)
    #         plt.ylabel("netIsSaturated")
    #         plt.show()


