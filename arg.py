import argparse


def main():
    parser = argparse.ArgumentParser(description="Sample argparse implementation.")
    parser.add_argument("input", type=str, help="Input file path")
    parser.add_argument("output", type=str, help="Output file path")
    parser.add_argument(
        "--verbose", action="store_true", help="Increase output verbosity"
    )

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")


if __name__ == "__main__":
    main()
