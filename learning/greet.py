import argparse

def main():

    # define what arguements cli tool accepts
    parser = argparse.ArgumentParser(description="Greet Someone") # creates the parser itself
    parser.add_argument("first_name", help="first name") # declare a positional arguemnt 
    parser.add_argument("last_name", help="last_name") # declare a positional arguement

    parser.add_argument("--shout", action="store_true", help="greet loudly") # optional flag 
    parser.add_argument("--times", type=int, default=1, help="how many times") # optional flag
    parser.add_argument("--whisper", action="store_true", help="greet softly") # optional flag

    # use arguements
    args = parser.parse_args()

    greeting = f"Hello, {args.first_name} {args.last_name}!"
    if args.shout:
        greeting = greeting.upper()

    if args.whisper:
        greeting = greeting.lower()
    
    for _ in range(args.times):
        print(greeting)

if __name__ == "__main__":
    main()