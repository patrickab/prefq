// Get buttons
var on_left_preferred       = document.getElementById('left_preferred')
var on_right_preferred      = document.getElementById('right_preferred')
// Get videos
var left_video              = document.getElementById('left_video')
var right_video             = document.getElementById('right_video')
// Get filename
var video_filename_left     = document.getElementById("video_filename_left").textContent;

let is_left_preferred  = null


function send_data() {
    
    const xhr = new XMLHttpRequest()                            // Create AJAX request to server   (HTTP request made by browser-resident Javascript)
    xhr.open('POST', '/feedback')                               // Set the HTTP method and endpoint URL
    xhr.setRequestHeader('Content-Type', 'application/json')    // Specify JSON datatype for HTTP header

    // Define http status code behavior
    xhr.onreadystatechange = function() {
        
        if (xhr.status >= 200 && xhr.status < 400 && xhr.readyState === XMLHttpRequest.DONE) // if http status between 200-399 (indicates success)  &&  if request has been sent
            // Handle successful requests
            {
            const response = JSON.parse(xhr.responseText)
            if(response.success === true)   {console.log('Acknowledgment received')}
            else                            {console.log('Message transfer failed')}
            }
                
        else
            // Handle unsuccessful requests
            {console.log('Request failed with status:', xhr.status)}
        }

    const data = {                                 // Prepare user data
        is_left_preferred: is_left_preferred,
        video_filename_left: video_filename_left,
        };
    const jsonData = JSON.stringify(data)          // Convert user data 
    xhr.send(jsonData)                             // Send user data to Server
}


function request_videos() {

    var xhr = new XMLHttpRequest();       // Create AJAX request to server
    xhr.open('GET', '/')                  // Set the HTTP method and endpoint URL

    // Define http status code behavior
    xhr.onreadystatechange = function() {

        if (xhr.status >= 200 && xhr.status < 400 && xhr.readyState === XMLHttpRequest.DONE) // if http status between 200-399 (indicates success)  &&  if request has been sent
            // Handle successful requests
            {
            console.log("Videos requested successfully");
            const newInterface = xhr.responseText;
            document.documentElement.innerHTML = newInterface;  // Update the DOM with the new interface
            attachEventHandlers();                              // Reattach event handlers to the new elements
            }
                
        else 
            // Handle unsuccessful requests
            {console.log('Request failed with status:', xhr.status)}

    };

    xhr.send(); 
}


function attachEventHandlers() {
    
    on_left_preferred  = document.getElementById('left_preferred');
    on_right_preferred = document.getElementById('right_preferred');
    video_filename_left = document.getElementById("video_filename_left").textContent;

    on_left_preferred.addEventListener('click', function() {
        is_left_preferred = true;
        send_data();
        request_videos();
    });

    on_right_preferred.addEventListener('click', function() {
        is_left_preferred = false;
        send_data();
        request_videos();
    });
}

// Attach Signal Handler
attachEventHandlers();

// Send null value to server when user leaves page without selecting preference
window.onbeforeunload = function() {
    if (is_left_preferred === null) {
        send_data();
    }
};