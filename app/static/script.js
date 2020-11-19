var modal = document.getElementById("myModal");

var class_show = function(class_name, class_id, length)
{
    xhttp = new XMLHttpRequest();
    left_ = event.pageX + 10;
    top_ = event.pageY + 10;
    height_ = 26 + 78;
    width_ = 84 * length;
    xhttp.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            modal.setAttribute("style", "left: "+left_+"px; top: "+top_+"px; width:"+width_+"px; height: "+height_+"px;");
            modal.innerHTML = this.response;
            modal.style.display = "block";
            MathJax.typeset();
        }
    };
    xhttp.open("GET", "/explore/"+class_name+"/"+class_id, true);
    xhttp.send();
}

var class_hide = function()
{
    modal.style.display = "none";
}

