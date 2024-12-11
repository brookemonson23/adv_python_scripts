import requests
import json
import networkx as nx
from itertools import permutations
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from datetime import datetime
import os
import csv
import logging

# Set logging level to ERROR to suppress info and debug messages
logging.basicConfig(level=logging.ERROR)

# Alpaca API credentials
api_key = ''
api_secret = ''

# Read the API keys from a file for security
with open('APIkeys.txt', 'r') as file:
    for line in file:
        if 'API_KEY' in line:
            api_key = line.split('=')[1].strip().strip("'")  # Extract API key
        elif 'API_SECRET' in line:
            api_secret = line.split('=')[1].strip().strip("'")  # Extract API secret

# Initialize the Alpaca trading client for executing orders
client = TradingClient(api_key, api_secret, paper=True)

# Dictionary of cryptocurrency names and their respective ticker symbols
coins = {
    'us dollar coin': 'usdc',
    'bitcoin-cash': 'bch',
    'litecoin': 'ltc',
    'ethereum': 'eth',
    'bitcoin': 'btc',
    'polkadot': 'dot',
    'chainlink': 'link',
    'stellar': 'xlm',
    'avalanche': 'avax',
    'basic attention token': 'bat',
    'sushiswap': 'sushi'
}
successful_orders = []  # List to track successful orders

def place_order(symbols, qty, side):
    """Place market orders for given symbols."""
    for symbol in symbols:
        order = MarketOrderRequest(
            symbol=(symbol.strip() + 'USD').upper(),  # Format the symbol for Alpaca
            notional=qty,  # Amount to invest
            side=side,  # Buy or Sell
            time_in_force=TimeInForce.GTC  # Order remains valid until canceled
        )
        try:
            client.submit_order(order_data=order)  # Submit the order to Alpaca
            print(f"{side.capitalize()} order for {symbol} placed successfully.")
            successful_orders.append(symbol.upper())  # Track successful orders
        except Exception as e:
            print(f"Error placing order for {symbol}: {str(e)}")  # Log any errors

def get_exchange_rates():
    """Fetch current cryptocurrency prices from CoinGecko."""
    names_url = ','.join(coins.keys())  # Get the names of cryptocurrencies
    ticker_url = ','.join(coins.values())  # Get the corresponding ticker symbols
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={names_url}&vs_currencies={ticker_url}'
    response = requests.get(url)  # Make the API request
    return response.json()  # Return the price data as JSON

def build_graph(data):
    """Construct a directed graph from exchange rate data."""
    g = nx.DiGraph()  # Initialize a directed graph
    for coin, coin_data in data.items():
        for tkr, rate in coin_data.items():
            node_from = coins[coin]  # Get the source node
            node_to = tkr  # Get the target node
            try:
                g.add_edge(node_from, node_to, weight=rate)  # Add an edge with the exchange rate
            except KeyError:
                print(f"Warning: Missing exchange rate from {node_from} to {node_to}. Skipping...")
                continue
    return g  # Return the constructed graph

def dfs(graph, node, visited):
    """Perform a depth-first search to find reachable nodes."""
    visited.add(node)  # Mark the current node as visited
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)  # Recursively visit neighbors

def check_reachability(graph, start_node):
    """Check which nodes are reachable from the starting node."""
    visited = set()  # Set to track visited nodes
    dfs(graph, start_node, visited)  # Perform DFS
    all_nodes = set(graph.nodes)  # Get all nodes in the graph
    missing_nodes = all_nodes - visited  # Identify missing nodes
    return missing_nodes  # Return unreachable nodes

def check_arbitrage(g):
    """Identify potential arbitrage opportunities in the graph."""
    arbitrage_opportunities = []  # List to store found opportunities

    # Check reachability from BTC
    missing_nodes = check_reachability(g, 'btc')

    if missing_nodes:
        print(f"Not all nodes are reachable from 'btc'. Missing nodes: {missing_nodes}")
        return []  # Exit if not all nodes are reachable
    else:
        print("All nodes are reachable from 'btc'. Proceeding with arbitrage check...")

    # Check for arbitrage opportunities between all pairs of nodes
    for n1, n2 in permutations(g.nodes, 2):
        if n1 in missing_nodes or n2 in missing_nodes:
            continue  # Skip if either node is missing

        for path in nx.all_simple_paths(g, source=n1, target=n2):
            try:
                # Calculate the product of weights for the forward path
                path_weight_to = 1.0
                for i in range(len(path) - 1):
                    path_weight_to *= g[path[i]][path[i + 1]]['weight']

                # Calculate the product of weights for the reverse path
                path_reverse = list(reversed(path))
                path_weight_from = 1.0
                for i in range(len(path_reverse) - 1):
                    path_weight_from *= g[path_reverse[i]][path_reverse[i + 1]]['weight']

                arbitrage_factor = path_weight_to * path_weight_from  # Calculate the arbitrage factor

                # Store the opportunity if it exceeds the threshold
                if arbitrage_factor > 1.0006:
                    arbitrage_opportunities.append({
                        "arbitrage_factor": arbitrage_factor,
                        "forward_path": path,
                        "reverse_path": path_reverse
                    })

            except KeyError:
                print(f"Missing edge for path: {path}")  # Handle missing edges
                continue

    # Sort opportunities by arbitrage factor and select the top 10
    arbitrage_opportunities.sort(key=lambda x: x["arbitrage_factor"], reverse=True)
    top_10_opportunities = arbitrage_opportunities[:10]

    print("=" * 50)
    if top_10_opportunities:
        print("Top 10 Arbitrage Opportunities:")
        for i, opportunity in enumerate(top_10_opportunities):
            print(f"{i + 1}. Arbitrage Factor: {opportunity['arbitrage_factor']}")
            print(f"   Forward Path: {opportunity['forward_path']} -> Reverse Path: {opportunity['reverse_path']}")

        # Save results in the existing data folder
        results_path = os.path.join('data', 'results.json')
        mkdirs = os.makedirs(os.path.dirname(results_path), exist_ok=True)  # Create directory if it doesn't exist
        with open(results_path, 'w') as json_file:
            json.dump(top_10_opportunities, json_file, indent=4)  # Save results as JSON

        return top_10_opportunities  # Return found opportunities
    else:
        print("No arbitrage opportunities found.")
        return []  # Return empty list if no opportunities

def save_arbitrage_pairs_to_csv(opportunities):
    """Save arbitrage opportunities to a CSV file."""
    data_directory = os.path.join('data')  # Use existing data directory
    os.makedirs(data_directory, exist_ok=True)  # Just in case, but it should already exist
    now = datetime.now()  # Get current timestamp
    filename = f"currency_pair_{now.strftime('%Y.%m.%d_%H.%M')}.txt"  # Create a timestamped filename
    filepath = os.path.join(data_directory, filename)  # Full path for the file

    try:
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)  # Create CSV writer
            writer.writerow(['currency_from', 'currency_to', 'exchange_rate'])  # Write header

            # Write each opportunity to the CSV file
            for opportunity in opportunities:
                forward_path = opportunity['forward_path']
                currency_from = forward_path[0]  # Get starting currency
                currency_to = forward_path[-1]  # Get ending currency
                exchange_rate = opportunity['arbitrage_factor']  # Get the arbitrage factor

                writer.writerow([currency_from, currency_to, exchange_rate])  # Write data row

        print(f"Arbitrage pairs saved to {filepath}")  # Log success
    except Exception as e:
        print("Error saving arbitrage pairs to CSV:", str(e))  # Log any errors

def main():
    """Main function to execute the arbitrage trading process."""
    positions = client.get_all_positions()  # Fetch current portfolio positions
    print("\nInitial Portfolio Positions:\n" + "-" * 50)
    for position in positions:
        print(f"{position.qty} shares of {position.symbol}")  # Display initial positions

    data = get_exchange_rates()  # Fetch exchange rates
    g = build_graph(data)  # Construct the graph from the rate data

    top_10_opportunities = check_arbitrage(g)  # Identify arbitrage opportunities

    save_arbitrage_pairs_to_csv(top_10_opportunities)  # Save opportunities to CSV

    # Place orders based on identified opportunities
    if top_10_opportunities:
        for opportunity in top_10_opportunities:
            forward_path = opportunity['forward_path']
            buy_symbol = forward_path[0].upper()  # Get the symbol to buy
            sell_symbol = forward_path[-1].upper()  # Get the symbol to sell
            qty = 100  # Define quantity for orders

            print(f"Placing buy order for {buy_symbol}...")
            place_order([buy_symbol], qty, OrderSide.BUY)  # Place buy order

            print(f"Placing sell order for {sell_symbol}...")
            place_order([sell_symbol], qty, OrderSide.SELL)  # Place sell order
    else:
        print("No arbitrage opportunities found. No orders will be placed.")

    positions = client.get_all_positions()  # Fetch updated positions after trading
    print("Successful Orders:", successful_orders)  # Display successful orders
    print("\nFinal Portfolio Positions:" + "-" * 50)
    for position in positions:
        print(f"{position.qty} shares of {position.symbol}")  # Display final positions

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()  # Start the program