import argparse
from diff_match_patch import DiffMatchPatch

def main():
    parser = argparse.ArgumentParser(description="Diff Match Patch API")
    subparsers = parser.add_subparsers(dest="operation")

    diff_parser = subparsers.add_parser("diff", help="Compute differences between two texts")
    diff_parser.add_argument("text1", help="First text")
    diff_parser.add_argument("text2", help="Second text")

    match_parser = subparsers.add_parser("match", help="Find the best match of a pattern within a text")
    match_parser.add_argument("text", help="Text to search in")
    match_parser.add_argument("pattern", help="Pattern to match")

    patch_parser = subparsers.add_parser("patch", help="Transform text1 into text2 using patches")
    patch_parser.add_argument("text1", help="Original text")
    patch_parser.add_argument("text2", help="Target text")

    args = parser.parse_args()

    dmp = DiffMatchPatch()

    if args.operation == "diff":
        diffs = dmp.diff_main(args.text1, args.text2)
        print("Diffs:", diffs)
    elif args.operation == "match":
        loc = dmp.match_main(args.text, args.pattern)
        print("Best match found at index:", loc)
    elif args.operation == "patch":
        patches = dmp.patch_make(args.text1, args.text2)
        patched_text = dmp.patch_apply(patches, args.text1)
        print("Patched text:", patched_text)

if __name__ == "__main__":
    main()