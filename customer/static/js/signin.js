
var config = {
    apiKey: "AIzaSyD8vfREJDT-2TIyZiWLUOTYev4EZ30ZOQ8",
    authDomain: "hsnetworld-da138.firebaseapp.com",
    databaseURL: "https://hsnetworld-da138.firebaseio.com",
    projectId: "hsnetworld-da138",
    storageBucket: "hsnetworld-da138.appspot.com",
    messagingSenderId: "1087402057046",
    appId: "1:1087402057046:web:e82ae844efa1df4bf10af7",
    measurementId: "G-CKLJL1YSTE"
  };

if (!firebase.apps.length) {
    firebase.initializeApp(config);
}
function currentUser(){
var currentUser = firebase.auth().currentUser;
}
function DetectIphone(){
var uagent = navigator.userAgent.toLowerCase();
}
function Googleauth(){

var provider = new firebase.auth.GoogleAuthProvider();

if (!firebase.apps.length) {
    firebase.initializeApp(config);
}

else{
    firebase.auth().signInWithPopup(provider).then(function(result) {
        // This gives you a Google Access Token. You can use it to access the Google API.
        var token = result.credential.accessToken;
        // The signed-in user info.
        var user = result.user;
            sessionStorage.setItem('user', JSON.stringify(user.uid))
            sessionStorage.setItem('name', JSON.stringify(user.displayName))
        // ...
        }).catch(function(error) {
            console.log(error)
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // The email of the user's account used.
        var email = error.email;
        // The firebase.auth.AuthCredential type that was used.
        var credential = error.credential;
        // ...
    });
}
}
function phoneAuth(){
try{
    window.open('http://127.0.0.1:8000/customer-service/phone-auth','mywin','width=500,height=500 status=yes, toolbar=no, menubar=no, location=no,addressbar=no');
    window.opener.postMessage(true, '*');
}
catch(e){
    console.log(e)
}

}
function setValue(val1) {
sessionStorage.setItem('user', JSON.stringify(val1.uid))
}
firebase.auth().onAuthStateChanged(function(user) {

if (user) {
sessionStorage.setItem('detailed', JSON.stringify(user))
sessionStorage.setItem('user', user.uid)
sessionStorage.setItem('name', JSON.stringify(user.displayName))            
window.location.href = "http://127.0.0.1:8000/customer-service/dashboard";
} else {
// No user is signed in.
console.log("USER NOT LOGGED IN");
}
});