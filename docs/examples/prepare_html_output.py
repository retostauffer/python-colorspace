

from bs4 import BeautifulSoup
import re, sys, os

if __name__ == "__main__":

    # ---------------------------------------------------------------
    # Parsing input arguments (a html file)
    # ---------------------------------------------------------------
    args = sys.argv
    if len(args) == 1:
        sys.exit("Input argument missing. Usage: {:s} <htmlfile.html>".format(args[0]))
    file = args[1]
    if not os.path.isfile(args[1]):
        sys.exit("File \"{:s}\" cannot be found.".format(file))
    
    with open(file,"r") as fid: content = fid.readlines()
    # Remove blank lines
    content = ["" if (len(l) == 0 or re.match("^\\n$",l)) else l for l in content]
    
    # ---------------------------------------------------------------
    # Extracting the body, remove included scripts and stuff.
    # ---------------------------------------------------------------
    BS = BeautifulSoup("".join(content), "lxml")
    # Rip scripts and styles out of the doc
    for s in BS(["script","style"]): s.extract()
    # Take body
    body = str(BS(["body"]))
    body = re.findall("(?<=\<body>).*(?=\</body\>)", body)[0]

    # ---------------------------------------------------------------
    # Replace some strings with html
    # ----------------------------------------------------------------
    ## <pre><code><check class="Rpy all-fine">All fine</check></code></pre>
    ## "## &lt;check class="Rpy all-fine"&gt;All fine&lt;/check&gt;" to html
    def check_to_html(body):
        body = body.split("\\n")
        for i in range(0, len(body)):
            pat = "<pre><code>(##\s+\\&lt;check.*)(?=(<\\/code><\\/pre>))"
            mtch = re.match(pat, body[i])
            if not mtch: continue
            # Manipulate the expression
            def comment_to_html(x):
                x = x.replace("#","").replace("&lt;", "<").replace("&gt;", ">")
                return x
            print mtch.group(1)
            body[i] = comment_to_html(mtch.group(1))
            #body[i] = body[i].replace(mtch.group(1), comment_to_html(mtch.group(1)))
    
        # Return body (as one string)
        return "\n".join(body)
    
    body = check_to_html(body)
    
    # ---------------------------------------------------------------
    # Write new content
    # ---------------------------------------------------------------
    fid = open(file, "w+")
    for l in body.split("\\n"):  fid.write("{:s}\n".format(l))
    fid.close()


