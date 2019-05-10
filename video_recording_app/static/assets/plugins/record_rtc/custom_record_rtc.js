


const ConfirmDelete = () => { 
    let $del = confirm("Are you sure you want to delete this video?")
    if ($del)
        return true;
    else
        return false;
}





var video = document.querySelector('video');
function captureStream(callback) {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(function (stream) {
        callback(stream);
    }).catch(function (error) {
        console.error(error);
        alert('Unable to capture your stream. Please check console logs.\n' + error);
    });
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



// when you click on stop recording
function stopRecordingCallback() {
    video.muted = false;
    video.volume = 1;
    video.src = video.srcObject = null;
    getSeekableBlob(recorder.getBlob(), function (seekableBlob) {
        video.src = URL.createObjectURL(seekableBlob);
        recorder.stream.stop();
        recorder.destroy();
        recorder = null;
        document.getElementById('btn-start-recording').disabled = false;
        


        let $formData = new FormData();
        $formData.append("video_name", seekableBlob, 'uploaded_video.webm');
        let $url = "/dashboard/";
        console.log(seekableBlob)
        $.ajax({
            method: 'POST',
            url: $url,
            data: $formData,
            success: function(data) {
                console.log(data);
            },
            error: function (errorData) {
                console.log(errorData);
            },
            processData: false,
            contentType: false,
            cache: false,
        });

        // invokeSaveAsDialog(seekableBlob, 'seekable-recordrtc.webm');

    });
}








var recorder; // globally accessible
document.getElementById('btn-start-recording').onclick = function () {
    this.disabled = true;
    captureStream(function (stream) {
        video.muted = true;
        video.volume = 0;
        video.srcObject = stream;
        recorder = RecordRTC(stream, {
            type: 'video'
        });
        // var recordingDuration = 5000;
        // recorder.setRecordingDuration(recordingDuration).onRecordingStopped(stopRecordingCallback);
        recorder.startRecording();
        // release stream on stopRecording
        recorder.stream = stream;
        console.log(recorder);
        document.getElementById('btn-stop-recording').disabled = false;
    });
};







document.getElementById('btn-stop-recording').onclick = function () {
    this.disabled = true;
    recorder.stopRecording(stopRecordingCallback);
};





function addStreamStopListener(stream, callback) {
    stream.addEventListener('ended', function () {
        callback();
        callback = function () { };
    }, false);
    stream.addEventListener('inactive', function () {
        callback();
        callback = function () { };
    }, false);
    stream.getTracks().forEach(function (track) {
        track.addEventListener('ended', function () {
            callback();
            callback = function () { };
        }, false);
        track.addEventListener('inactive', function () {
            callback();
            callback = function () { };
        }, false);
    });
}