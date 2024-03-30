var search_bar = document.getElementById("search");
var keyword_info = document.getElementById("keyword_info");
var graph = document.getElementById("graph");

search_bar.addEventListener('keypress', getData);

async function getData(evt){
    if (evt.key == "Enter" && search_bar.checkValidity()){
        var search_keyword = search_bar.value;
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