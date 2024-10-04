# hard.py
# input into chatgpt: 
# Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array.
# Then analyze the time complexity of the solution using Big O notation, and find what the Big O notation of the code you wrote is 

def max_difference(arr):
    if len(arr) < 2:
        return None  # Array must have at least 2 elements
    
    #initiatlize min_element to the first element
    min_element = arr[0]
    max_diff = 0
    
    #loop through array
    for i in range(1, len(arr)):
        #if the difference between the current element and min_element is greater than max_diff, update max_diff
        if arr[i] - min_element > max_diff:
            max_diff = arr[i] - min_element
        #if the current element is less than min_element, update min_element
        if arr[i] < min_element:
            min_element = arr[i]
    #return max_diff
    return max_diff

# Example usage
arr = [7, 1, 5, 3, 6, 4]
result = max_difference(arr)
print(f"Maximum difference: {result}")

# Time Complexity: O(n)
# We iterate through each element once, performing constant-time operations for each.
# So, the time complexity is the same as the array size.