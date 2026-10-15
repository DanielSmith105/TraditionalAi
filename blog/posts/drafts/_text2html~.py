import os
import sys
import subprocess

###################################################################################
# subprocesses for tasklist and ansi color workarounds
###################################################################################
subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Write-Output 'Subprocess Ready!'"])
print(f"\033[1;36m{sys.executable}\033[0m\n\033[3m\033[0m")

########################################
# Get filenames
########################################

input_file = input("\n\033[92mDirectory:\033[0m Type the path to the file: ")
base_name = os.path.splitext(os.path.basename(input_file))[0]


title = (
    base_name
    .replace("-", " ")   # hyphens -> spaces
    .replace("_", " ")   # underscores -> spaces
    .title()             # Capitalize words
)
output_folder = input("\n\033[92mDirectory:\033[0m Type the output path: ")
output_file = os.path.join(output_folder, base_name + ".html")

########################################
# Read article
########################################

with open(input_file, "r", encoding="utf-8") as infile:
    article = infile.read()

# Replace line breaks with HTML
article = article.replace("&", "&amp;")
article = article.replace("<", "&lt;")
article = article.replace(">", "&gt;")
article = article.replace("\n", "<br>\n")

html = f"""<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{base_name}</title>

    <link rel="stylesheet" href="../../../style.css">
    <link rel="icon" type="image/png"
          href="../../../images/icons8-search-in-browser-windows-11-color-96.png">
</head>

<body>

<div class="stars"></div>

<div id="header"></div>

<script>
fetch("../../../header.html")
.then(response => response.text())
.then(html => {{
    document.getElementById("header").innerHTML = html;
}});
</script>

<nav>
    <a href="../../../index.html">Home</a>
    <a href="../../../index.html#about">About</a>
    <a href="../../../index.html#services">Services</a>
    <a href="../../../index.html#research">Research</a>
    <a href="../../../index.html#news">News</a>
    <a href="../../../index.html#events">Events</a>
    <a href="../../../index.html#partners">Partners</a>
    <a href="../../../index.html#contact">Contact</a>
    <a href="../../../index.html#blog" class="button-link active">Blog</a>
</nav>

<main>

<section id="blog">
    <a href="../../../blog/blog-index.html">Back to All Posts  <span id="postNumber"></span></a> 
    
    <div class="blog-nav">
        <a id="prevBtn">◀ Previous</a>
        <a id="nextBtn">Next ▶</a>
    </div>

<h2>🔬 {title}</h2>

<p>

{article}

</p>

</section>

<section id="legal">

<h2>⚖ Legal Information</h2>

<p>
This website is operated by a nonprofit advanced technological
corporation. All content is provided for informational purposes
unless otherwise stated.
</p>

</section>

</main>

<div id="footer"></div>

<script>
fetch("../../../footer.html")
.then(response => response.text())
.then(html => {{
    document.getElementById("footer").innerHTML = html;
}});
</script> 

<script src="../../blog-posts.js"></script>
<script src="../../blog-nav.js"></script> 

</body>
</html>
"""

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write(html)

print("Finished converting.")