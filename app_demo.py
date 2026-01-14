#!/usr/bin/env python3
"""
A sample Python application (non-interactive version)
"""

def say_hello(name="World"):
    """Function to say hello"""
    return f"Hello, {name}! Nice to meet you!"

def perform_calculation(num1, num2):
    """Function to perform a calculation"""
    result = num1 + num2
    return f"The sum of {num1} and {num2} is {result}"

def main():
    """Main function of the application"""
    print("Welcome to your new Python application!")
    print("This application is running in the virtual environment.")
    
    # Demonstrating the functionality without user input
    print("\n--- Demonstrating Application Features ---")
    
    # Feature 1: Say hello
    print("1. Say hello:")
    greeting = say_hello("User")
    print(f"   {greeting}")
    
    # Feature 2: Perform a calculation
    print("\n2. Perform a calculation:")
    calc_result = perform_calculation(5, 7)
    print(f"   {calc_result}")
    
    # Additional examples
    print("\n3. More examples:")
    print(f"   {say_hello('Qwen')}")
    print(f"   {perform_calculation(10.5, 20.3)}")
    
    print("\nApplication demonstration completed successfully!")
    print("To use the interactive version, run 'python app.py' and respond to the prompts.")

if __name__ == "__main__":
    main()