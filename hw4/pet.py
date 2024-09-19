#chatgptlink: https://chatgpt.com/c/66ec7ee3-42ac-8002-b0d4-52fd565aa46a

class Pet:
    # Class variable to store species
    species = ""
    
    # Constructor to initialize name, age, and species
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        Pet.species = species
    
    # Method to calculate age in human years
    def age_in_human_years(self):
        if Pet.species == 'dog':
            return self.age * 7  # Dog years
        elif Pet.species == 'cat':
            return self.age * 5  # Cat years
        else:
            return self.age  # For other animals, assume 1-to-1 ratio for simplicity
    
    # Static method to get the average lifespan of the species
    @staticmethod
    def average_lifespan(species):
        lifespans = {
            'dog': 13,
            'cat': 15,
            'rabbit': 9,
            'bird': 5,
            'hamster': 2
        }
        return lifespans.get(species, "Unknown lifespan")

# Creating instances of the Pet class
pet1 = Pet("Buddy", 3, "dog")
pet2 = Pet("Whiskers", 2, "cat")
pet3 = Pet("Nibbles", 1, "rabbit")

# Calculate and print the age of each pet in human years
print(f"{pet1.name} is {pet1.age_in_human_years()} human years old.")
print(f"{pet2.name} is {pet2.age_in_human_years()} human years old.")
print(f"{pet3.name} is {pet3.age_in_human_years()} human years old.")

# Retrieve and print the average lifespan for each pet's species
print(f"The average lifespan of a {pet1.species} is {Pet.average_lifespan(pet1.species)} years.")
print(f"The average lifespan of a {pet2.species} is {Pet.average_lifespan(pet2.species)} years.")
print(f"The average lifespan of a {pet3.species} is {Pet.average_lifespan(pet3.species)} years.")

