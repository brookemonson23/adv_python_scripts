# medium.py
# input into chatgpt:
# Given an array of integers, write a function that finds the second largest number in the array.
# Then analyze the time complexity of the solution using Big O notation, and find what the Big O notation of the code you wrote is

# Time Complexity: O(n)
# The time complexity is O(n), where n is the number of elements in the array.
# This is because we need to iterate through the array exactly once to determine the largest and second largest elements.

def find_second_largest(arr):
    if len(arr) < 2:
        return None  # Array must have at least 2 elements
    
    #set both number to negative infinity first
    largest = second_largest = float('-inf')
    
    #loop through array
    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    
    if second_largest == float('-inf'):
        return None  # No second largest found (all elements are the same)
    
    return second_largest

# Example usage
arr = [10, 5, 8, 12, 3, 7, 12]
result = find_second_largest(arr)
print(f"Second largest number: {result}")