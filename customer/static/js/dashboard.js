
var firebaseConfig = {
  apiKey: "AIzaSyD8vfREJDT-2TIyZiWLUOTYev4EZ30ZOQ8",
  authDomain: "hsnetworld-da138.firebaseapp.com",
  databaseURL: "https://hsnetworld-da138.firebaseio.com",
  projectId: "hsnetworld-da138",
  storageBucket: "hsnetworld-da138.appspot.com",
  messagingSenderId: "1087402057046",
  appId: "1:1087402057046:web:e82ae844efa1df4bf10af7",
  measurementId: "G-CKLJL1YSTE"
};

// $(document).on('click','.close',function(){
// 	$(this).parents('span').remove();

// })

// document.getElementById('uploadBtn').onchange = uploadOnChange;



    
// function uploadOnChange() {
//     document.getElementById("uploadFile").value = this.value;
//     var filename = this.value;
//     var lastIndex = filename.lastIndexOf("\\");
//     if (lastIndex >= 0) {
//         filename = filename.substring(lastIndex + 1);
//     }
//     var files = $('#uploadBtn')[0].files;
//     for (var i = 0; i < files.length; i++) {
//      $("#upload_prev").append('<span>'+'<div class="filenameupload">'+files[i].name+'</div>'+'<p class="close" >X</p></span>');
//     }
//     document.getElementById('filename').value = filename;
// }


var message_ele = document.getElementById("flash");
setTimeout(function(){ 
    message_ele.style.display = "none"; 
}, 5000);
function getUserDetails(){

    let displayName = null
    const name = sessionStorage.getItem('name')
    if(name === null){
        const mobile = JSON.parse(sessionStorage.getItem('detailed'))
        if(!mobile){
          window.location.href = "http://127.0.0.1:8000/customer-service/"
        }
        displayName = mobile.phoneNumber
        document.getElementById('job-owner').value = displayName
    }
    else{
        displayName = name
        document.getElementById('job-owner').value =JSON.parse(sessionStorage.getItem('detailed'))["email"]
    }
    if(!displayName){
      window.location.href = "http://127.0.0.1:8000/customer-service/"
    }
    else{
      document.getElementById('user-name').innerText = displayName
    }

}

if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
}
function logOut(){
    firebase.auth().signOut().then(function() {
        sessionStorage.clear();
        window.location.href = "http://127.0.0.1:8000/customer-service/"
    }, function(error) {
    });
}



if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

      // Create a Recaptcha verifier instance globally
      // Calls submitPhoneNumberAuth() when the captcha is verified
      window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
        'size': 'invisible',
        'callback': function(response) {
            submitPhoneNumberAuth()
        },
        'expired-callback': function() {
            window.close()
            // Response expired. Ask user to solve reCAPTCHA again.
            // ...
        }
        });
      // This function runs when the 'sign-in-button' is clicked
      // Takes the value from the 'phoneNumber' input and sends SMS to that phone number
      function submitPhoneNumberAuth() {
        var phoneNumber = document.getElementById("phoneNumber").value;
        var appVerifier = window.recaptchaVerifier;
        appVerifier.verify()
        firebase
          .auth()
          .signInWithPhoneNumber(phoneNumber, appVerifier)
          .then(function(confirmationResult) {
            window.confirmationResult = confirmationResult;
          })
          .catch(function(error) {
            console.log(error);
          });
      }

      // This function runs when the 'confirm-code' button is clicked
      // Takes the value from the 'code' input and submits the code to verify the phone number
      // Return a user object if the authentication was successful, and auth is complete
      function submitPhoneNumberAuthCode() {
        var code = document.getElementById("code").value;
        confirmationResult
          .confirm(code)
          .then(function(result) {
            var user = result.user;
            window.opener.setValue(user.uid);
            window.close()
          })
          .catch(function(error) {
            console.log(error);
          });
      }



      //This function runs everytime the auth state changes. Use to verify if the user is logged in
      firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            
            window.opener.setValue(user);
            window.close()
        } else {
          // No user is signed in.
          console.log("USER NOT LOGGED IN");
        }
      });
        