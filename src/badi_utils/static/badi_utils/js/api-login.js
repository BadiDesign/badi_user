const message_url = (text) => {
    return '?message_text={' + text + '}'
};
const go_to_login = (msg = '') => {
    if (msg !== '')
        msg = '?error=' + msg;
    document.querySelector('body').classList.add('loading');
    window.open(LOGIN_URL + msg, '_self');
};

if (CURRENT_URL.includes('message_text={')) {
    const message = CURRENT_URL.split('message_text={')[1].split('}')[0]
    if (message.length > 5) {
        toastr.success(decodeURI(message));
        window.history.replaceState('Object', 'Title', window.location.pathname);
    }
}

const redirect = (url) => {
    bodyLoading();
    window.open(url, '_self');
};

const checkToken = (response, callBack) => {
    if (localStorage.getItem('session_refresh') === null)
        go_to_login();
    else if (response['status'] === 401) {
        $.ajax({
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            url: REFRESH_TOKEN_URL,
            data: JSON.stringify({refresh: localStorage.getItem('session_refresh')}),
            success: function (res) {
                if (response['code']) {
                    localStorage.removeItem('session_key');
                    localStorage.removeItem('session_refresh');
                    go_to_login();
                    callBack(false);
                } else {
                    localStorage.setItem('session_key', 'Bearer ' + res["access"]);
                    callBack(true);
                }
            },
            error: function (res) {
                if (res['status'] === 401) {
                    swalFireError('احراز هویت شما منتقضی شده است لطفا دوباره وارد شوید!');
                    go_to_login();
                }
                console.log('checkTokenError', res);
                swalFireError('مشکلی پیش آمده است لطفا دوباره امتحان کنید!');
                callBack(false);
            }
        });
    } else {
        callBack(response['status']);
    }
};
const getFormData = (qs = 'form') => {
    let res = {}
    for (const inputEl of $(`${qs} input, ${qs} select, ${qs} textarea`)) {
        if (inputEl.type === "checkbox") {
            res[inputEl.name] = inputEl.checked ? 'on' : 'off'
        } else if (inputEl.classList.contains('date')) {
            res[inputEl.name] = toEnglishDate($(inputEl).val())
        } else if (inputEl.classList.contains('currency')) {
            res[inputEl.name] = deFormatNumber($(inputEl).val())
        } else if (inputEl.type === "file") {
            res[inputEl.name] = inputEl.files ? inputEl.files[0] : {}
        } else {
            const inputName = inputEl.name;
            res[inputName] = $(inputEl).val()
        }
    }
    return res;
}

const getFormDataWithFile = (qs = 'form') => {
    let res = new FormData(document.querySelector(qs));
    for (const inputEl of $(`${qs} input, ${qs} select, ${qs} textarea`)) {
        if (inputEl.type === "file") {
            res.delete(inputEl.name)
            let files = inputEl.files;

            if (files.length > 0) {
                for (const f in files)
                    res.append(inputEl.name, files[f]);
            }
            if (document.querySelector(`input[name="${inputEl.name}_delete"]`)) {
                if (document.querySelector(`input[name="${inputEl.name}_delete"]`).checked === true) {
                    res.delete(inputEl.name);
                    res.append(inputEl.name, '');
                }
            }
        }
        if (inputEl.classList.contains('date')) {
            res.delete(inputEl.name);
            if ($(inputEl).val() !== '')
                res.append(inputEl.name, toEnglishDate($(inputEl).val()))
        } else if (inputEl.classList.contains('currency')) {
            res.delete(inputEl.name);
            res[inputEl.name] = deFormatNumber($(inputEl).val())
        }
    }
    return res;
}

const DisplayFormData = (formData, log = false) => {
    const response = {}
    for (let pair of formData.entries()) {
        if (log)
            console.log(pair[0] + ' : ' + pair[1]);
        response[pair[0]] = pair[1]
    }
    return response;
}

const instanceSetter = (instance, object, titles = {}) => {
    for (const index in object) {
        if (object[index])
            if (typeof object[index] === 'object') {
                if (titles[index]) {
                    instance = instance.replace('{#@' + index + '}', object[index][titles[index]])
                } else if (object[index].title)
                    instance = instance.replace('{#@' + index + '}', object[index].title)
                else
                    console.log(index, 'NOTFOUND')
            } else {
                if (index.endsWith('_date') && (object[index] && object[index] !== '') && object[index].split('-').length === 3) {
                    const this_date = new Date(object[index]).toLocaleDateString('fa-IR');
                    instance = instance.replace('{#@' + index + '}', this_date)
                } else {
                    instance = instance.replace('{#@' + index + '}', object[index]);
                }
            }
    }
    instance = instance.replace(/ +(?= )/g, '');
    for (const word of instance.split(' ')) {
        if (word.startsWith('{#@')) {
            instance = instance.replaceAll(word, 'تعریف نشده!')
        }
    }
    return instance
}

const instanceDataTableSetter = (instance, object, defaults = {}) => {
    for (const index in object) {
        if (object[index])
            instance = instance.replace('#@' + index, object[index])
        else {
            if (defaults[index])
                instance = instance.replace('#@' + index, defaults[index])

        }
    }
    instance = instance.replace(/ +(?= )/g, '');
    for (const word of instance.split(' ')) {
        if (word.startsWith('#@')) {
            instance = instance.replaceAll(word, 'تعریف نشده!')
        }
    }
    return instance
}

const FormShowData = (qs) => {
    const response = {}
    for (let input of $(qs + ' input')) {
        response[input.name] = input.value
    }
    for (let input of $(qs + ' select')) {
        response[input.name] = $(input).find("option:selected").text();
    }
    return response;
}

const formErrorHandler = (listErrors, qs = document) => {
    for (let field_error in listErrors) {
        if (listErrors[field_error] instanceof Array) {
            toastr.error(listErrors[field_error].join('<br>'));
            if (field_error) {
                const errorInput = qs.querySelector(`[name=${field_error}]`);
                if (errorInput) {
                    errorInput.classList.add('is-invalid');
                    errorInput.parentElement.classList.add('has-danger');
                    if (errorInput.parentElement.querySelector('.form-text')) {
                        errorInput.parentElement.querySelector('.form-text').innerHTML = listErrors[field_error].join('<br>');
                        errorInput.parentElement.querySelector('.form-text').classList.add('danger');
                    }
                }
            }
        }
    }
};

const formFiller = (values, qs = document, clearFields = true) => {
    if (clearFields) {
        $(qs).find('select').val('').change();
        $(qs).find('input,textarea').val('');
    }
    for (let field in values) {
        console.log(values)
        const value = values[field];
        const input = qs.querySelector(`[name=${field}]`);
        if (input && value) {
            if (typeof value === 'object') {
                let newOption;
                if (value.title) {
                    newOption = new Option(value.title, value.id, true, true);
                    $(input).append(newOption).trigger('change');
                } else
                    console.log(value, 'INDEX NOT FOUND')
            } else {
                if (field.endsWith('_date') && (value && value !== '') && value.split('-').length === 3) {
                    const this_date = new Date(value);
                    if ($(input).data().datepicker) {
                        console.log(this_date.getTime())
                        $(input).val(this_date.toLocaleDateString('fa-IR'))
                        $(input).data().datepicker.setDate(this_date.getTime());
                    } else
                        $(input).val(this_date.toLocaleDateString('fa-IR'))
                } else
                    try {
                        $(input).val(value)
                    } catch {
                    }
            }
        }
    }
};

const replaceByClass = (data) => {
    for (const i in data) {
        if (data[i])
            if (typeof data[i] === 'object') {
                for (const j in data[i]) {

                    if (data[i][j] && document.querySelector(`.id_${i}__${j}`)) {
                        if (document.querySelector(`.id_${i}__${j}`).nodeName === 'IMG')
                            $(`.id_${i}__${j}`).attr('src', data[i][j]);
                        else
                            $(`.id_${i}__${j}`).html(data[i][j]);
                    } else {
                        if (document.querySelector(`.id_${i}__${j}`)) {
                            document.querySelector(`.id_${i}__${j}`).innerHTML = ''
                        }
                    }
                }
            } else {
                if (document.querySelector(`.id_${i}`))
                    if (document.querySelector(`.id_${i}`).nodeName === 'IMG')
                        $(`.id_${i}`).attr('src', data[i]);
                    else
                        $(`.id_${i}`).html(data[i])
                else {
                    if (document.querySelector(`.id_${i}`)) {
                        document.querySelector(`.id_${i}`).innerHTML = ''
                    }
                }
            }
    }
}


const ApiAjax = (jsonValues) => {
    const api_button = jsonValues['button'];
    const api_modal = jsonValues['modal'];
    const api_table = jsonValues['table'];
    let api_url = jsonValues['url'];
    const api_after_error = jsonValues['error'] ? jsonValues['error'] : (x) => {
    };
    const api_before_error = jsonValues['before_error'] ? jsonValues['before_error'] : (x) => {
    };
    const api_success = jsonValues['success'] ? jsonValues['success'] : (x) => {
    };
    const api_check_data = jsonValues['check'] ? jsonValues['check'] : (x) => x
    let api_data = jsonValues['data'] ? jsonValues['data'] : null;
    let api_token = jsonValues['token'] !== undefined ? jsonValues['token'] : true;
    const api_method = jsonValues['method'] ? jsonValues['method'] : 'GET';
    const api_handler = jsonValues['handler'] ? jsonValues['handler'] : true;
    const api_clearForm = jsonValues['clearForm'] !== undefined ? jsonValues['clearForm'] : true;
    const api_success_message = (jsonValues['success_message'] !== undefined) ? jsonValues['success_message'] : 'Done Successfully!';
    const api_success_url = jsonValues['success_url'];
    const api_extra = jsonValues['extra'];
    const api_form = jsonValues['form'];
    const api_params = jsonValues['params'];
    const api_selector = jsonValues['selector'] ? jsonValues['selector'] : null;
    let api_header = {
        // 'Authorization': localStorage.getItem('session_key'),
        'Content-Type': 'application/json'
    }
    let api_final_data = {};
    const api_pk = jsonValues['pk'];
    let processData = true
    if (api_pk)
        api_url += api_pk + '/';
    if (api_params)
        api_url += api_params;

    if (jsonValues['form']) {
        $(api_form + ' .has-danger').removeClass('has-danger');
        $(api_form + ' .has-success').removeClass('has-success');
        $(api_form + ' .is-valid').removeClass('is-valid');
        $(api_form + ' .is-invalid').removeClass('is-invalid');
    }
    if (!api_data) {
        api_final_data = JSON.stringify(getFormData(api_form))
        if (api_method.toLowerCase() === 'get') {
            api_final_data = new URLSearchParams(JSON.parse(api_final_data)).toString();
        }
    } else
        api_final_data = JSON.stringify(api_data)
    if (api_extra) {
        api_final_data = $.extend(api_final_data, api_extra);
        api_final_data = JSON.stringify(api_final_data)
    }
    if (api_button)
        spinnerButtonON(api_button);
    if (api_selector)
        loadingFormENABLE(api_selector);
    if (jsonValues['file']) {
        processData = false;
        api_header = {
            'Authorization': localStorage.getItem('session_key'),
        }
        api_final_data = getFormDataWithFile(api_form)
    }
    api_final_data = api_check_data(api_final_data)
    $.ajax({
        headers: api_header,
        method: api_method,
        processData: processData,
        contentType: false,
        url: api_url,
        data: api_final_data,
        success: function (res) {
            if (api_clearForm === true) {
                $(api_form ? api_form : 'form').first().find("input:not([type=hidden]), textarea").val("");
                $(api_form ? api_form : 'form').first().find("select").val("").change();
            }
            // if (res['messages'])
            //     if (api_success_url)
            //         redirect(api_success_url + message_url());
            if (api_modal)
                $(api_modal).modal('hide');
            if (api_table)
                api_table.draw(false);
            if (api_success_url)
                redirect(api_success_url + message_url(api_success_message));
            else {
                if (api_button)
                    spinnerButtonOFF(api_button);
                if (api_selector)
                    loadingFormDISABLE(api_selector);
            }
            if (api_success_message)
                toastr.success(api_success_message);

            api_success(res);
        },
        error: function (res) {
            console.log(res)
            api_before_error(res);
            if (api_token)
                checkToken(res, (tokenStatus) => {
                    if (tokenStatus === true) {
                        ApiAjax(jsonValues);
                    } else if (tokenStatus === 400) {
                        if (api_button)
                            spinnerButtonOFF(api_button);
                        if (api_handler)
                            if (!api_data)
                                formErrorHandler(res.responseJSON, api_form ? document.querySelector(api_form) : document.querySelector('form'))

                        if (api_button)
                            spinnerButtonOFF(api_button);
                        if (api_selector)
                            loadingFormDISABLE(api_selector);
                        console.log('api_after_error()');
                        api_after_error(res['responseJSON'])
                    } else if (tokenStatus === 403) {
                        if (api_button)
                            spinnerButtonOFF(api_button);
                        if (api_handler)
                            if (!api_data)
                                formErrorHandler(res.responseJSON, api_form ? document.querySelector(api_form) : document.querySelector('form'))
                        if (api_selector)
                            loadingFormDISABLE(api_selector);
                        if (res.responseJSON['detail'])
                            toastrFireError(res.responseJSON['detail'])
                        api_after_error(res['responseJSON'])


                    } else {
                        console.error('UNKNOWN ERROR Backend RES :', res);
                        console.log('tokenStatus:', tokenStatus)
                        if (api_button)
                            spinnerButtonOFF(api_button);
                        if (api_selector)
                            loadingFormDISABLE(api_selector);
                        api_after_error(res['responseJSON'])
                    }
                });

        }
    }).done(function (e) {
        if (api_button)
            spinnerButtonOFF(api_button);
        if (api_selector)
            loadingFormDISABLE(api_selector);
    });
};


const ApiAjaxReader = (jsonValues) => {
    let api_url = jsonValues['url'];
    const api_after_error = jsonValues['error'] ? jsonValues['error'] : (x) => {
    };
    const api_before_error = jsonValues['before_error'] ? jsonValues['before_error'] : (x) => {
    };
    const api_success = jsonValues['success'] ? jsonValues['success'] : (x) => {
    };
    const api_data = jsonValues['data'] ? jsonValues['data'] : {};
    const api_modal = jsonValues['modal'] ? jsonValues['modal'] : null;
    const api_loading = jsonValues['loading'] ? jsonValues['loading'] : true;
    const api_method = jsonValues['method'] ? jsonValues['method'] : 'GET';
    const api_success_message = jsonValues['success_message'] ? jsonValues['success_message'] : null;
    const api_selector = jsonValues['selector'] ? jsonValues['selector'] : null;
    const api_pk = jsonValues['pk'];
    if (api_pk)
        api_url += api_pk + '/';
    if (api_loading)
        loadingFormENABLE(api_selector, [], true, 'sm')
    $.ajax({
        headers: {
            'Authorization': localStorage.getItem('session_key'),
            'Content-Type': 'application/json'
        },
        timeout: 10000,
        method: api_method,
        url: api_url,
        data: JSON.stringify(api_data),
        success: function (res) {
            if (api_modal) {
                $(api_modal).modal('show');
            }
            if (api_loading)
                loadingFormDISABLE(api_selector)
            if (api_success_message)
                toastr.success(api_success_message);
            api_success(res);
        },
        error: function (res) {
            api_before_error(res);
            checkToken(res, (tokenStatus) => {
                if (tokenStatus === true) {
                    ApiAjaxReader(jsonValues);
                } else {
                    if (api_loading)
                        loadingFormDISABLE(api_selector)
                    if (tokenStatus === 400) {
                        api_after_error(res['responseJSON'])
                    } else {
                        console.error('UNKNOWN ERROR Backend RES :', res);
                        api_after_error(res['responseJSON'])
                    }
                }
            });

        }
    }).done(function (e) {
        if (api_loading)
            loadingFormDISABLE(api_selector)
    });
};
