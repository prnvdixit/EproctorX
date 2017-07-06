/* Javascript for EproctoringXBlock. */
function EproctoringXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var startingtime = runtime.handlerUrl(element, 'startingtime');
    var endingtime = runtime.handlerUrl(element, 'endingtime');
    var differenceoftimes = runtime.handlerUrl(element, 'differenceoftimes');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });
    

    $(function ($) {
        /* Here's where you'd do things on page load. */

        
var modal1 = document.getElementById('myModal1');
var modal2 = document.getElementById('myModal2');
var modal3 = document.getElementById('myModal3');
var modal4 = document.getElementById('myModal4');
var modal5 = document.getElementById('myModal5');
var resize_count=0;
var notification_count=0;
// Get the button that opens the modal
//var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span1 = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
var span3 = document.getElementsByClassName("close")[2];
var span4 = document.getElementsByClassName("close")[3];

// When the user clicks the button, open the modal 
/*btn.onclick = function() {
    modal.style.display = "block";
}*/

// When the user clicks on <span> (x), close the modal
span1.onclick = function() {
    modal1.style.display = "none";
}
span2.onclick = function() {
    modal2.style.display = "none";
}
span3.onclick = function() {
    modal3.style.display = "none";
}
span4.onclick = function() {
    modal4.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
    }
window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}
window.onclick = function(event) {
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
}
window.onclick = function(event) {
    if (event.target == modal4) {
        modal4.style.display = "none";
    }
}
//DETECTION OF SPECIAL KEYS SUCH AS CTRL,SHIFT,ALT
function detectspecialkeys(e){
    var evtobj=window.event? window.event : e
    if (evtobj.altKey || evtobj.ctrlKey){//evtobj.shiftKey
        //window.alert("DON'T PRESS CTRL,ALT,SHIFT AND ANY SPECIAL KEYS");
        modal1.style.display = "block";}
}

//VISIBILITY CHANGER--MINIMIZING,NEW TAB
/*document.addEventListener("visibilitychange", function() {
if (document.hidden) {//window.alert("YOU SHOULD NOT MINIMIZE BROWSER");
	modal2.style.display = "block";} 
else {   }
});*/
document.onkeydown=detectspecialkeys

//RESIZING FUNCTION
window.addEventListener("resize", myFunction);
function myFunction() {
	if(resize_count!=0){
    //window.alert("DON'T RESIZE WINDOW");
    modal3.style.display = "block";
    }//var element = document.getElementById('myModal3');
    //screenshot_modal(element);
    else
    resize_count++;
}

//NAVIGATES TO OTHER PAGES
//flag=0;
var away=0;
var flag = 0;
// flag == 0 means that person is away from page for the first time
setInterval( checkPageFocus, 200 );
function checkPageFocus() {
  if ( document.hasFocus() ) {
     notification_count=0;
     if(away==1){   
	//	  var getData;
	//    $.ajax({
        //    type: "POST",
        //    url: endingtime,
        //    data: JSON.stringify({"hello": "world"}),
            //success: alert("ending time funvtion"),
           
       // });
        $.ajax({
            type: "POST",
            url: differenceoftimes,
            data: JSON.stringify({"hello": "world"}),
            //success: alert("difference time function"),
          
        });flag=0;
        away = 0;
        }
     else{}

      }
  else {//window.alert("DON'T NAVIGATE TO OTHER APPLICATIONS/DON'T MINIMIZE THE BROWSER.STAY HERE ONLY");
	if(flag == 0){
 	  $.ajax({
            type: "POST",
            url: startingtime,
            data: JSON.stringify({"hello": "world"}),
            //success: alert("starting time function"),
        });away=1;flag = 1;
}
           modal4.style.display = "block";notifyMe();notification_count=1;}
}
//var getCanvas;
//function screenshot_modal (element) {
//         html2canvas(element, {
//         onrendered: function (canvas) {
//                $("#previewImage").append(canvas);
//                getCanvas = canvas;
//             }
//        });
//    };


//CLOSING TAB OR WINDOW
/*window.addEventListener("beforeunload", function (e) {
 var confirmationMessage = "tab close";
e.returnValue = confirmationMessage;     //Gecko + IE
window.event.returnValue = confirmationMessage;
 sendkeylog(confirmationMessage);
return confirmationMessage;                                //Webkit, Safari, Chrome etc.
});*/ 

//NOTIFICATIONS
function notifyMe() {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }

  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
	  if(notification_count==0){
    // If it's okay let's create a notification
       var notification = new Notification("Suspicious Activity Identified", {

        body: "Don't navigate to other pages and don't minimize the browser!. Please go back to the browser window of the test again."

        }); }
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== "denied") {
    Notification.requestPermission(function (permission) {
      // If the user accepts, let's create a notification
      if (permission === "granted") {
		  if(notification_count==0){
       var notification = new Notification("Suspicious Activity Identified", {

        body: "Don't navigate to other pages and don't minimize the browser!. Please go back to the browser window of the test again."

        }); }
      }
    });
  }

  // At last, if the user has denied notifications, and you 
  // want to be respectful there is no need to bother them any more.
}




        
        
    });
}






