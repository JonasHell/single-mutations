import requests, sys

# get output filename and Ensembl ID as user input
print("Enter output file location (e.g. C:/PATH/FILE.csv): ")
filename = input()
filename = str(filename)
if not filename.endswith(".csv"):
    print("Please use .csv in filename.")
    sys.exit()

print("Enter Ensembl ID: ")
ID = input()
ID = str(ID)

print("output file: " + filename)
print("Ensembl ID: " + ID)

# request sequence from ensemble server
server = "https://grch37.rest.ensembl.org"     # use "https://rest.ensembl.org" for current ensembl version
ext = "/sequence/id/" + ID + "?type=cds"
req = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})

# check whether request is okay or not
if not req.ok:
  req.raise_for_status()
  sys.exit()

# convert sequence to text (string), save protein name and remove newline chars
seq = req.text
# first_line = seq[seq.find("\")]
seq = seq[seq.find("\n")+1:]
seq = seq.replace("\n", "")

# write output in output file
out_file = open(filename, "w")
bases = ["A", "C", "G", "T"]
position = 1

for letter in seq:
    for base in bases:
        if letter != base:
            out_file.write(str(position) + letter + ">" + base + "\n")  # heiko.brennenstuhl@med.uni-heidelberg.de
    position += 1

out_file.close()