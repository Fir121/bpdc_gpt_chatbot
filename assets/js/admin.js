const format = (text) => {
    return text.replace(/(?:\r\n|\r|\n)/g, '<br>')
}

const markdown          = window.markdownit();

document.addEventListener("load", () => {
    var elems = document.getElementsByClassName("content");
    for (var i=0; i<elems.length; i++){
        var text =  elems.innerHTML;
        elems.innerHTML = markdown.render(text);
    } 
});