
markdown: str = """
# A Compendium of Code Snippets and Random Information

## Table of Contents
1. [Programming Languages](#programming-languages)
2. [Historical Facts](#historical-facts)
3. [Science Tidbits](#science-tidbits)
4. [Mathematical Concepts](#mathematical-concepts)
5. [Literature Excerpts](#literature-excerpts)
6. [Cooking Recipes](#cooking-recipes)
7. [Famous Quotes](#famous-quotes)
8. [Interesting Animals](#interesting-animals)
9. [World Geography](#world-geography)
10. [Music Theory](#music-theory)

## Programming Languages

### Python

Python is a high-level, interpreted programming language known for its simplicity and readability.

```python
# Hello World in Python
print("Hello, World!")

# Function to calculate factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

# Example usage
print(factorial(5))  # Output: 120
```

### JavaScript

JavaScript is a versatile programming language primarily used for web development.

```javascript
// Hello World in JavaScript
console.log("Hello, World!");

// Arrow function to check if a number is prime
const isPrime = (num) => {
  for (let i = 2; i <= Math.sqrt(num); i++) {
    if (num % i === 0) return false;
  }
  return num > 1;
};

// Example usage
console.log(isPrime(17));  // Output: true
```

### Java

Java is a popular object-oriented programming language known for its "write once, run anywhere" philosophy.

```java
// Hello World in Java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// Bubble Sort implementation
public static void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                // swap arr[j+1] and arr[j]
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}
```

### Ruby

Ruby is a dynamic, object-oriented programming language known for its simplicity and productivity.

```ruby
# Hello World in Ruby
puts "Hello, World!"

# Method to generate Fibonacci sequence
def fibonacci(n)
  return [] if n == 0
  return  if n == 1
  fib = [0, 1]
  (2...n).each do |i|
    fib << fib[i-1] + fib[i-2]
  end
  fib
end

# Example usage
p fibonacci(10)  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### C++

C++ is a powerful, high-performance programming language that extends the C programming language.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

// Hello World in C++
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}

// Function to find the maximum element in a vector
template <typename T>
T findMax(const std::vector<T>& vec) {
    return *std::max_element(vec.begin(), vec.end());
}

// Example usage
std::vector<int> numbers = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
std::cout << "Max element: " << findMax(numbers) << std::endl;
```

## Historical Facts

1. The Great Wall of China is the largest man-made structure in the world, stretching over 13,000 miles.

2. The ancient Egyptians were the first to develop a 365-day calendar.

3. The Rosetta Stone, discovered in 1799, was instrumental in deciphering ancient Egyptian hieroglyphs.

4. The printing press was invented by Johannes Gutenberg around 1440, revolutionizing the spread of information.

5. The Industrial Revolution began in Great Britain in the late 18th century and spread to other parts of the world.

6. The American Revolution lasted from 1765 to 1783 and resulted in the independence of the United States from Great Britain.

7. The French Revolution, which began in 1789, led to the end of the monarchy in France and significant social and political changes.

8. World War I, also known as the Great War, lasted from 1914 to 1918 and involved many of the world's major powers.

9. The Russian Revolution of 1917 led to the creation of the Soviet Union, the world's first socialist state.

10. The Apollo 11 mission in 1969 resulted in the first human landing on the Moon.

## Science Tidbits

1. The speed of light in a vacuum is approximately 299,792,458 meters per second.

2. The human body contains enough carbon to make about 900 pencils.

3. The Earth's atmosphere is composed of approximately 78% nitrogen, 21% oxygen, and 1% other gases.

4. The Great Red Spot on Jupiter is a giant storm that has been raging for at least 400 years.

5. The human brain contains about 86 billion neurons.

6. The coldest temperature theoretically possible is absolute zero, which is -273.15°C or -459.67°F.

7. DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms.

8. The Hubble Space Telescope was launched into low Earth orbit in 1990 and remains in operation today.

9. Quantum entanglement is a phenomenon where particles become interconnected and share their quantum states.

10. The periodic table of elements currently contains 118 confirmed elements.

## Mathematical Concepts

### The Fibonacci Sequence

The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones. It typically starts with 0 and 1.

```python
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return 
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### The Golden Ratio

The golden ratio, denoted by φ (phi), is approximately 1.618033988749895. It's found in various natural phenomena and is often used in art and architecture.

```python
import math

def golden_ratio():
    return (1 + math.sqrt(5)) / 2

print(f"The golden ratio is approximately {golden_ratio():.10f}")
```

### The Pythagorean Theorem

The Pythagorean theorem states that in a right-angled triangle, the square of the length of the hypotenuse is equal to the sum of squares of the other two sides.

```python
def pythagorean_theorem(a, b):
    return math.sqrt(a**2 + b**2)

print(f"The hypotenuse of a right triangle with sides 3 and 4 is {pythagorean_theorem(3, 4)}")
```

### The Euler's Number (e)

Euler's number, e, is a mathematical constant approximately equal to 2.71828. It's the base of natural logarithms.

```python
def calculate_e(precision):
    e = 2
    factorial = 1
    for i in range(2, precision):
        factorial *= i
        e += 1 / factorial
    return e

print(f"e is approximately {calculate_e(100):.10f}")
```

### The Sieve of Eratosthenes

The Sieve of Eratosthenes is an ancient algorithm for finding all prime numbers up to a given limit.

```python
def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    primes = primes = False
    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i*i, n+1, i):
                primes[j] = False
    return [i for i in range(n+1) if primes[i]]

print(sieve_of_eratosthenes(50))
```

## Literature Excerpts

1. From "Pride and Prejudice" by Jane Austen:
   "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife."

2. From "1984" by George Orwell:
   "War is peace. Freedom is slavery. Ignorance is strength."

3. From "To Kill a Mockingbird" by Harper Lee:
   "You never really understand a person until you consider things from his point of view...Until you climb inside of his skin and walk around in it."

4. From "The Great Gatsby" by F. Scott Fitzgerald:
   "So we beat on, boats against the current, borne back ceaselessly into the past."

5. From "Moby-Dick" by Herman Melville:
   "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."

## Cooking Recipes

### Classic Chocolate Chip Cookies

Ingredients:
- 2 1/4 cups all-purpose flour
- 1 tsp baking soda
- 1 tsp salt
- 1 cup unsalted butter, softened
- 3/4 cup granulated sugar
- 3/4 cup brown sugar
- 2 large eggs
- 2 tsp vanilla extract
- 2 cups semi-sweet chocolate chips

Instructions:
1. Preheat oven to 375°F (190°C).
2. In a bowl, mix flour, baking soda, and salt.
3. In another bowl, cream together butter and sugars. Beat in eggs and vanilla.
4. Gradually stir in the dry ingredients. Fold in chocolate chips.
5. Drop spoonfuls of dough onto ungreased baking sheets.
6. Bake for 9-11 minutes or until golden brown.
7. Cool on baking sheets for 2 minutes, then transfer to wire racks.

### Simple Tomato Pasta Sauce

Ingredients:
- 2 tbsp olive oil
- 1 onion, finely chopped
- 2 cloves garlic, minced
- 2 cans (14.5 oz each) crushed tomatoes
- 1 tsp dried basil
- 1 tsp dried oregano
- Salt and pepper to taste
- Sugar to taste (optional)

Instructions:
1. Heat olive oil in a saucepan over medium heat.
2. Add onion and garlic, cook until softened.
3. Add crushed tomatoes, basil, and oregano.
4. Simmer for 20-30 minutes, stirring occasionally.
5. Season with salt and pepper. Add sugar if desired to balance acidity.
6. Serve over your favorite pasta.

## Famous Quotes

1. "I think, therefore I am." - René Descartes

2. "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe." - Albert Einstein

3. "Be the change you wish to see in the world." - Mahatma Gandhi

4. "To be or not to be, that is the question." - William Shakespeare (Hamlet)

5. "I have a dream that one day this nation will rise up and live out the true meaning of its creed: 'We hold these truths to be self-evident, that all men are created equal.'" - Martin Luther King Jr.

6. "Ask not what your country can do for you – ask what you can do for your country." - John F. Kennedy

7. "The only way to do great work is to love what you do." - Steve Jobs

8. "In three words I can sum up everything I've learned about life: it goes on." - Robert Frost

9. "The greatest glory in living lies not in never falling, but in rising every time we fall." - Nelson Mandela

10. "Life is what happens to you while you're busy making other plans." - John Lennon

## Interesting Animals

1. Axolotl: A salamander with the ability to regenerate lost body parts.

2. Tardigrade: Microscopic animals that can survive extreme conditions, including the vacuum of space.

3. Platypus: A semi-aquatic egg-laying mammal with a duck-like bill.

4. Octopus: Highly intelligent invertebrates known for their problem-solving abilities.

5. Naked Mole Rat: Eusocial mammals with high resistance to cancer and pain.

6. Leafcutter Ant: Ants that cultivate fungus gardens as their primary food source.

7. Mantis Shrimp: Crustaceans with complex eyes and powerful striking claws.

8. Lyrebird: Australian birds known for their elaborate courtship displays and ability to mimic sounds.

9. Pangolin: Scaly anteaters that are unfortunately the most trafficked mammals in the world.

10. Blob Fish: Deep-sea fish that appear blob-like when brought to the surface due to decompression.

## World Geography

1. The Nile is the longest river in the world, stretching 6,650 kilometers (4,132 miles).

2. Russia is the largest country by land area, covering 17,098,246 square kilometers (6,601,670 square miles).

3. The Dead Sea, bordering Israel and Jordan, is the lowest point on Earth at 423 meters (1,388 feet) below sea level.

4. The Pacific Ocean is the largest and deepest ocean, covering an area of about 165,250,000 square kilometers (63,800,000 square miles).

5. Antarctica is the coldest continent, with the lowest recorded temperature on Earth at -89.2°C (-128.6°F).

6. The Amazon Rainforest, primarily located in Brazil, is the largest tropical rainforest in the world.

7. Mount Everest, located in the Himalayas, is the highest point on Earth at 8,848 meters (29,029 feet) above sea level.

8. The Great Barrier Reef off the coast of Australia is the world's largest coral reef system.

9. The Sahara Desert in North Africa is the largest hot desert in the world, covering an area of about 9,200,000 square kilometers (3,600,000 square miles).

10. Venice, Italy is built on 118 small islands connected by bridges and separated by canals.

## Music Theory

### The Major Scale

The major scale is one of the most fundamental concepts in Western music. It consists of seven notes with a specific pattern of whole steps and half steps.

```python
def major_scale(root):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    root_index = notes.index(root)
    scale = [notes[(root_index + i) % 12] for i in [0, 2, 4, 5, 7, 9, 11]]
    return scale

print(major_scale('C'))  # Output: ['C', 'D', 'E', 'F', 'G', 'A', 'B']
```

### The Circle of Fifths

The Circle of Fifths is a visual representation of the relationships among the 12 tones of the chromatic scale, their corresponding key signatures, and the associated major and minor keys.
"""

markdown2: str = """# Random Facts You Didn't Know

## 1. Honey Never Spoils
Honey has been found in ancient Egyptian tombs that is over 3,000 years old and still perfectly edible. Its natural preservatives and low moisture content make it resistant to bacteria.

## 2. Bananas are Berries
Botanically speaking, bananas are classified as berries, while strawberries are not! This is due to the way the plants grow and produce fruit.

## 3. The Eiffel Tower Can Be 15 cm Taller in Summer
Due to thermal expansion, the iron structure of the Eiffel Tower expands in heat, making it up to 15 centimeters taller during the summer months.

## 4. Octopuses Have Three Hearts
Two hearts pump blood to the gills, while one pumps it to the rest of the body. Interestingly, when an octopus swims, the heart that delivers blood to the body stops beating!

## 5. A Day on Venus is Longer Than a Year on Venus
Venus has an extremely slow rotation on its axis, taking about 243 Earth days to complete one rotation. In contrast, it takes about 225 Earth days to orbit the Sun.

## 6. Cows Have Best Friends
Studies have shown that cows are social animals and can form close bonds with other cows. When separated from their friends, they can become stressed.

## 7. The Shortest War in History Lasted 38 Minutes
The Anglo-Zanzibar War fought between the United Kingdom and the Sultanate of Zanzibar on August 27, 1896, is considered the shortest war in history.

## 8. Humans Share 60% of Their DNA with Bananas
While we may not look like bananas, a significant portion of our genetic makeup is shared with them! This highlights the common ancestry of all living organisms.

## 9. A Group of Flamingos is Called a "Flamboyance"
Flamingos are known for their vibrant colors and unique social behavior. Their collective noun reflects their striking appearance and social nature.

## 10. The World's Largest Desert is Antarctica
When most people think of deserts, they picture hot sandy landscapes. However, a desert is defined by its low precipitation levels, making Antarctica the largest desert on Earth.
"""
