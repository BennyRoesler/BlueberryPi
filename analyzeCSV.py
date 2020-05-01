import csv
import argparse
import json

# Parse arguments
parser = argparse.ArgumentParser(
    description='Analyze CSV file from BlueberryPi')
parser.add_argument('-i', '--input', metavar='<CSV file path>',
                    help='Path to CSV file to analyze')

parser.add_argument('-o', '--output', metavar='<Output file path>',
                    help='Path to output txt file')

args = parser.parse_args();

if not args.input:
    print("CSV file path missing. Please use '-i <CSV file path>'")
    exit(1)

if not args.output:
    print("Output file path missing. Please use '-o <Output file path>'")
    exit(1)


csvfile = open(args.input, 'r')
filereader = csv.reader(csvfile)

parsed = {}

write = open(args.output, "w+")

for i in filereader:
    if not i[0] in parsed: # if key doesn't exist
        parsed[i[0]] = i[1]

    if not i[4] == "None":
        parsed[i[0]] += ", "
        parsed[i[0]] += i[4]

write.write(json.dumps(parsed))

print(f"Output file saved at: {args.output}")