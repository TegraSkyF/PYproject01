#!/usr/bin/env python3
"""
A sample Python application
"""

def main():
    """Main function of the application"""
    print("Welcome to your new Python application!")
    print("This application is running in the virtual environment.")
    
    # Simple example functionality
    while True:
        print("\nChoose an option:")
        print("1. Say hello")
        print("2. Perform a calculation")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            name = input("What's your name? ")
            print(f"Hello, {name}! Nice to meet you!")
        elif choice == "2":
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = num1 + num2
                print(f"The sum of {num1} and {num2} is {result}")
            except ValueError:
                print("Please enter valid numbers!")
        elif choice == "3":
            print("Thank you for using the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()