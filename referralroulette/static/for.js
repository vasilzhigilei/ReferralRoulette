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
}

$('#link').click(function(){
    ga('send','event','Click','Input Field');
});

$('#copy-button').click(function(){
    ga('send','event','Click','Copy Button');
});

$('#open-button').click(function(){
    ga('send','event','Click','Open New Tab Button');
});