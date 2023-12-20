import argparse
import sys
def parse_args(args):
    parser = argparse.ArgumentParser(description="generate answer",add_help=True)
    parser.add_argument(
        '-f',nargs='?',default=1,
        help='starting_index'
    )
    parser.add_argument(
        '-l',nargs='?',default=1107,
        help='ending_index'
    )
    parser.add_argument(
        '-i',
        help='filepath_of_ques_csv', required=True
    )
    parser.add_argument(
        '-o',nargs='?',default='not_provided',
        help='file_path_of_output_csv'
    )
    parser.add_argument(
        '-d', '-output',
        help='filepath_of_dataset_csv', required=True
    )
    parser.add_argument(
        '-c',nargs='?',default='not_provided',
        help='answer_column_name'
    )
    parsed_args = parser.parse_args()
    return parsed_args


def main(args):
    args = parse_args(args)
    return [args.f,args.l,args.i,args.o,args.d,args.c]
if __name__ == '__main__':
    main(sys.argv[1:])