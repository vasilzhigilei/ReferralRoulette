function generatenew(slug){
    fetch("/api/generatereferral/" + slug).then(function(response) {
        response.text().then(function(text) {
            document.getElementById('link').value = text;
            if(text != "No referral links") {
                strval = document.getElementById('clicks').textContent;
                document.getElementById('clicks').textContent = (Number(strval) + 1).toString();
            };
        });
    });
}