import os
import sys
import shutil

########################################
# Get filenames
########################################
output_folder = "../Live"
input_file = sys.argv[1]

base_name = os.path.splitext(os.path.basename(input_file))[0]

title = (
    base_name
    .replace("-", " ")   # hyphens -> spaces
    .replace("_", " ")   # underscores -> spaces
    .title()             # Capitalize words
)
output_file = os.path.join(output_folder, base_name + ".html")

destination = os.path.join(
    output_folder,
    os.path.basename(input_file)
)

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
    <a href="../../../index.html#blog" class="active">Blog</a>
</nav>

<main>

<section id="blog">

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

</body>
</html>
"""

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write(html)

shutil.move(input_file, destination)

print("Finished converting.")
