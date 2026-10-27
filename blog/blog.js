const list = document.getElementById("blog-post-list");

blogPosts.forEach(file => {
    const li = document.createElement("li");
    const link = document.createElement("a");

    link.href = `posts/Live/${file}`;
    link.textContent = file;

    li.appendChild(link);
    list.appendChild(li);
});