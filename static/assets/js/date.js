

// ============================ Date :
var element = document.getElementById("inpDate");

let unix_timestamp = element // from django
var now = new Date(unix_timestamp * 1000);
var day = ("0" + now.getDate()).slice(-2);
var month = ("0" + (now.getMonth() + 1)).slice(-2);
var today = now.getFullYear() + "-" + (month) + "-" + (day);

element.value = today;