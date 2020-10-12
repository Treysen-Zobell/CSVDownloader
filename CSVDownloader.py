import urllib3
import argparse
import datetime
import sys
import termcolor


# Convert strftime characters (ex: %Y, %m, %d) to current timestamps
# Check for invalid characters in path
def process_filename(filename):
    new_filename = datetime.datetime.now().strftime(filename)
    if 1 in [c in new_filename for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']]:
        print('File destination contained an invalid character!')
        print('Invalid characters are: \\, /, :, *, ?, ", <, >, |')
        sys.exit(-1)
    return new_filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url of file to be downloaded')
    parser.add_argument('-o', '--output', help='where to save file (default: ...\\file). also supports datetime strftime formatting, ex: %Y=year, %m=month, etc.')
    args = parser.parse_args()

    if args.output is None:
        args.output = 'file'
    args.output = process_filename(args.output)

    http = urllib3.PoolManager()
    r = http.request('GET', args.url, preload_content=False)

    try:
        with open(args.output, 'wb') as out:
            while True:
                data = r.read(16)
                if not data:
                    break
                out.write(data)
    except OSError:
        print('OSError Occured. Known causes include:')
        print('   Using ":" in output file option')
        sys.exit(-1)

    r.release_conn()


if __name__ == "__main__":
    main()
