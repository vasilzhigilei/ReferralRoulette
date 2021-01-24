var myModal = new bootstrap.Modal(document.getElementById('modal'), {
    keyboard: false
});

myModal.show();

function generatenew(slug){
    fetch("/api/generatereferral/" + slug).then(function(response) {
        response.text().then(function(text) {
            document.getElementById('link').value = text;
            if(text != "No referral links") {
                strval = document.getElementById('clicks').textContent;
                document.getElementById('clicks').textContent = (Number(strval) + 1).toString();
            };
            myModal.show();
        });
    });
    gtag('event','generate_new_link',{'service':slug});
}

$('#link').click(function(){
    gtag('event','link_interaction',{'method':'input field'});
});

$('#copy-button').click(function(){
    gtag('event','link_interaction',{'method':'copy button'});
});

$('#open-button').click(function(){
    gtag('event','link_interaction',{'method':'open button'});
});