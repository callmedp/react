const startDictation = () => {

    if (window?.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new window.webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
            document.getElementById('transcript').value = e.results[0][0].transcript;
            recognition.stop();
            // document.getElementById('searchForm').submit();
        };
        
        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}

export {
    startDictation
}