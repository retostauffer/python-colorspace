

from bs4 import BeautifulSoup
import re, sys, os

args = sys.argv
if len(args) == 1:
    sys.exit("Input argument missing. Usage: {:s} <htmlfile.html>".format(args[0]))
file = args[1]
if not os.path.isfile(args[1]):
    sys.exit("File \"{:s}\" cannot be found.".format(file))

with open(file,"r") as fid: content = fid.readlines()
# Remove blank lines
content = ["" if (len(l) == 0 or re.match("^\\n$",l)) else l for l in content]
BS = BeautifulSoup("".join(content), "lxml")

# Rip scripts and styles out of the doc
for s in BS(["script","style"]): s.extract()
# Take body
body = str(BS(["body"]))
body = re.findall("(?<=\<body>).*(?=\</body\>)", body)[0]

# Write new content
fid = open(file, "w+")
for l in body.split("\\n"): fid.write("{:s}\n".format(l))
fid.close()


