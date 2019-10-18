// this link works
// https://accounts.spotify.com/authorize?client_id=c00c658f3a8a4a29961ae9fe70ffde7e&redirect_uri=http:%2F%2Flocalhost:8888%2Fcallback&scope=user-read-private%20user-read-email&response_type=token&state=123
// do this function uses http://jsfiddle.net/JMPerez/62wafrm7/ for reference
// https://developer.spotify.com/documentation/web-api/libraries/

function dothis() {
    
    function login(callback) {
        // var CLIENT_ID = 'c00c658f3a8a4a29961ae9fe70ffde7e';
        var CLIENT_ID = '39f9460f4cc04748bc5db13628766419' ;
        var REDIRECT_URI = 'https://www-student.cse.buffalo.edu/CSE442-542/2019-Fall/cse-442j/';   
        function getLoginURL(scopes) {
            return 'https://accounts.spotify.com/authorize?client_id=' + CLIENT_ID +
              '&redirect_uri=' + encodeURIComponent(REDIRECT_URI) +
              '&scope=' + encodeURIComponent(scopes.join(' ')) +
              '&response_type=token';
        }
        
        var url = getLoginURL([
            'user-read-email'
        ]);
        
        var width = 450,
            height = 730,
            left = (screen.width / 2) - (width / 2),
            top = (screen.height / 2) - (height / 2);
    
        window.addEventListener("message", function(event) {
            var hash = JSON.parse(event.data);
            if (hash.type == 'access_token') {
                callback(hash.access_token);
            }
        }, false);
        
        var w = window.open(url,
                            'Spotify',
                            'menubar=no,location=no,resizable=no,scrollbars=no,status=no, width=' + width + ', height=' + height + ', top=' + top + ', left=' + left
                           );
        
    }

    function getUserData(accessToken) {
        return $.ajax({
            url: 'https://api.spotify.com/v1/me',
            headers: {
               'Authorization': 'Bearer ' + accessToken
            }
        });
    }

    var loginButton = document.getElementById('btn');
    

        login(function(accessToken) {
            getUserData(accessToken)
                .then(function(response) {
                    console.log("hello");
                    window.location.href ="index.html"
                        //  window.location.href =""

                });
            });
  
    
}