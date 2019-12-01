

document.addEventListener('DOMContentLoaded', init, false);

function init(){

        

    var li = document.getElementsByClassName("tracklist");



    for(var i = 0;i<li.length;i++){
        li[i].addEventListener("click", display);
    }

    function display(e){
        var playlistId;
        if((e.target.attributes.class.value).localeCompare("tracklist")==0 )
        {
            playlistId=e.target.attributes.id.value;
        }
        else
        {
            playlistId=e.target.parentElement.attributes.id.value;
        }
        var player= document.getElementById("embededPlayer");
        player.src="https://open.spotify.com/embed/playlist/"+playlistId;  
        player.style.height="80px";
        var button= document.getElementById("showSongs");
        button.style.display = "block";
        button.innerHTML="show songs";
        
    }

    
}

function showSongs(){
    var button = document.getElementById("showSongs");
    var player =document.getElementById("embededPlayer");
    
    if(button.value== "show songs")
    {
        player.style.height="460px";
        button.value="hide songs";
        button.innerHTML="hide songs";
    }
    else
    {
        player.style.height="80px";
        button.value="show songs";
        button.innerHTML="show songs";
    }
}