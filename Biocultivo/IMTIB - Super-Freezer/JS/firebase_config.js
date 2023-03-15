// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyBrGwM_jZCwwk3T-3dRPFq1hU2q2Gumo28",
    authDomain: "r-pi-5fa93.firebaseapp.com",
    databaseURL: "https://r-pi-5fa93-default-rtdb.firebaseio.com",
    projectId: "r-pi-5fa93",
    storageBucket: "r-pi-5fa93.appspot.com",
    messagingSenderId: "72246664319",
    appId: "1:72246664319:web:210c416fcdbdde4cc2b34a"
    };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Temperatura Super Freezer
var firebaseRef_3 = firebase.database().ref("SuperFreezer-TemperaturaActual");
firebaseRef_3.on("value", function(snapshot){
    var data_3 = snapshot.val();
    super_f = data_3.TemperaturaSuperFreezer
    console.log(data_3);
    document.getElementById("super_f").textContent = super_f
    if(super_f > -80){
        //alert("supero 40°C")
        console.log("supero -80°c")
    }
})