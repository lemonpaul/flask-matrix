var modal = document.getElementById("myModal");

var h_class_show = function(class_id, length, height, width)
{
    xhttp = new XMLHttpRequest();
    left_ = event.pageX + 10;
    top_ = event.pageY + 10;
    height_ = 26 + 26 * height;
    width_ = (12 + 24 * width)*length;
    xhttp.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            modal.setAttribute("style", "left: "+left_+"px; top: "+top_+"px; width:"+width_+"px; height: "+height_+"px;");
            modal.innerHTML = this.response;
            modal.style.display = "block";
            MathJax.typeset();
        }
    };
    xhttp.open("GET", "/class/h_class/"+class_id, true);
    xhttp.send();
}

var h_class_hide = function(class_id)
{
    modal.style.display = "none";
}
