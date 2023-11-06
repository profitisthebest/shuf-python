#!/usr/local/cs/bin/python3

import random, sys, string, argparse

def main():
    usage_message = """Usage: %(prog)s [OPTION]... [FILE]\n
    or:  %(prog)s -e [OPTION]... [ARG]...\n
    or:  %(prog)s -i LO-HI [OPTION]...\n
    Write a random permutation of the input lines to standard output.\n
    \n
    With no FILE, or when FILE is -, read standard input.\n
    \n
    Mandatory arguments to long options are mandatory for short options too.\n
    """
    parser = argparse.ArgumentParser(description=usage_message)

    parser.add_argument(
        "-e",
        "--echo",
        action="store",
        nargs="*",
        dest="echo",
        help="treat each arg as an input line"
    )
    parser.add_argument(
        "-i",
        "--input_range",
        action="store",
        dest="input_range",
        help="treat each number LO through HI as an input line"
    )
    parser.add_argument(
        "-n",
        "--head-count",
        action="store",
        dest="head_count",
        type=int,
        help="output at most COUNT lines"
    )
    parser.add_argument(
        "-r",
        "--repeat",
        action="store_true",
        dest="repeat",
        help="output lines can be repeated",
        default=False
    )


    args, unknown_args = parser.parse_known_args(sys.argv[1:])
    headcount = None
    result = []
    unknownlength = len(unknown_args)


    # option error
    if args.echo and args.input_range:
        parser.error("cannot combine -e and -i options")


    if args.head_count:
        if args.head_count < 0:
            parser.error("invalid line count: {0}".format(args.head_count))
        headcount = args.head_count


    if args.echo is not None:
        result = args.echo
        if unknownlength:
            result.extend(unknown_args)
        random.shuffle(result)
        if args.head_count:
            if args.head_count > len(result):
                i = len(result)
            else: 
                i = args.head_count
            for line in result[:i]:
                sys.stdout.write(line + "\n")
        else:
            for line in result:
                sys.stdout.write(line + "\n")
        exit(0)
    elif args.input_range:
        temp = str(args.input_range)
        input_r = temp.split("-")
        if len(input_r) != 2:
            parser.error("invalid input range: {0}".format(args.input_range))
        l = int(input_r[0])
        h = int(input_r[-1])
        if l >= 0 and h >= 0 and l-h <= 1:
            result = [i for i in range(l, h+1)]
        else:
            parser.error("invalid input range: {0}".format(args.input_range))
    elif args.input_range is None:
        if unknownlength==0 or unknown_args[0] == "-":
            temp = sys.stdin.readlines()
            result = [line.rstrip('\n') for line in temp]
        else:
            filename = unknown_args[0]
            f = open(filename, 'r')
            result = [line.rstrip('\n') for line in list(f)]
            f.close()
    else:
        if unknownlength:
            parser.error("extra operand '" + unknown_args[0] + "'")

    random.shuffle(result)

    if not args.repeat and args.head_count is None: # false true
        if headcount is None:
            headcount = len(result)
        while headcount > 0:
            sys.stdout.write(str(result[headcount-1]) + '\n')
            headcount -= 1
    elif not args.repeat and args.head_count is not None: # false false
        if headcount > len(result):
            headcount = len(result)
        while headcount > 0:
            sys.stdout.write(str(result[headcount-1]) + '\n')
            headcount -= 1
    elif args.repeat and args.head_count is None: # true true
        while headcount != 0:
            sys.stdout.write(str(result[0]) + '\n')
            random.shuffle(result)
            # infinite loop
    else: # true false
        while headcount > 0:
            sys.stdout.write(str(result[0]) + '\n')
            random.shuffle(result)
            headcount -= 1

if __name__ == "__main__":
    main()
