import os
import sys
import shutil

import re

########################################
#####  Get andd Set filenames
########################################
output_folder = "../Live"
input_file = sys.argv[1] if len(sys.argv) > 1 else input("Enter filename: ")
base_name = os.path.splitext(os.path.basename(input_file))[0]
js_file = "../../blog-posts.js"


title = (
    base_name
    .replace("-", " ")   # hyphens -> spaces
    .replace("_", " ")   # underscores -> spaces
    .title()             # Capitalize words
)

destination_html = os.path.join(output_folder, base_name + ".html")
destination_txt = os.path.join(output_folder, os.path.basename(input_file))

########################################
#### Error Handling (overwrite) 
########################################

existing_files = [
    path for path in (destination_html, destination_txt)
    if os.path.exists(path)
]

if existing_files:
    print("The following files already exist:")
    for path in existing_files:
        print(f"  {path}")

    try:
        response = input("Overwrite existing files? (y/n): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        raise SystemExit(1)

    if response != "y":
        print("Operation cancelled.")
        raise SystemExit(0)

########################################
####    Read article into HTML
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
<h2></h2>

<h2>🔬 {title}</h2>

<p>

{article}

</p>
<br>

    <div class="blog-nav">
        <a id="bot-prevBtn">◀ Previous</a>
        <!--<span id="bot-postNumber"></span>-->
        <a id="bot-nextBtn">Next ▶</a>
    </div>    
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

############################################
####  HTML Loaded now some file handling 
############################################

with open(destination_html, "w", encoding="utf-8") as outfile: outfile.write(html)
shutil.move(input_file, destination_txt)

#### "article.html" was created and moved to 'Live' ####

with open(js_file, "r", encoding="utf-8") as f:
    content = f.read()
#
 #   new_entry = f'    "{base_name}.html"'
#
 #   pattern = r'(const blogPosts = \[\s*)(.*?)(\s*\];)'
#
 #   content, count = re.subn(
  #      pattern,
   #     lambda m: m.group(1) + m.group(2).rstrip() +
    #        ("," if m.group(2).strip() else "") +
   #         "\n" + new_entry + "\n" + m.group(3).strip(),
   #     content,
   #     count=1,
   #     flags=re.DOTALL
   # )

    # if count == 0:
    #    raise ValueError("Could not find the blogPosts array in the JS file.")

############### test ####
    pattern = r'(const blogPosts = \[\s*)(.*?)(\s*\];)'
    match = re.search(pattern, content, flags=re.DOTALL)

    if not match:
        raise SystemExit("Could not find the blogPosts array in the JS file.")

    new_entry = f'"{base_name}.html"'
    entries = re.findall(r"""["']([^"']+\.html)["']""", match.group(2))

    # Remove existing copies of this filename
    entries = [entry for entry in entries if entry != f"{base_name}.html"]

    # Add it once at the beginning
    entries.insert(0, f"{base_name}.html")

    # Rebuild the array
    array_content = ",\n".join(f'    "{entry}"' for entry in entries)

    content = (
        match.group(1)
        + "\n"
        + array_content
        + "\n"
        + match.group(3).strip()
    )

with open(js_file, "w", encoding="utf-8") as f: f.write(content)

####  blog-posts.js has been appended!  ####

print("Finished converting.")
