import { submitData } from './searchFunctions'

const startDictation = () => {

    if (window?.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new window.webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
            const query = e.results[0][0].transcript
            document.getElementById('transcript').value = query;
            recognition.stop();
            // document.getElementById('searchForm').submit();
            submitData({
                'query' : query
            });
        };
        
        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}

export {
    startDictation
}