# main.py

import argparse
from diff_match_patch import DiffMatchPatch

def main():
    parser = argparse.ArgumentParser(description="Diff Match Patch API")
    parser.add_argument("operation", choices=["diff", "match", "patch"], help="Operation to perform")
    parser.add_argument("text1", help="First text or the main text")
    parser.add_argument("text2", nargs='?', default="", help="Second text or the pattern (optional for patching)")
    parser.add_argument("pattern", nargs='?', default="", help="Pattern to match (required for match operation)")

    args = parser.parse_args()

    dmp = DiffMatchPatch()

    if args.operation == "diff":
        diffs = dmp.diff_main(args.text1, args.text2)
        print("Diffs:", diffs)
    elif args.operation == "match":
        if not args.pattern:
            print("Error: The 'match' operation requires a 'pattern' argument.")
            return
        loc = dmp.match_main(args.text1, args.pattern)
        print("Best match found at index:", loc)
    elif args.operation == "patch":
        patches = dmp.patch_make(args.text1, args.text2)
        patched_text = dmp.patch_apply(patches, args.text1)
        print("Patched text:", patched_text)

if __name__ == "__main__":
    main()