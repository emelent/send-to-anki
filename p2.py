import sys


def main():
    # Read from standard input
    print("Reading from stdin:")
    stdin_lines = sys.stdin.read().strip().splitlines()  # Read all input at
    for line in stdin_lines:
        print(f"Received: {line.strip()}")

    # Now asking for additional input
    try:
        name = input("your name: ")
    except EOFError:
        print("\nNo name provided.")
        return

    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
