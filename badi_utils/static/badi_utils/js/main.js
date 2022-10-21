const success = "#1BC5BD", info = "#8950FC", warning = "#FFA800", danger = "#F64E60";
const persianMonth = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",]
if (!String.prototype.isInList) {
    Object.defineProperty(String.prototype, 'isInList', {
        get: () => function (...args) {
            let value = this.valueOf();
            for (let i = 0, l = args.length; i < l; i += 1) {
                if (arguments[i] === value) return true;
            }
            return false;
        }
    });
}
const urlSearchParams = new URLSearchParams(window.location.search)
const CURRENT_URL = window.location.pathname,
    CURRENT_SEARCH = window.location.search,
    URL_SEARCH_PARAMS = new URLSearchParams(window.location.search),
    NEXT_PAGE_REDIRECT = URL_SEARCH_PARAMS.get('next');
const badiConfig = {
    ...{
        tooltip: true,
        star: true,
        select2_placeholder: 'جهت انتخاب کلیک کنید!',
        select2_direction: 'rtl',
        select2_active: true,
        select2_searching_text: 'درحال جستجو',
        select2_no_result_text: 'موردی یافت نشد',
        element_image_404: '/static/assets/media/users/default.jpg',
        currency_append: " تومان",
        calendar_date_active: true,
        calendar_datetime_active: true,
        clock_picker_active: true,


    }, ...window['BADI_CONFIG']
}
const getCurrentValueOfKey = (key, def = "") => {
    if (!localStorage.getItem(key)) {
        localStorage.setItem(key, "")
    }
    return localStorage.getItem(key)
}
const getCurrentPage = (default_page = 1) => {
    let page = urlSearchParams.get('page');
    if (page) {
        return parseInt(page)
    } else {
        return default_page
    }
}
const getCurrentPages = (default_page = 1) => {
    let page = urlSearchParams.get('pages');
    if (page) {
        return parseInt(page)
    } else {
        return default_page
    }
}
const initDefaultFormsUI = () => {
    $('[data-toggle="tooltip"], [data-toggle="kt-tooltip"]').tooltip();
    $('form:not(.filters):not([data-filter]) input[required]').parent().find('label').append(' <span class="text-danger"> * </span> ');
    $('form:not(.filters):not([data-filter]) select[required]').parent().find('label').append(' <span class="text-danger"> * </span> ');
    $('form:not(.filters):not([data-filter]) textarea[required]').parent().find('label').append(' <span class="text-danger"> * </span> ');

    $('input.only-number').keydown(function (e) {
        $(this).val($(this).val().replace(/[^\d].+/, ""));
        console.log(e.which)
        if (!((e.which >= 48 && e.which <= 57) ||
            (e.which >= 96 && e.which <= 105) ||
            e.which === 16 ||
            e.which === 37 ||
            e.which === 35 ||
            e.which === 36 ||
            e.which === 39 ||
            e.which === 13 ||
            e.which === 17 ||
            e.which === 18 ||
            e.which === 27 ||
            e.which === 8 ||
            e.which === 9
        ))
            if (!((e.which > 48 && e.which < 57) || (e.which > 95 && e.which < 106)))
                e.preventDefault();
    });
    $(".percent-input").change(function () {
        CheckPercentageNumber($(this))
    }).keyup(function () {
        CheckPercentageNumber($(this));
    });

    $(".persian-input").change(function () {
        JustPersian($(this))
    }).keyup(function () {
        JustPersian($(this));
    });
    if (badiConfig.select2_active)
        $('form select:not(.no-select2)').select2({
            dir: badiConfig.select2_direction,
            minimumResultsForSearch: -1,
            allowClear: true,
            placeholder: badiConfig.select2_placeholder
        });
    $('form').on('reset', function (e) {
        $(this).find('select').val('').change()
    });
}
$(document).ready(function () {
    initDefaultFormsUI()
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function elementImageNotFound(image) {
    image.onerror = "";
    image.src = badiConfig.element_image_404;
    return true;
}

var scrollToElement = function (el, ms) {
    var speed = (ms) ? ms : 600;
    $('html,body').animate({
        scrollTop: $(el).offset().top
    }, speed);
};
const swalDelete = {
    title: 'آیا مطمئن هستید ؟',
    text: "رکورد پس از حذف قابل بازگشت نخواهد بود !",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#F64E60',
    cancelButtonColor: '#0bb783',
    confirmButtonText: 'بله! حذفش کن',
    cancelButtonText: 'لغو'
};
const swalFireError = (desc = 'مشکلی پیش آمده است.') => {
    swal.fire('خطا', desc, 'error');
};
const swalFireSuccess = (desc = 'با موفقیت انجام شد.') => {
    swal.fire('انجام شد!', desc, 'success');
};
const swalFireLoading = (title = 'درحال دریافت اطلاعات...', html = "لطفا منتظر بمانید") => {
    Swal.fire({
        title: title,
        html: html,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
        }
    })
};
const swalFireClose = () => Swal.close();

const valid_persian_date = /^[0-9]{4}\/[0-9]{1,2}\/[0-9]{1,2}?$/,
    valid_persian_datetime = /^[0-9]{4}\/[0-9]{1,2}\/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}?$/
;
const code_meli_valid = (input) => {
    input = toEnglishDigit(input);
    if (!/^\d{10}$/.test(input)
        || input == '0000000000'
        || input == '1111111111'
        || input == '2222222222'
        || input == '3333333333'
        || input == '4444444444'
        || input == '5555555555'
        || input == '6666666666'
        || input == '7777777777'
        || input == '8888888888'
        || input == '9999999999')
        return false;
    var check = parseInt(input[9]);
    var sum = 0;
    var i;
    for (i = 0; i < 9; ++i) {
        sum += parseInt(input[i]) * (10 - i);
    }
    sum %= 11;
    return (sum < 2 && check == sum) || (sum >= 2 && check + sum == 11);
}

const bodyLoading = (qs = 'body') => document.querySelector(qs).classList.add('loading');
const bodyLoadingDisable = (qs = 'body') => document.querySelector(qs).classList.remove('loading');
const toEnglishDigit = (replaceString) => {
    var find = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    var replace = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var regex;
    for (var i = 0; i < find.length; i++) {
        regex = new RegExp(find[i], "g");
        replaceString = replaceString.replace(regex, replace[i]);
    }
    return replaceString;
};

const toPersianDigit = (replaceString) => {
    var replace = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    var find = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var regex;
    for (var i = 0; i < find.length; i++) {
        regex = new RegExp(find[i], "g");
        replaceString = replaceString.replace(regex, replace[i]);
    }
    return replaceString;
}
const CheckPercentageNumber = (input) => {
    if (parseInt(input.val()) > 100) input.val('100')
    if (parseInt(input.val()) < 0) input.val('0')
}

$("input[data-type='currency'],input.currency").on({
    keyup: function (e) {
        formatCurrency($(this), event);
    },
    blur: function (e) {
        formatCurrency($(this), event);
    }
}).each(function (e) {
    formatCurrency($(this), event);
});

function formatNumber(n) {
    // format number 1000000 to 1,234,567
    return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

function deFormatNumber(n) {
    // format number 1000000 to 1,234,567
    return n.replace(/\D/g, "").replace(",", "")
}

const dateToPersianString = (date) => {
    date = toEnglishDigit(date);
    let dates = date.split('/');
    date = `${dates[2]} ${persianMonth[dates[1] - 1]} ${dates[0]}`
    return date
}

function formatCurrency(input, event) {
    let key
    let input_val
    if (event) {
        key = event.keyCode || event.charCode;
        if (key == 8 || key == 46) {
            $(input).val($(input).val().replace(/[^0-9.]/g, "").slice(0, -1))
        }
    }
    input_val = input.val();
    if (input_val === "") {
        return;
    }
    var original_len = input_val.length;
    var caret_pos = input.prop("selectionStart");
    if (input_val.indexOf(".") >= 0) {
        var decimal_pos = input_val.indexOf(".");
        var left_side = input_val.substring(0, decimal_pos);
        var right_side = input_val.substring(decimal_pos);
        left_side = formatNumber(left_side);
        right_side = formatNumber(right_side);
        right_side = right_side.substring(0, 2);
        input_val = left_side + badiConfig.currency_append;

    } else {
        input_val = formatNumber(input_val);
        input_val = input_val + badiConfig.currency_append;
    }
    input.val(input_val);
    var updated_len = input_val.length;
    caret_pos = updated_len - original_len + caret_pos;
    input[0].setSelectionRange(caret_pos, caret_pos);
}

const regexFA = /^[پچجحخهعغفقثصضشسیبلاتنمآکگوئدذرزطظژؤإأءًٌٍَُِّ\s\n\r\t\d\(\)\[\]\{\}.,،;\-؛]+$/;
const regexValidFloat = /^\d+\.\d{2}$/;
const persianRegaxText = 'فقط حروف فارسی وارد شود!';
const numberFloatRegaxText = 'با دو رقم وارد شود مثال: 19.00';
const persianRegax = {
    regexp: regexFA,
    message: persianRegaxText
};
const numberFloatRegax = {
    regexp: regexValidFloat,
    message: numberFloatRegaxText
};
const UsernameRegax = /^[a-zA-Z0-9_.-]+$/;
const notEmpty = {
    message: 'این فیلد الزامی است!'
};
const between_validation = (start, end) => {
    return {
        min: start,
        max: end,
        message: ' این فیلد باید بین ' + start + ' تا ' + end + ' کاراکتر باشد!'
    }
}
const JustPersian = (input) => {
    if (input.val() != '') {
        if (!regexFA.test(input.val())) {
            input.val("");
        }
    }
}
const loadingFormENABLE = (querySelector = 'form', buttons = [], relative = false, size = null) => {
    if (document.querySelector(querySelector)) {
        document.querySelector(querySelector).parentElement.classList.add('loading');
        if (size)
            document.querySelector(querySelector).parentElement.classList.add('loading-sm');
        if (relative)
            document.querySelector(querySelector).parentElement.classList.add('position-relative');
        for (const btn of buttons)
            document.querySelector(btn).disabled = true
    }
};
const loadingFormDISABLE = (querySelector = 'form', buttons = [], relative = false) => {
    if (document.querySelector(querySelector)) {

        document.querySelector(querySelector).parentElement.classList.remove("loading");
        document.querySelector(querySelector).parentElement.classList.remove('loading-sm');
        for (const btn of buttons)
            document.querySelector(btn).disabled = false
    }
};
$('form').on("submit", function (e) {
    $(this).find('button[type=submit]').addClass('spinner spinner-white spinner-right');
    // $('form').find('input,select,textarea,button').addClass('disabled').prop('readonly', true);
});
const date_picker_config = {
    altFormat: 'X',
    calendarType: 'persian',
    initialValueType: 'gregorian',
    persianDigit: false,
    format: 'YYYY/MM/D',
    observer: true,
    initialValue: true,
    timePicker: {
        enabled: false
    },
    toolbox: {
        calendarSwitch: {
            enabled: false
        }
    },
    onSelect: function (e) {
        let input_date = $(this.model.input.elem)
        if (!valid_persian_date.test(toEnglishDigit(input_date.val()))) {
            swalFireError('تاریخ وارد شده صحیح نمی باشد')
            $(input_date).val('')
            $(input_date).removeClass('is-valid')
            $(input_date).addClass('is-invalid')
        } else {
            $(input_date).addClass('is-valid')
            $(input_date).removeClass('is-invalid')
        }
        $('.datepicker-plot-area td span').click(function (e) {
            $('.datepicker-plot-area').parent().addClass('pwt-hide')
        });
    }
};
const datetime_picker_config = {
    altFormat: 'X',
    calendarType: 'persian',
    initialValueType: 'gregorian',
    persianDigit: false,
    format: 'YYYY/MM/D HH:mm:ss',
    observer: true,
    initialValue: true,
    timePicker: {
        enabled: true
    },
    toolbox: {
        calendarSwitch: {
            enabled: false
        }
    },
    onSelect: function (e) {
        let input_date = $(this.model.input.elem)
        if (!valid_persian_datetime.test(toEnglishDigit(input_date.val()))) {
            swalFireError('تاریخ وارد شده صحیح نمی باشد')
            $(input_date).val('')
            $(input_date).removeClass('is-valid')
            $(input_date).addClass('is-invalid')
        } else {
            $(input_date).addClass('is-valid')
            $(input_date).removeClass('is-invalid')
        }
        $('.datepicker-plot-area td span').click(function (e) {
            $('.datepicker-plot-area').parent().addClass('pwt-hide')
        });
    }
};
if (badiConfig.calendar_date_active)
    if (document.querySelector('.date'))
        $('.date').change(function (e) {
                let input_date = $(this)
                if (!valid_persian_date.test(toEnglishDigit(input_date.val()))) {
                    swalFireError('تاریخ وارد شده صحیح نمی باشد')
                    input_date.val('')
                    input_date.removeClass('is-valid')
                    input_date.addClass('is-invalid')
                } else {
                    input_date.addClass('is-valid')
                    input_date.removeClass('is-invalid')
                }
            }
        ).persianDatepicker(date_picker_config);
if (badiConfig.calendar_datetime_active)
    if (document.querySelector('.date-time'))
        $('.date-time').change(function (e) {
                let input_date = $(this)
                if (!valid_persian_datetime.test(toEnglishDigit(input_date.val()))) {
                    swalFireError('تاریخ وارد شده صحیح نمی باشد')
                    input_date.val('')
                    input_date.removeClass('is-valid')
                    input_date.addClass('is-invalid')
                } else {
                    input_date.addClass('is-valid')
                    input_date.removeClass('is-invalid')
                }
            }
        ).persianDatepicker(datetime_picker_config);
$('.datepicker-plot-area td span').click(function (e) {
    $('.datepicker-plot-area').parent().addClass('pwt-hide')
});
const spinnerButtonON = (qs) => {
    if (qs.type === 'checkbox') {
        qs.parentElement.classList.add('opacity-30')
        $(qs).parent().parent().addClass('spinner spinner-white spinner-right')
        qs.disabled = true;
    } else
        $(qs).addClass('spinner spinner-white spinner-right').prop("disabled", true)
};
const spinnerButtonOFF = (qs) => {
    if (qs.type === 'checkbox') {
        qs.parentElement.classList.remove('opacity-30')
        $(qs).parent().parent().removeClass('spinner spinner-white spinner-right')
        qs.disabled = false;
    } else
        $(qs).removeClass('spinner spinner-white spinner-right disabled').prop("disabled", false)
};
$('form a').click(function (e) {
    if (!$(this).attr("href").startsWith('#'))
        $(this).addClass('spinner spinner-white spinner-right');
});

$('form input[required]:not([type="checkbox"]):not([type="hidden"]):not([type="hidden"]),form select[required],form textarea[required]').parent().append(`<span class="form-text d-none text-muted"> الزامی </span>`);
$('form input:not([type="checkbox"]):not(:required):not([type="hidden"]),form select:not(:required),form textarea:not(:required)').parent().append(`<span class="form-text d-none text-muted"> اختیاری </span>`);
$('.no-form-text span.form-text.text-muted').remove();
$('span.form-text.text-muted').removeClass('d-none');
const toastrFireError = (desc = 'مشکلی پیش آمده است.') => {
    toastr.error(desc);
};
const toastrFireSuccess = (desc = 'با موفقیت انجام شد.') => {
    toastr.success(desc);
};
$('form:not(.filters):not([data-filter])').parent().prepend(`<div class="precustom-loader"><div class="custom-loader"></div></div>`)
$.fn.select2.defaults.defaults.language['searching'] = () => badiConfig.select2_searching_text
$.fn.select2.defaults.defaults.language['noResults'] = () => badiConfig.select2_no_result_text


function removeItemAll(arr, value) {
    var i = 0;
    while (i < arr.length) {
        if (arr[i] === value) {
            arr.splice(i, 1);
        } else {
            ++i;
        }
    }
    return arr;
}

const tableToExcel = (function () {
    let uri = 'data:application/vnd.ms-excel;base64,'
        ,
        template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/><x:DisplayRightToLeft/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        }
        , format = function (s, c) {
            return s.replace(/{(\w+)}/g, function (m, p) {
                return c[p];
            })
        }
    return function (table, name, filename) {
        if (!table.nodeType) table = document.getElementById(table)
        let ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
        window.open(uri + base64(format(template, ctx)));
    }
})();
const getUrlPk = () => location.pathname.split('/')[location.pathname.split('/').length - 1];


const toEnglishDate = (value) => {
    if (value.length > 5) {
        let dateSplit = toEnglishDigit(value).split("/"),
            jD = JalaliDate.jalaliToGregorian(dateSplit[0], dateSplit[1], dateSplit[2])
        return jD[0] + "-" + jD[1] + "-" + jD[2];
    } else {
        return null;
    }
};


JalaliDate = {
    g_days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    j_days_in_month: [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
};

JalaliDate.jalaliToGregorian = function (j_y, j_m, j_d) {
    j_y = parseInt(j_y);
    j_m = parseInt(j_m);
    j_d = parseInt(j_d);
    var jy = j_y - 979;
    var jm = j_m - 1;
    var jd = j_d - 1;

    var j_day_no = 365 * jy + parseInt(jy / 33) * 8 + parseInt((jy % 33 + 3) / 4);
    for (var i = 0; i < jm; ++i) j_day_no += JalaliDate.j_days_in_month[i];

    j_day_no += jd;

    var g_day_no = j_day_no + 79;

    var gy = 1600 + 400 * parseInt(g_day_no / 146097); /* 146097 = 365*400 + 400/4 - 400/100 + 400/400 */
    g_day_no = g_day_no % 146097;

    var leap = true;
    if (g_day_no >= 36525) /* 36525 = 365*100 + 100/4 */
    {
        g_day_no--;
        gy += 100 * parseInt(g_day_no / 36524); /* 36524 = 365*100 + 100/4 - 100/100 */
        g_day_no = g_day_no % 36524;

        if (g_day_no >= 365) g_day_no++;
        else leap = false;
    }

    gy += 4 * parseInt(g_day_no / 1461); /* 1461 = 365*4 + 4/4 */
    g_day_no %= 1461;

    if (g_day_no >= 366) {
        leap = false;

        g_day_no--;
        gy += parseInt(g_day_no / 365);
        g_day_no = g_day_no % 365;
    }

    for (var i = 0; g_day_no >= JalaliDate.g_days_in_month[i] + (i == 1 && leap); i++)
        g_day_no -= JalaliDate.g_days_in_month[i] + (i == 1 && leap);
    var gm = i + 1;
    var gd = g_day_no + 1;

    gm = gm < 10 ? "0" + gm : gm;
    gd = gd < 10 ? "0" + gd : gd;

    return [gy, gm, gd];
};

const clockPicker = (inputSelectors, title = undefined, defaultValue = undefined) => {
    for (const inputSelector of document.querySelectorAll(inputSelectors)) {
        $(inputSelector).attr('autocomplete', 'off');
        const configThis = () => {
            if ($(inputSelector).val() || (!defaultValue && defaultValue !== false))
                defaultValue = $(inputSelector).val();
            let hour = '0', minute = '0', defaultList = [];
            if (defaultValue && defaultValue.includes(':')) {
                defaultList = defaultValue.split(':')
                if (defaultList.length === 2) {
                    hour = defaultList[0];
                    minute = defaultList[1];
                }
            }
            if (!title)
                title = $(inputSelector).parent().parent().find('label').html();
            const refreshTime = () => {
                $('#modal_timepicker .hour-shower').html(10 > parseInt(hour) ? ('0' + parseInt(hour)) : hour);
                $('#modal_timepicker .minute-shower').html(10 > parseInt(minute) ? ('0' + parseInt(minute)) : minute);
            };
            $('body').append(`
    <div class="modal fade" id="modal_timepicker" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content border-modal">
                <div class="modal-header bg-primary">
                    <h5 class="modal-title text-white">${title}</h5>
                </div>
                <div class="modal-body py-0">
                    <div class="d-flex justify-content-around text-center">
                        <h1 class="display-1 w-25 increase-minute">
                            <i class="fa icon-2x cursor-pointer fa-angle-up text-hover-primary"></i>
                        </h1>
                        <h1 class="w-25">
                        </h1>
                        <h1 class="display-1 w-25 increase-hour">
                            <i class="fa icon-2x cursor-pointer fa-angle-up text-hover-primary"></i>
                        </h1>
                    </div>
                    <div class="d-flex justify-content-around text-center">
                        <h1 class="display-1 minute-shower w-25"></span>
                        <h1 class="display-1 w-25">:</span>
                        <h1 class="display-1 hour-shower w-25"></span>
                    </div>
                    <div class="d-flex justify-content-around text-center">
                        <h1 class="display-1 w-25 reduce-minute">
                            <i class="fa icon-2x cursor-pointer fa-angle-down text-hover-primary"></i>
                        </h1>
                        <h1 class="w-25">
                        </h1>
                        <h1 class="display-1 w-25 reduce-hour">
                            <i class="fa icon-2x cursor-pointer fa-angle-down text-hover-primary"></i>
                        </h1>
                    </div>
                </div>
                <div class="modal-footer p-1">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">انصراف
                    </button>
                    <button type="button" class="btn btn-primary">تایید</button>
                </div>
            </div>
        </div>
    </div>
        `);
            let $modalTimePicker = $('#modal_timepicker');
            refreshTime();
            $modalTimePicker.modal('show');
            $modalTimePicker.find('.btn-primary').off().click(function (e) {
                $(inputSelector).val(`${10 > parseInt(hour) ? ('0' + parseInt(hour)) : hour}:${10 > parseInt(minute) ? ('0' + parseInt(minute)) : minute}`);
                $('#modal_timepicker').modal('hide');
            });
            $modalTimePicker.find('.increase-hour').click(function (e) {
                hour = (parseInt(hour) + 1) % 24;
                refreshTime();
            });
            $modalTimePicker.find('.increase-minute').click(function (e) {
                minute = (parseInt(minute) + 5) % 60;
                refreshTime();
            });
            $modalTimePicker.find('.reduce-hour').click(function (e) {
                hour = (parseInt(hour) - 1) % 24;
                if (hour < 0) {
                    hour = 23
                }
                refreshTime();
            });
            $modalTimePicker.find('.reduce-minute').click(function (e) {
                minute = (parseInt(minute) - 5) % 60;
                if (minute < 0) {
                    minute = 55
                }
                refreshTime();
            })
        }
        if ($(inputSelector).parent().hasClass('input-group')) {
            $($(inputSelector).parent().find('.input-group-prepend')).click(function (e) {
                configThis()
            })
        } else
            $(inputSelector).click(function (e) {
                configThis()
            })

    }
};
$(document).ready(function () {
    if (badiConfig.clock_picker_active)
        clockPicker('.time');
});
const setProgress = (qs = '.progress-upload', percent, uploaded, total) => {
    $(qs).removeClass('fade');
    if (total > 1000) {
        $(qs).find('.progress-uploaded').html(parseInt(uploaded));
        $(qs).find('.progress > div').width(percent + '%');
        $(qs).find('.progress-upload-total').html(parseInt(total));
        $(qs).find('.progress-percent').html(percent);
    }
};
$(`.menu-item a[href="${CURRENT_URL}"]`).addClass('active').parent().addClass('menu-item-active')
$(`a.nav-link[href="${CURRENT_URL}"]`).addClass('active')
$('input[data-show]').change(function () {
    let $target = $($(this).attr('data-show'));
    $target.toggleClass('d-none')
    if ($target.attr('data-clear'))
        $target.find('input,select,textarea').val('').change()
})

function convertToSlug(titleStr) {
    titleStr = titleStr.replace(/^\s+|\s+$/g, '');
    titleStr = titleStr.toLowerCase();
    titleStr = titleStr.replace(/[^a-z0-9_\s-ءاأإآؤئبتثجحخدذرزسشصضطظعغفقكلمنهويةى]#u/g, '')
        .replace('»', '').replace('«', '').replace(':', '').replace(',', '').replace('‌', '-')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-');
    return titleStr;
}

function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // IE specific code path to prevent textarea being shown while dialog is visible.
        return clipboardData.setData("Text", text);

    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in MS Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

const copyText = (value) => {
    const result = copyToClipboard(value);
    if (result)
        toastrFireSuccess('به کلیپ بورد کپی شد')
}