import matplotlib.pyplot as plt
import networkx as nx
import pygraphviz
from Route_Planner import Route_Planner
class Route_Painter(Route_Planner):
    def __init__(self,file_path,ins=False):
        super().__init__(file_path,ins)
        self.G=nx.DiGraph()
        self.edges=[]
        self.pos=None
        self.node_color_map=[]
        self.edge_color_map=[]
        self.red_node_num=0
        self.source=None
        self.destination=None
        self.shortest_path=None
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

    def onClick(self,event):
        (x,y)   = (event.xdata, event.ydata)
        clicked_node=None
        for index,i in enumerate(self.G.nodes):          
            node = self.pos[i]
            distance = pow(x-node[0],2)+pow(y-node[1],2)
            if distance < 20:
                clicked_node=i
                self.shortest_path=None
                if(self.node_color_map[index]=='red'):
                    if(self.destination==clicked_node):
                        self.destination=None
                    else:
                        self.source=None
                    self.red_node_num-=1
                    self.node_color_map[index]='green'
                elif(self.red_node_num<2):
                    if(self.red_node_num==0):
                        self.source=i
                    else:
                        self.destination=i
                        self.Dijkstra(self.source)
                        self.get_command(self.destination,file_name='graphviz_command.txt')
                        self.shortest_path=self.get_shortest_path(self.destination)

                    self.red_node_num+=1
                    self.node_color_map[index]='red'
                print('Node ',i,'is clicked')
                self.change_path_color(self.shortest_path)
                self.draw()
                break
    def add_edges(self):
        '''
        layout type: neato dot fdp sfdp twopi circo
        '''
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if(self.map[i][j]!=None):
                    #self.edges.append((i,j))
                    self.G.add_edge(i,j,color='black',weight=self.map[i][j])
        #self.G.add_edges_from(self.edges)
        self.pos=nx.nx_agraph.graphviz_layout(self.G,prog="neato")
        self.node_color_map=['green']*len(self.G.nodes)
        self.edge_color_map=['black']*len(self.G.edges)
        self.draw()
    def change_path_color(self,path=None):
        self.edge_color_map=['black']*len(self.G.edges)
        if(path==None):
            print('can not reach')
            return
        for index in range(len(path.split(' '))-1):
            edge=(int(path.split(' ')[index]),int(path.split(' ')[index+1]))
            self.edge_color_map[list(self.G.edges).index(edge)]='red'
        pass
    def draw(self):
        plt.clf()
        nx.draw(self.G,node_color=self.node_color_map,edge_color=self.edge_color_map,with_labels=True ,pos=self.pos,connectionstyle='arc3, rad = 0.1')
        nx.draw_networkx_edge_labels(self.G,pos=self.pos,edge_labels=nx.get_edge_attributes(self.G,'weight'))
        plt.text(130, -80, 'source node '+str(self.source), ha='left', wrap=True,fontsize=12)
        plt.text(130, -90, 'destination node '+str(self.destination), ha='left', wrap=True,fontsize=12)
        plt.text(130, -100, 'shortest paht  '+str(self.shortest_path), ha='left', wrap=True,fontsize=12)
        plt.show()
    
if __name__ == "__main__":  
    Painter=Route_Painter('map.xlsx',ins=True)
    Painter.add_edges()

