import networkx as nx
import matplotlib.pyplot as plt

def visualiser_ptvft(noeuds, tournees):
    G = nx.DiGraph()

    # 1. Ajout des noeuds au graphe
    for n_id, data in noeuds.items():
        G.add_node(n_id, pos=data['pos'], type=data['type'], tw=data.get('tw', (0,0)))

    # 2. Configuration des positions et des couleurs
    pos = nx.get_node_attributes(G, 'pos')
    
    # Séparer le dépôt des clients pour l'affichage
    depots = [n for n, d in G.nodes(data=True) if d['type'] == 'depot']
    clients = [n for n, d in G.nodes(data=True) if d['type'] == 'client']

    plt.figure(figsize=(10, 8))

 # Dessiner les noeuds (remplacement de 'marker' par 'node_shape')
    nx.draw_networkx_nodes(G, pos, nodelist=depots, node_color='red', node_size=500, node_shape='s', label='Dépôt')
    nx.draw_networkx_nodes(G, pos, nodelist=clients, node_color='lightblue', node_size=300, node_shape='o', label='Clients')

    # Ajouter les labels (ID du noeud + Fenêtre de temps)
    labels = {n: f"{n}\n[{G.nodes[n]['tw'][0]}-{G.nodes[n]['tw'][1]}]" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    # 3. Ajout et tracé des arêtes (les tournées)
    couleurs_tournees = ['blue', 'green', 'purple', 'orange', 'cyan']
    
    for i, tournee in enumerate(tournees):
        couleur = couleurs_tournees[i % len(couleurs_tournees)]
        
        # Créer les paires d'arêtes pour la tournée (ex: [0, 1, 3, 0] -> (0,1), (1,3), (3,0))
        aretes = [(tournee[j], tournee[j+1]) for j in range(len(tournee)-1)]
        G.add_edges_from(aretes)
        
        # Dessiner les arêtes spécifiques à cette tournée
        nx.draw_networkx_edges(
            G, pos, edgelist=aretes, 
            edge_color=couleur, 
            arrows=True, 
            arrowstyle='-|>', 
            arrowsize=15, 
            width=2,
            label=f'Véhicule {i+1}'
        )

    # 4. Finalisation de l'affichage
    plt.title("Visualisation des tournées (PTVFT)")
    plt.legend(scatterpoints=1)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axis('equal') # Pour ne pas déformer les coordonnées
    plt.show()

# ==========================================
# EXEMPLE D'UTILISATION
# ==========================================
if __name__ == "__main__":
    # Données factices : ID -> position (x,y), type, fenêtre de temps (début, fin)
    mes_noeuds = {
        0: {'pos': (50, 50), 'type': 'depot',  'tw': (0, 200)},
        1: {'pos': (20, 30), 'type': 'client', 'tw': (10, 40)},
        2: {'pos': (80, 40), 'type': 'client', 'tw': (50, 90)},
        3: {'pos': (60, 80), 'type': 'client', 'tw': (100, 150)},
        4: {'pos': (30, 70), 'type': 'client', 'tw': (120, 180)},
        5: {'pos': (10, 60), 'type': 'client', 'tw': (15, 60)}
    }

    # Deux véhicules partent du dépôt (0), visitent des clients, et reviennent.
    mes_tournees = [
        [0, 1, 5, 4, 0], # Tournée du Véhicule 1
        [0, 2, 3, 0]     # Tournée du Véhicule 2
    ]

    visualiser_ptvft(mes_noeuds, mes_tournees)