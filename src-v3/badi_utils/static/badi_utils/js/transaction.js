$('.charge-modal').click(function (e) {
    $('#charge-modal').modal('show');
});
$('#request-charge-form').on('submit', function (e) {
    e.preventDefault();
    ApiAjax({
        method: 'POST',
        url: ZP_TRANSACTION_REQUEST_CHARGE,
        form: '#request-charge-form',
        success_message: false,
        modal: '#charge-modal',
        button: $(this).find('button[type=submit]')[0],
        success: (res) => {
            window.open(res['redirect'], '_self')
        },
        error: (err) => {
            if (err.reason && err.reason.error)
                swalFireError(err.reason.error)
        }
    });
});
