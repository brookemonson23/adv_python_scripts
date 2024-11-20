import requests
import json
import os
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
 
# Dictionary of cryptocurrency names and their ticker symbols
coins = {
    'ripple': 'xrp',
    'cardano': 'ada',
    'bitcoin-cash': 'bch',
    'eos': 'eos',
    'litecoin': 'ltc',
    'ethereum': 'eth',
    'bitcoin': 'btc'
}
 
def fetch_coin_prices(coins):
    """
    Fetch cryptocurrency exchange rates from CoinGecko API.
    
    Args:
        coins (dict): Dictionary of cryptocurrency names and tickers
    
    Returns:
        dict: API response containing exchange rates
    """
    # Construct URL by joining coin names and tickers
    names_url = ','.join(coins.keys())
    ticker_url = ','.join(coins.values())
 
    # Construct full API URL for price retrieval
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={names_url}&vs_currencies={ticker_url}'
    
    # Make API request and parse JSON response
    response = requests.get(url)
    data = response.json()
    
    # Save JSON data to local file for reference
    curr_dir = os.path.dirname(__file__)
    file_name = os.path.join(curr_dir, 'exchange_rates.json')
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    return data
 
def create_crypto_graph(data, coins):
    """
    Create a directed graph representing cryptocurrency exchange rates.
    
    Args:
        data (dict): Exchange rate data from CoinGecko
        coins (dict): Dictionary of cryptocurrency names and tickers
    
    Returns:
        networkx.DiGraph: Graph with nodes as crypto tickers and edges as exchange rates
    """
    # Initialize list to store graph edges
    edges = []
    
    # Iterate through each coin to create graph edges
    for coin in coins:
        one_coin_dict = data[coin]
        for tkr in one_coin_dict:
            # Extract node information and exchange rate
            node_from = coins[coin]
            node_to = tkr
            directed_edge_weight = one_coin_dict[tkr]
            edges.append((node_from, node_to, directed_edge_weight))
    
    # Create directed graph and add weighted edges
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)
    
    return g
 
def visualize_graph(graph):
    """
    Create and save a visualization of the cryptocurrency graph.
    
    Args:
        graph (networkx.DiGraph): Graph to visualize
    """
    # Determine current directory for saving visualization
    curr_dir = os.path.dirname(__file__)
    graph_visual_fil = os.path.join(curr_dir, "graph_visual.png")
    
    # Create circular layout for graph visualization
    pos = nx.circular_layout(graph)
    plt.figure(figsize=(10, 10))
    
    # Draw nodes and edges
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', 
                     node_size=500, font_size=10, font_weight='bold')
    
    # Add edge weight labels
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    
    # Save the graph visualization
    plt.tight_layout()
    plt.savefig(graph_visual_fil)
    plt.close()
 
def find_arbitrage_opportunities(graph):
    """
    Find potential arbitrage opportunities by calculating path weights.
    
    Args:
        graph (networkx.DiGraph): Cryptocurrency exchange rate graph
    
    Returns:
        tuple: Smallest and highest arbitrage path factors
    """
    # Initialize variables to track  opportunities
    highest_factor = 0
    smallest_factor = float('inf')
    smallest_paths = []
    highest_path = []
    
    # Iterate through all possible node pairs
    for n1, n2 in permutations(graph.nodes, 2):
        # Find all paths between two nodes
        for path in nx.all_simple_paths(graph, source=n1, target=n2):
            # Calculate forward path weight
            forward_path_weight = 1
            for i in range(len(path)-1):
                forward_path_weight *= graph[path[i]][path[i+1]]['weight']
            
            # Find reverse paths
            for path_back in nx.all_simple_paths(graph, source=n2, target=n1):
                # Calculate backward path weight
                backward_path_weight = 1
                for j in range(len(path_back)-1):
                    backward_path_weight *= graph[path_back[j]][path_back[j+1]]['weight']
                
                # Calculate path weights factor
                path_weights_factor = forward_path_weight * backward_path_weight
                
                # Update smallest arbitrage opportunity
                if path_weights_factor < smallest_factor:
                    smallest_factor = path_weights_factor
                    smallest_paths = path + path_back
                
                # Update highest arbitrage opportunity
                if path_weights_factor > highest_factor:
                    highest_factor = path_weights_factor
                    highest_path = path + path_back
    
    return smallest_factor, smallest_paths, highest_factor, highest_path
 
def main():
    """
    Main function to orchestrate cryptocurrency arbitrage analysis.
    """
    # Fetch cryptocurrency exchange rates
    data = fetch_coin_prices(coins)
    
    # Create cryptocurrency exchange rate graph
    graph = create_crypto_graph(data, coins)
    
    # Visualize the graph
    visualize_graph(graph)
    
    # Find opportunities
    smallest_factor, smallest_paths, highest_factor, highest_path = find_arbitrage_opportunities(graph)
    
    # Print  opportunity results
    print('_____________________________________________________')
    print('Smallest Paths weight factor:', smallest_factor) 
    print('Paths:', smallest_paths)   
    
    print('Greatest Paths weight factor:', highest_factor)
    print('Paths:', highest_path)
 
# Ensure script runs only when directly executed
if __name__ == "__main__":
    main()