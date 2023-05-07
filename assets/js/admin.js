const format = (text) => {
    return text.replace(/(?:\r\n|\r|\n)/g, '<br>')
}

const markdown          = window.markdownit(
    {
        linkify: true,
      }
);

document.addEventListener("load", () => {
    var elems = document.getElementsByClassName("content");
    for (var i=0; i<elems.length; i++){
        var text =  elems.innerHTML;
        elems.innerHTML = markdown.render(text);
    } 
});

document.querySelector('.mobile-sidebar').addEventListener('click', (event) => {
    const sidebar = document.querySelector('.conversations');
    
    if (sidebar.classList.contains('shown'))  {
        sidebar.classList.remove('shown');
        event.target.classList.remove('rotated');
    } else {
        sidebar.classList.add('shown');
        event.target.classList.add('rotated');
    }

    window.scrollTo(0, 0);
})