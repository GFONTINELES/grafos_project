import tkinter as tk
import tkinter.messagebox as messagebox
import networkx as nx
import matplotlib.pyplot as plt


class GraphApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Aplicativo de Grafos")

        self.num_vertices = tk.StringVar()
        self.num_arestas = tk.StringVar()
        self.edge_inputs = []

        self.create_initial_window()

    def create_initial_window(self):
        label_vertices = tk.Label(self.window, text="Número de Vértices:")
        label_vertices.pack()
        entry_vertices = tk.Entry(self.window, textvariable=self.num_vertices)
        entry_vertices.pack()

        label_arestas = tk.Label(self.window, text="Número de Arestas:")
        label_arestas.pack()
        entry_arestas = tk.Entry(self.window, textvariable=self.num_arestas)
        entry_arestas.pack()

        submit_button = tk.Button(self.window, text="Submit", command=self.submit_graph_info)
        submit_button.pack()

    def submit_graph_info(self):
        self.create_edge_inputs()

        submit_button = tk.Button(self.window, text="Submit", command=self.process_kruskal)
        submit_button.pack()

    def create_edge_inputs(self):
        num_arestas = int(self.num_arestas.get())
        for i in range(num_arestas):
            frame = tk.Frame(self.window)
            frame.pack()

            label_v1 = tk.Label(frame, text=f"Aresta {i + 1}, V1:")
            label_v1.pack(side=tk.LEFT)
            entry_v1 = tk.Entry(frame)
            entry_v1.pack(side=tk.LEFT)

            label_v2 = tk.Label(frame, text="V2:")
            label_v2.pack(side=tk.LEFT)
            entry_v2 = tk.Entry(frame)
            entry_v2.pack(side=tk.LEFT)

            label_peso = tk.Label(frame, text="Peso:")
            label_peso.pack(side=tk.LEFT)
            entry_peso = tk.Entry(frame)
            entry_peso.pack(side=tk.LEFT)

            self.edge_inputs.append((entry_v1, entry_v2, entry_peso))

    def process_kruskal(self):
        num_vertices = int(self.num_vertices.get())
        edges = []

        for edge_input in self.edge_inputs:
            v1 = int(edge_input[0].get())
            v2 = int(edge_input[1].get())

           
            if 0 <= v1 < num_vertices and 0 <= v2 < num_vertices:
                peso = float(edge_input[2].get())
                edges.append((v1, v2, peso))
            else:
                messagebox.showerror("Erro", "Vértices inválidos! Certifique-se de que estão na faixa válida.")

        mst = self.kruskal(num_vertices, edges)

        self.display_graph(edges, mst)

    def kruskal(self, num_vertices, edges):
        parent = [i for i in range(num_vertices)]
        rank = [0] * num_vertices
        mst = []

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1

        edges.sort(key=lambda x: x[2])

        for edge in edges:
            v1, v2, peso = edge
            if find(v1) != find(v2):
                union(v1, v2)
                mst.append(edge)

        return mst

    def display_graph(self, all_edges, mst):
        G = nx.Graph()
        for edge in all_edges:
            v1, v2, peso = edge
            G.add_edge(v1, v2, weight=peso)

        pos = nx.spring_layout(G)

        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=all_edges)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

        # arestas da árvore geradora mínima em destaque
        red_edges = [(v1, v2) for v1, v2, _ in mst]
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', width=2.0)

        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    app = GraphApp()
    app.window.mainloop()
