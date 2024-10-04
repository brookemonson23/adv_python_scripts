#easy.py
#input into chatgpt: 

def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total

# Example usage
arr = [1, 2, 3, 4, 5]
result = sum_array(arr)
print(f"Sum of array elements: {result}")

# Time Complexity: O(n), where n is the number of elements in the array.
# We iterate through each element once and perform a constant-time operation.
# So, the time complexity, is the same size as the input array.