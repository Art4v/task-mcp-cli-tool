import argparse

def main():

    # define what arguements cli tool accepts
    parser = argparse.ArgumentParser(description="Greet Someone") # creates the parser itself
    parser.add_argument("name", help="who to greet") # declare a positional arguemnt 
    parser.add_argument("--shout", action="store_true", help="greet loudly") # optional flag 
    parser.add_argument("--times", type=int, default=1, help="how many times") # optional flag

    # use arguements
    args = parser.parse_args()

    greeting = f"Hello, {args.name}!"
    if args.shout:
        greeting = greeting.upper()

    for _ in range(args.times):
        print(greeting)

if __name__ == "__main__":
    main()