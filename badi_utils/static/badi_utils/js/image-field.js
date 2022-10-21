$('.image-field-hover').click(function () {
    const imageField = $(this).parent().find('.d-none input[type=file]')[0];
    let imageBackGround = $(this).parent().find('img').attr('src');
    if (imageField.files.length === 0) {
        imageField.click();
    } else {
        if ($(this).parent().find('.d-none a')) {
            imageBackGround = $(this).parent().find('.d-none a').attr('href')
        }
        imageField.value = "";
        $(this).parent().find('img').attr('src', imageBackGround);
        $(this).find('div').html('<i class="fa fa-upload large"></i>');
    }
});
$('.image-field-1 .switch input[type="checkbox"]').change(function (e) {
    $(this).parent().parent().parent().find('.d-none input[type="checkbox"]').val($(this).val())
})
$(".image-field-1 > .d-none input[type=file]").change(function () {

    var control = $(this)[0];
    var files = control.files;
    var errorText = '';
    var errorIs = false;
    for (var i = 0; i < files.length; i++) {
        if (files[i].type.includes("jpeg") || files[i].type.includes("png") || files[i].type.includes("webp")) {
            errorText = ''
        } else {
            errorText += 'فرمت فایل باید jpg/png/webp باشد' + '<br>';
            errorIs = true;
        }
        if (files[i].size > 2621440 / 5) {
            errorText += 'حجم عکس نباید بیشتر از 0.5 مگابایت باشد' + '<br>';
            errorIs = true;
        }
        if (errorIs) {
            swal.fire({
                title: 'خطا',
                html: '<div class="swal2-html-container">' + errorText + '</div>',
                icon: "error",
                confirmButtonText: "i got that",
                customClass: {
                    confirmButton: "btn font-weight-bold btn-secondary"
                }
            });
            $(this).val('');
        }
    }
    readURL(this);
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var image = new Image();
            image.src = e.target.result;
            $(input).parent().parent().find('img').attr('src', e.target.result)
        };
        reader.readAsDataURL(input.files[0]); // convert to base64 string
        $(input).parent().parent().find('.image-field-hover div').html('<i class="fa fa-trash large"></i>');
    }
}
