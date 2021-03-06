from graphviz import Digraph

G = Digraph(format="png")
G.attr("node", shape="square", style="filled")
G.edge("start","listening",label="")
G.edge("listening","restore\n Process",label="(1)")
G.edge("listening","Getting \nthe corrected \ndata", label="(2)")
G.edge("Getting \nthe corrected \ndata","restore\n Process",label="(3)")
G.edge("Getting \nthe corrected \ndata","listening" ,label="(4)")
G.edge("restore\n Process","listening",label="(5)")
G.node("start", shape="circle", color="pink")
G.render("graphs")
