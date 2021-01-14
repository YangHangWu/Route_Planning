import pandas as pd
pd.set_option("display.max_columns",500)
class Route_Planner:
    def __init__(self,file_path,ins=False):
        pd.set_option('mode.chained_assignment', None)
        self.modify=True
        self.file_path=None
        self.map=None
        self.direction=None
        self.table_df=None
        self.file_path=file_path
        self.ins=ins
        self.read_map()

    def read_map(self):
        df = pd.read_excel(self.file_path,sheet_name=0)
        df=df.loc[:, ~df.columns.str.contains('^Unnamed',na=False)].where(pd.notnull(df), None)
        df=df[:len(df.columns)]
        print('map:')
        print(df)
        self.map=df.values.tolist()
        print('')
        if(self.ins):
            df = pd.read_excel(self.file_path,sheet_name=1)
            df=df.loc[:, ~df.columns.str.contains('^Unnamed',na=False)].where(pd.notnull(df), None)
            df=df[:len(df.columns)]
            print('direction:')
            print(df)
            self.direction=df.values.tolist()
    
    def create_table_df(self):
        table=[[None,False,None,''] for j in range(len(self.map))]
        self.table_df=pd.DataFrame.from_records(table)
        self.table_df.columns=['Distance','Visited','Path','Instruction']

    def update_table_df(self):
        min_dis=None
        pending_node=None
        for node,dis in enumerate(self.table_df['Distance']):
            if (dis!=None and self.table_df['Visited'][node]==False):
                if(min_dis==None or min_dis>dis):
                    min_dis=dis
                    pending_node=node

        self.table_df['Visited'][pending_node]=True
        #print(self.table_df)
        #self.table_df['Instruction'][pending_node]=self.table_df['Instruction'][pending_node]+' 0'
        return pending_node

    def Dijkstra(self,source):
        if(source==None or source>=len(self.map)):
            print('out of the map')
            fp = open("command.txt", "w")
            fp.write('-1')
            fp.close()
            return
        self.create_table_df()
        self.table_df['Distance'][source]=0
        self.table_df['Visited'][source]=True
        self.table_df['Path'][source]=str(source)
        #self.table_df['Instruction'][source]=0
        index=0
        while(index<len(self.map)):
            #print(self.table_df)
            index+=1
            for node, edge in enumerate(self.map[source]):
                ##update table
                if (edge !=None and (self.table_df['Distance'][node]==None or self.table_df['Distance'][node]>self.table_df['Distance'][source]+edge)):
                    #print(node, edge)
                    self.table_df['Distance'][node]=self.table_df['Distance'][source]+edge
                    self.table_df['Path'][node]=str(self.table_df['Path'][source])+' '+str(node)
                    #self.table_df['Instruction'][node]=str(self.table_df['Instruction'][source])+' '+(str(self.direction[source][node]))
                    if(self.ins):
                        self.table_df['Instruction'][node]=str(self.table_df['Instruction'][source])+' '+(str(self.direction[source][node])).split('.')[0]
            ##check visited and find next source
            source=self.update_table_df()
            if source==None:
                break
        print('')
        print('Single-Source Shortest Path')
        print(self.table_df)
        self.table_df.to_excel("path.xlsx") 
    def get_shortest_path(self,destination):
            print(self.table_df['Path'][destination])
            return self.table_df['Path'][destination]
    def get_command(self,destination,file_name='command.txt'):
        if(not self.ins):
            print('no instruction')
            return
        else:
            if(destination>=len(self.map)):
                print('out of the map')
                fp = open(file_name, "w")
                fp.write('-1')
                fp.close()
                return
            if(self.table_df['Visited'][destination]==True):
                path_list=list(self.table_df['Path'][destination].split(' '))
                for index,node_num in enumerate(path_list):
                    if(len(node_num)<2):
                        path_list[index]='0'+path_list[index]
                ins_list=list(self.table_df['Instruction'][destination].split(' ')[1:]).copy()
                ins_list=ins_list+['0']
                data={ 
                    'Path':path_list,
                    'Instruction': ins_list
                }
                df = pd.DataFrame(data).sort_values(by=['Path'])
                sorted_path=list(df['Path'])
                sorted_ins=list(df['Instruction'])
                command=''
                for index in range(len(sorted_path)):
                    command=command+sorted_path[index]+','+sorted_ins[index]+';'
                print('command ',command)
                fp = open(file_name, "w")
                fp.write(command)
                fp.close()
            else:
                print('can not reach')
                fp = open(file_name, "w")
                fp.write('-1')
                fp.close()


if __name__ == "__main__":   
    Planner=Route_Planner('map.xlsx',ins=True)
    source=None
    destination=None
    while True:
        f = open('source.txt')
        text=f.readline()
        try:
            int(text.split(';')[1])
        except:
            continue
        if(source != int(text.split(';')[0])):
            source=int(text.split(';')[0])
            destination=int(text.split(';')[1])
            Planner.Dijkstra(source)
            Planner.get_command(destination=destination)
            #Planner.get_shortest_path(destination=destination)
        elif(destination!=int(text.split(';')[1])):
            destination=int(text.split(';')[1])
            Planner.get_command(destination=destination)
        else:
            pass
        