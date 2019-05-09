$(document).ready(function () {

    // To Initialise Date picker
    $("#datepicker-view-start").datepicker({
        autoClose: true,
        viewStart: 2
    });

    $("#bvn-validation").on('keyup paste', function () {
        $length = $(this).val().length;
        if($length == 10){
            $(this).css("border", "1px solid green");
        }else{
            $(this).css("border", "1px solid red");
        }
    });

    let $className = $('.if-profile-image-change');
    $className.on('change', function (e) {
        e.preventDefault();
        let $formData = new FormData(this);
        let $url = $className.attr('action') || window.location.href;
        $.ajax({
            method: 'POST',
            url: $url,
            data: $formData,
            success: changeImageHanler,
            error: function (errorData) {
                console.log(errorData);
            },
            processData: false,
            contentType: false,
            cache: false,
        });
    });

    const changeImageHanler = (data) => { 
        if (data.status == "success") {
            $('.avater-container img').remove();
            $newImg = '<img src="/media/' + data.avatar + '" height="200px" width="200px" class="dashboard_image_settings">';
            $('.avater-container').prepend($newImg);
        }
    };









    // To handle error generated
    function handleError(ThrowError) {
        console.log(ThrowError)
    }

    // To capitalize the first letter of any string
    function capitalize(s) { return s.toUpperCase(); }
    String.prototype.capitalize = function () {
        return this.toString().replace(/\b[a-z]/g, capitalize);
    };







});



