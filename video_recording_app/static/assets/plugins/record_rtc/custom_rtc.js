



var video = document.querySelector('video');
function captureCamera(callback) {
    navigator.mediaDevices.getUserMedia({ audio: true, video: true }).then(function (camera) {
        callback(camera);
    }).catch(function (error) {
        alert('Unable to capture your camera. Please check console logs.');
        console.error(error);
    });
}




function stopRecordingCallback() {
    video.srcObject = null;
    var blob = recorder.getBlob();
    video.src = URL.createObjectURL(blob);
    recorder.camera.stop();
}







var recorder; // globally accessible
document.getElementById('btn-start-recording').onclick = function () {
    this.disabled = true;
    captureCamera(function (camera) {
        video.srcObject = camera;
        recorder = RecordRTC(camera, {
            type: 'video'
        });
        var recordingDuration = parseInt(document.getElementById('txt-recording-duration').value) || 5000;
        recorder.setRecordingDuration(recordingDuration).onRecordingStopped(stopRecordingCallback);
        recorder.startRecording();
        // release camera on stopRecording
        recorder.camera = camera;
        document.getElementById('btn-stop-recording').disabled = false;
        document.getElementById('btn-pause-recording').disabled = false;
    });
};





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
        $name = invokeSaveAsDialog(seekableBlob, 'seekable-recordrtc.webm');
        console.log(seekableBlob);
        alert(seekableBlob);
    });
}





document.getElementById('btn-pause-recording').onclick = function () {
    this.disabled = true;
    if (this.innerHTML === 'Pause Recording') {
        recorder.pauseRecording();
        this.innerHTML = 'Resume Recording';
    }
    else {
        recorder.resumeRecording();
        this.innerHTML = 'Pause Recording';
    }
    setTimeout(function () {
        document.getElementById('btn-pause-recording').disabled = false;
    }, 2000);
};