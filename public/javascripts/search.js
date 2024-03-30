var search_field = document.getElementById("search");
var keyword_info = document.getElementById("statistics");
var graph = document.getElementById("graph");
var back_arrow = document.getElementById("home");

//Statistics Tab DOM Elements
var meanField = document.getElementById("mean");
var gradientField = document.getElementById("gradient");
var peakField = document.getElementById("peak");
var minimumField = document.getElementById("minimum");
var maximumField = document.getElementById("maximum");
var interceptField = document.getElementById("intercept");
var currentInterestField = document.getElementById("current");

search_field.addEventListener('keypress', getData);
back_arrow.addEventListener('click', returnHome);
console.log("search.js is loaded!");

initial_page_load();

//Run once when page is loaded
async function initial_page_load(){
    var search_keyword = search_field.value;
    console.log("Submit "+search_keyword+"!");
    try {
        let response = await fetch('http://localhost:3000/search?keyword='+search_keyword);
        if (response.status == 200){
            var data = await response.json();
            var mean = data.mean.toString();
            var gradient = data.gradient.toString();
            var peak = data.peak;
            var minimum = data.minimum.toString();
            var maximum = data.maximum.toString();
            var intercept = data.intercept.toString();
            var current = data.currentInterest.toString();
            var img_link = data.image_link;

            meanField.innerHTML = `Mean Views: <b>${mean}</b>`;
            gradientField.innerHTML = `Linear Gradient: <b>${gradient}</b>`;
            peakField.innerHTML = `Peak Popularity: <b>${peak}</b>`;
            minimumField.innerHTML = `Minimum Views: <b>${minimum}</b>`;
            maximumField.innerHTML = `Maximum Views: <b>${maximum}</b>`;
            interceptField.innerHTML = `Interest Intercept: <b>${intercept}</b>`;
            currentInterestField.innerHTML = `Current Interest: <b>${current}</b>`;

            graph.innerHTML = 
            `
            <img src="${img_link}" id="graph_img" alt="Graph detailing the keyword's popularity trend for the last seven days">
            `;
        }
        else{
            console.log("HTTP return status: "+response.status);
            var data = await response.json();
            keyword_info.innerHTML = 
            `
            Error: ${response.status + " " + data.error}
            `;
            graph.innerHTML = 
            `
            Error: ${response.status + " " + data.error}
            `;
        }
    }
    catch {
        console.log("Fetch Error!");
    }
}

async function getData(evt){
    if (evt.key == "Enter" && search_field.checkValidity()){
        var search_keyword = search_field.value;
        try {
            let response = await fetch('http://localhost:3000/searchpage?keyword='+search_keyword);
            if (response.status == 200){
                console.log("Changing Webpage...")
                window.location = 'http://localhost:3000/searchpage?keyword='+search_keyword;
            }
            else{
                console.log("HTTP return status: "+response.status);
            }
        }
        catch {
            console.log("Fetch Error!");
        }
    }
}

async function returnHome(){
    try {
        let response = await fetch('http://localhost:3000/')
        if (response.status == 200){
            console.log("Changing Webpage...")
            window.location = 'http://localhost:3000/';
        }
        else
        {
            console.log("HTTP return status: "+response.status);
        }
    }
    catch {
        console.log("HTTP return status: "+response.status);
    }
}