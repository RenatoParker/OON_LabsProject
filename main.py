import numpy as np

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
            # nodeData["transceiver"] = "flex_rate"
            new_node = Node.Node(nodeData)
            nodes_full[nodeKey] = new_node

    with open("Resource/279186/not_full_network.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_not_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            # nodeData["transceiver"] = "flex_rate"
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

    plt.bar(list(range(0, len(fullTopologyStats["latency"]))), fullTopologyStats["latency"], color='#b5ffb9', edgecolor='white')
    plt.xlabel("Link id")
    plt.ylabel("Latency")
    plt.savefig("./pic/latencyOnLinks", dpi=200.0)
    plt.show()
    plt.bar(list(range(0, len(fullTopologyStats["SNR"]))), fullTopologyStats["SNR"], color='#b5ffb9', edgecolor='white')
    plt.xlabel("Link id")
    plt.ylabel("SNR")
    plt.savefig("./pic/SNROnLinks", dpi=200.0)
    plt.show()

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
    #     for index, simulationResults in enumerate([simulationResultsFull, simulationResultsNotFull]):
    #         if index == 0:
    #             netType = "Full network"
    #         if index == 1:
    #             netType = "Not Full network"
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
    #         perLinkGSNRAvg = []
    #         perLinkGSNRMin = []
    #         perLinkGSNRMax = []
    #
    #         perLinkLatencyAvg = []
    #         perLinkLatencyMin = []
    #         perLinkLatencyMax = []
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
    #
    #             perLinkBitRateAvg.append(res["perLinkBitRateAvg"])
    #             perLinkBitRateMin.append(res["perLinkBitRateMin"])
    #             perLinkBitRateMax.append(res["perLinkBitRateMax"])
    #
    #             perLinkGSNRAvg.append(res["perLinkGSNRAvg"])
    #             perLinkGSNRMin.append(res["perLinkGSNRMin"])
    #             perLinkGSNRMax.append(res["perLinkGSNRMax"])
    #
    #             perLinkLatencyAvg.append(res["perLinkLatencyAvg"])
    #             perLinkLatencyMin.append(res["perLinkLatencyMin"])
    #             perLinkLatencyMax.append(res["perLinkLatencyRMax"])
    #
    #         avgBitrateAllocated /= len(simulationResults)
    #         avgAllocatedConnections /= len(simulationResults)
    #         avgBlockingEvent /= len(simulationResults)
    #
    #         print(" ====== Bitrate Allocated ====== ")
    #         print("Average: ", avgBitrateAllocated)
    #         print("Min: ", min(bitrateAllocated))
    #         print("Max: ", max(bitrateAllocated))
    #
    #         print(" ====== GSNR ======")
    #         print("Average: ", sum(GSNRavgs)/len(GSNRavgs))
    #         print("Min: ", min(GSNRavgs))
    #         print("Max: ", max(GSNRavgs))
    #
    #         print(" ====== Connection Allocated ======")
    #         print("Average: ", sum(allocatedConnections)/len(allocatedConnections))
    #         print("Min: ", min(allocatedConnections))
    #         print("Max: ", max(allocatedConnections))
    #
    #         print(" ====== Blocking Event ======")
    #         print("Average: ", sum(blockingEvent)/len(blockingEvent))
    #         print("Min: ", min(blockingEvent))
    #         print("Max: ", max(blockingEvent))
    #
    #         print(" ====== Link Capacity ======")
    #         print("Average: ", sum(perLinkBitRateAvg)/len(perLinkBitRateAvg))
    #         print("Min: ", min(perLinkBitRateAvg))
    #         print("Max: ", max(perLinkBitRateAvg))
    #
    #
    #         print(" ====== Link GSNR ======")
    #         print("Average: ", sum(perLinkGSNRAvg)/len(perLinkGSNRAvg))
    #         print("Min: ", min(perLinkGSNRAvg))
    #         print("Max: ", max(perLinkGSNRAvg))
    #
    #         print(" ====== Link Latency ======")
    #         print("Average: ", sum(perLinkLatencyAvg)/len(perLinkLatencyAvg))
    #         print("Min: ", min(perLinkLatencyAvg))
    #         print("Max: ", max(perLinkLatencyAvg))
    #
    #         plt.hist(GSNRavgs, bins=50)
    #         plt.gca().set(title='GSNR average Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/GSNR average Histogram ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #
    #         print("bit rate")
    #         print(bitrateAllocated)
    #         plt.hist(bitrateAllocated, bins=50)
    #         plt.gca().set(title='bitrate Allocated Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/bitrate Allocated Histogram ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(allocatedConnections, bins=50)
    #         plt.gca().set(title='allocated Connections  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/allocated Connections  Histogram  ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(blockingEvent, bins=50)
    #         plt.gca().set(title='blockingEvent average Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/blockingEvent average Histogram ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(perLinkBitRateAvg, bins=20)
    #         plt.gca().set(title='perLinkBitRate average  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkBitRate average  Histogram   ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(perLinkBitRateMin, bins=20)
    #         plt.gca().set(title='perLinkBitRate min  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkBitRate min  Histogram  ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(perLinkBitRateMax, bins=20)
    #         plt.gca().set(title='perLinkBitRate max  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkBitRate max  Histogram   ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #         print("as")
    #
    #         print(perLinkGSNRAvg)
    #
    #         plt.hist(perLinkGSNRAvg, bins=20)
    #         plt.gca().set(title='perLinkGSNRAvg average  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkGSNRAvg average  Histogram  ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(perLinkGSNRMin, bins=20)
    #         plt.gca().set(title='perLinkGSNRMin min  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkGSNRMin min  Histogram   ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #         plt.hist(perLinkGSNRMax, bins=20)
    #         plt.gca().set(title='perLinkGSNRMax max  Histogram ' + fom + ' ' + netType, ylabel='Frequency')
    #         plt.savefig('./pic/perLinkGSNRMax max  Histogram   ' + fom + ' ' + netType, dpi=200.0)
    #         plt.show()
    #
    #
    #         # plt.bar(emme, bitrateAllocated)
    #         # plt.ylabel("Bitrate Allocated")
    #         # plt.show()
    #         # plt.bar(emme, allocatedConnections)
    #         # plt.ylabel("Allocated Connections")
    #         # plt.show()
    #         # plt.bar(emme, blockingEvent)
    #         # plt.ylabel("Blocking Events")
    #         # plt.show()
    #         # plt.bar(emme, GSNRavgs)
    #         # plt.ylabel("GSNR average")
    #         # plt.show()
    #         # plt.bar(emme, netIsSaturated)
    #         # plt.ylabel("netIsSaturated")
    #         # plt.show()

    # todo confronta in vari transceiver
    for fom in ["latency", "snr"]:
        simulationResultsFull = []
        simulationResultsNotFull = []
        emme = range(1, 50)
        for m in emme:
            traffic_matrix = []
            for indexRow, valueRow in enumerate(nodes_not_full):
                row = []
                for indexCol, valueCol in enumerate(nodes_not_full):
                    if indexRow == indexCol:
                        row.append(0)
                    else:
                        row.append(100 * m)
                traffic_matrix.append(row)
            simulationResultsFull.append(net.createAndManageConnections(traffic_matrix, fom))
            simulationResultsNotFull.append(net_not_full.createAndManageConnections(traffic_matrix, fom))
            print("qqq")
            print(simulationResultsFull)

        for index, simulationResults in enumerate([simulationResultsFull, simulationResultsNotFull]):
            print("qua")
            print(len(simulationResults))
            print(index)
            if index == 0:
                print("FULL")
                netType = "Full network"
            if index == 1:
                netType = "Not Full network"
            print(netType)
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

            perLinkGSNRAvg = []
            perLinkGSNRMin = []
            perLinkGSNRMax = []

            perLinkLatencyAvg = []
            perLinkLatencyMin = []
            perLinkLatencyMax = []

            for res in simulationResults:
                print(res)
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

                perLinkGSNRAvg.append(res["perLinkGSNRAvg"])
                perLinkGSNRMin.append(res["perLinkGSNRMin"])
                perLinkGSNRMax.append(res["perLinkGSNRMax"])

                perLinkLatencyAvg.append(res["perLinkLatencyAvg"])
                perLinkLatencyMin.append(res["perLinkLatencyMin"])
                perLinkLatencyMax.append(res["perLinkLatencyRMax"])

            avgBitrateAllocated /= len(simulationResults)
            avgAllocatedConnections /= len(simulationResults)
            avgBlockingEvent /= len(simulationResults)

            print(" ====== Bitrate Allocated ====== ")
            print("Average: ", avgBitrateAllocated)
            print("Min: ", min(bitrateAllocated))
            print("Max: ", max(bitrateAllocated))

            print(" ====== GSNR ======")
            print("Average: ", sum(GSNRavgs)/len(GSNRavgs))
            print("Min: ", min(GSNRavgs))
            print("Max: ", max(GSNRavgs))

            print(" ====== Connection Allocated ======")
            print("Average: ", sum(allocatedConnections)/len(allocatedConnections))
            print("Min: ", min(allocatedConnections))
            print("Max: ", max(allocatedConnections))

            print(" ====== Blocking Event ======")
            print("Average: ", sum(blockingEvent)/len(blockingEvent))
            print("Min: ", min(blockingEvent))
            print("Max: ", max(blockingEvent))

            print(" ====== Link Capacity ======")
            print("Average: ", sum(perLinkBitRateAvg)/len(perLinkBitRateAvg))
            print("Min: ", min(perLinkBitRateAvg))
            print("Max: ", max(perLinkBitRateAvg))


            print(" ====== Link GSNR ======")
            print("Average: ", sum(perLinkGSNRAvg)/len(perLinkGSNRAvg))
            print("Min: ", min(perLinkGSNRAvg))
            print("Max: ", max(perLinkGSNRAvg))

            print(" ====== Link Latency ======")
            print("Average: ", sum(perLinkLatencyAvg)/len(perLinkLatencyAvg))
            print("Min: ", min(perLinkLatencyAvg))
            print("Max: ", max(perLinkLatencyAvg))


            plt.bar(emme, bitrateAllocated)
            plt.gca().set(title='Bitrate Allocated ' + fom + ' ' + netType, ylabel='Bitrate Allocated')
            plt.savefig('./pic/Bitrate Allocated ' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, allocatedConnections)
            plt.gca().set(title='Allocated Connections ' + fom + ' ' + netType, ylabel='Allocated Connections')
            plt.savefig('./pic/Allocated Connections' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, blockingEvent)
            plt.gca().set(title='Blocking Events ' + fom + ' ' + netType, ylabel='Blocking Events')
            plt.savefig('./pic/Blocking Events' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, netIsSaturated)
            plt.gca().set(title='netIsSaturate ' + fom + ' ' + netType, ylabel='netIsSaturate')
            plt.savefig('./pic/netIsSaturate' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, GSNRavgs)
            plt.gca().set(title='GSNR average ' + fom + ' ' + netType, ylabel='GSNR average')
            plt.savefig('./pic/GSNR average' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkBitRateAvg)
            plt.gca().set(title='per Link BitRate Avg ' + fom + ' ' + netType, ylabel='per Link BitRate ')
            plt.savefig('./pic/per Link BitRate ' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkBitRateMax)
            plt.gca().set(title='per Link BitRate Max ' + fom + ' ' + netType, ylabel='per Link BitRate Max')
            plt.savefig('./pic/per Link BitRate Max' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkBitRateMin)
            plt.gca().set(title='per Link BitRate Min ' + fom + ' ' + netType, ylabel='per Link BitRate Min')
            plt.savefig('./pic/per Link BitRate Min' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkLatencyAvg)
            plt.gca().set(title='per Link Latency ' + fom + ' ' + netType, ylabel='per Link Latency ')
            plt.savefig('./pic/per Link Latency ' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkLatencyMin)
            plt.gca().set(title='per Link Latency Min' + fom + ' ' + netType, ylabel='per Link Latency Min')
            plt.savefig('./pic/per Link Latency Min' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkLatencyMax)
            plt.gca().set(title='per Link Latency Max' + fom + ' ' + netType, ylabel='per Link Latency Max')
            plt.savefig('./pic/per Link Latency Max' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkGSNRAvg)
            plt.gca().set(title='per Link GSNR ' + fom + ' ' + netType, ylabel='per Link GSNR ')
            plt.savefig('./pic/per Link GSNR ' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkGSNRMin)
            plt.gca().set(title='per Link GSNR Min' + fom + ' ' + netType, ylabel='per Link GSNR Min')
            plt.savefig('./pic/per Link GSNR Min' + fom + ' ' + netType, dpi=200.0)
            plt.show()

            plt.bar(emme, perLinkGSNRMax)
            plt.gca().set(title='per Link GSNR Max' + fom + ' ' + netType, ylabel='per Link GSNR Max')
            plt.savefig('./pic/per Link GSNR Max' + fom + ' ' + netType, dpi=200.0)
            plt.show()








