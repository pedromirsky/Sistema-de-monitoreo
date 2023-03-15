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

// Temperatura Bioterio
var database = firebase.database();
var firebaseRef = firebase.database().ref("BioterioTemperaturaActual");
firebaseRef.on("value", function(snapshot){
    var data = snapshot.val();
    temperatura = data.Temperatura
    console.log(firebaseRef);
    document.getElementById("temperatura").textContent = temperatura
    if(temperatura > 40){
        //alert("supero 40°C")
        console.log("supero 40°c")
    }
})

// Humedad bioterio
var firebaseRef_2 = firebase.database().ref("BioterioHumedadActual");
firebaseRef_2.on("value", function(snapshot){
    var data_2 = snapshot.val();
    humedad = data_2.Humedad
    console.log(data_2);
    document.getElementById("humedad").textContent = humedad
    if(humedad > 70){
        //alert("supero 40°C")
        console.log("supero 70°c")
    }
})