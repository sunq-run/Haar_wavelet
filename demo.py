#!/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx
import sys,random

args = sys.argv

G = nx.DiGraph()
# make grahp
print args
if len(args) == 1:
    G.add_node(0, data=23)
    G.add_node(1, data=8)
    G.add_node(2, data=2)
    G.add_node(3, data=10)
    G.add_node(4, data=11)
    G.add_node(5, data=67)
    G.add_node(6, data=22)
    G.add_node(7, data=43)
elif args[1] == "-r":
    G.add_node(0, data=random.randint(1,100))
    G.add_node(1, data=random.randint(1,100))
    G.add_node(2, data=random.randint(1,100))
    G.add_node(3, data=random.randint(1,100))
    G.add_node(4, data=random.randint(1,100))
    G.add_node(5, data=random.randint(1,100))
    G.add_node(6, data=random.randint(1,100))
    G.add_node(7, data=random.randint(1,100))
else:
    print "invalid Options"

G.add_node(8, data=[])
G.add_node(9, data=[])
G.add_node(10, data=[])
G.add_node(11, data=[])
G.add_node(12, data=[])
G.add_node(13, data=[])
G.add_node(14, data=[])

G.add_edges_from([(0, 8),
                  (1, 8),
                  (2, 9),
                  (3, 9),
                  (4, 10),
                  (5, 10),
                  (6, 11),
                  (7, 11),
                  (8, 12),
                  (9, 12),
                  (10, 13),
                  (11, 13),
                  (12, 14),
                  (13, 14)
                  ]
                )

#set value edge server
#for i in len(G.nodes()):
    
#matplot posision
pos = { 0 : (0, 80),
        1 : (0, 70),
        2 : (0, 60),
        3 : (0, 50),
        4 : (0, 40),
        5 : (0, 30),
        6 : (0, 20),
        7 : (0, 10),
        8 : (10, 75),
        9 : (10, 55),
        10 : (10, 35),
        11 : (10, 15),
        12 : (20, 65),
        13 : (20, 25),
        14 : (30, 45)
        } 

def getdata(name):
    return str(G.nodes(data=True)[name][1]['data'])

def display():
    #reset graph
    plt.figure()
    #draw graph
    nx.draw_networkx(G, pos=pos)
    #draw text
    plt.text(-4,80,getdata(0),fontsize=12)
    plt.text(-4,70,getdata(1),fontsize=12)
    plt.text(-4,60,getdata(2),fontsize=12)
    plt.text(-4,50,getdata(3),fontsize=12)
    plt.text(-4,40,getdata(4),fontsize=12)
    plt.text(-4,30,getdata(5),fontsize=12)
    plt.text(-4,20,getdata(6),fontsize=12)
    plt.text(-4,10,getdata(7),fontsize=12)
    plt.text(10,70,getdata(8),fontsize=12)
    plt.text(10,50,getdata(9),fontsize=12)
    plt.text(10,30,getdata(10),fontsize=12)
    plt.text(10,10,getdata(11),fontsize=12)
    plt.text(20,60,getdata(12),fontsize=12)
    plt.text(20,20,getdata(13),fontsize=12)
    plt.text(30,45,getdata(14),fontsize=12)
    #How display time per one frame?
    plt.pause(4)

def support_server(a,b):
    for support in range(a,b):
        X = G.nodes(data=True)[support][1]['data'][0]
        Y = G.nodes(data=True)[support][1]['data'][1]
        print "[LOG] Sending data at server" + str(support) + " " + str(X) + "+" + str(Y)
        send_data = int(X) + int(Y)
        save_data = int(X) - int(Y)
        #save
        del G.nodes(data=True)[support][1]['data'][0:]
        G.nodes(data=True)[support][1]['data'].append(save_data)
        #send
        parentis = G.succ[support].keys()[0]
        G.nodes(data=True)[parentis][1]['data'].append(send_data)

def sending_edge():
    for i in range(8):
        parentis = G.succ[i].keys()[0]
        G.nodes(data=True)[parentis][1]['data'].append(getdata(i))

def sending_data_process():
    print "[LOG] Start send Processing"
    for clock in range(6):
        if clock == 1:
            display()
        if clock == 2:
            sending_edge()
            display()
        if clock == 3:
            support_server(8,12)
            display()
        if clock == 4:
            support_server(12,14)
            display()

def server_restore(server):
    server_data = G.nodes(data=True)[server][1]['data']
    children = G.pred[server].keys()
    if server_data[0] > server_data[1]:
        print "send sum! children[0]"
        G.nodes(data=True)[children[0]][1]['data'].append(["R",server_data[0]])
    elif server_data[0] < server_data[1]:
        print "send sum! children[1]"
        G.nodes(data=True)[children[1]][1]['data'].append(["R",server_data[1]])
    else :
        print "ignore"

def support_restore(a,b,edge):
    #a,bはその階層の範囲　edgeは、edgeserverの次のノードかどうか
    #support server [13,["R",143]] when restore from server
    for support in range(a,b):
        children = G.pred[support].keys()
        print "[LOG]children is " + str(children)
        support_data = G.nodes(data=True)[support][1]['data']
        print support_data
        if len(support_data) == 2 and support_data[1][0] == "R":
           #X = <support diffrence + server sum data /2>
           print "[LOG] (X + Y)/2 ::::" + "(" + str(support_data[1][1]) + "+" + str(support_data[0]) + ")/2"
           X = (support_data[1][1] + support_data[0])/2
           print "[LOG] (X + Y)/2 ::::" + "(" + str(support_data[1][1]) + "-" + str(support_data[0]) + ")/2"
           Y = (support_data[1][1] - support_data[0])/2
           print "[LOG] support data X = " + str(X) + " Y = " + str(Y)
           if edge:
                print "GET!! two Edge Node Value X = " + str(X) + " Y = " + str(Y)
                break
           if X > Y:
               print "send sum! X"
               G.nodes(data=True)[children[0]][1]['data'].append(["R",X])
           elif X < Y:
               print "send sum! Y"
               G.nodes(data=True)[children[1]][1]['data'].append(["R",Y])
           else:
               print "ignore"
        else:
            print "Nothing Recive data from server"
            
            
def restore_data_process():
    print "[LOG] Start restore Processing"
    for clock in range(6):
        if clock == 1:
            display()
        if clock == 2:
            server_restore(G.nodes()[-1])
            display()
        if clock == 3:
            support_restore(12,14,edge=False)
            display()
        if clock == 4:
            support_restore(8,12,edge=True)
            display()

sending_data_process()
restore_data_process()

