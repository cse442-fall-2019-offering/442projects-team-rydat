

document.addEventListener('DOMContentLoaded', init, false);

function init(){

        

    var li = document.getElementsByClassName("tracklist");



    for(var i = 0;i<li.length;i++){
        li[i].addEventListener("click", myScript);
    }

    function myScript(e){
        var playlistId=e.target.attributes.id.value;
        document.getElementById("embededPlayer").src="https://open.spotify.com/embed/playlist/"+playlistId;       
    }

}