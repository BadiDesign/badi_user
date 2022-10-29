const defaultLoader = `<div class="precustom-loader"><div class="custom-loader"></div></div>`;
window.data_table_cool_options = {
    columnDefs: [
        {className: "text-center", targets: "_all"},
    ],
    "aaSorting": [],
    'paging': true,
    'lengthChange': false,
    'searching': false,
    'ordering': true,
    "pageLength": localStorage.getItem('pageLength') ? localStorage.getItem('pageLength') : 25,
    'info': true,
    'autoWidth': true,
    'responsive': false,
    'oLanguage': badiConfig["datatable__oLanguage"]
};
var raw_data_table_cool_options = JSON.parse(JSON.stringify(window.data_table_cool_options));
window.getData = function (oTable, ele) {
    return oTable.row(ele.closest('tr')).data()
};
window.getId = function (oTable, ele) {
    return getData(oTable, ele)[0]
};

window.datatable_simple_show = function (options, settings) {
    let searchForm = options['filterForm'] || '.filters';
    if (options['api_url']) {
        options['url'] = options['url'] || (options['api_url'] + 'datatable/')
        options['up_url'] = options['up_url'] || 'update/0'
        options['del_url'] = options['del_url'] || (options['api_url'] + '0')
    }
    if (!settings)
        settings = {};

    let window_options = $.extend(true, {}, window.data_table_cool_options, settings);
    window_options["processing"] = true;
    window_options["serverSide"] = true;
    // url which we get table's data from
    window_options["ajax"] = {
        url: options['url'],
        method: 'POST',
        'beforeSend': (request) => request.setRequestHeader("Authorization", localStorage.getItem('session_key')),
        data: function (d) {
            if (!options['disable_search'])
                $(`${searchForm} input, ${searchForm} select`).each(function (i, e) {
                    d[e.getAttribute('name')] = $(e).val();
                })
            if (options['extra_filters'])
                options['extra_filters'](d);
            // console.log(d);
        },
    };
    if (!options['no_error']) {
        window_options["ajax"]['error'] = function (xhr, error, code) {
            checkToken(xhr, (tokenStatus) => {
                if (tokenStatus === true) {
                    oTable.draw(false);
                } else {
                    console.error('UNKNOWN ERROR Backend RES :', xhr);
                    console.log('tokenStatus:', tokenStatus)
                }
            });
        }
    }
    // add a column to overall columns so we can have delete and edit buttons
    window_options["columns"] = [];
    let do_not_order = options["do_not_order"] ? options["do_not_order"] : [];
    for (let i = 0; i < options['real_cols']; i++) {
        defaulta = {
            className: "text-center",
        };
        if (options['this_column_data']) {
            options['this_column_data'](i, defaulta);
        }
        if (do_not_order.includes(i)) {
            defaulta['orderable'] = false;
        }
        window_options["columns"].push(defaulta);
    }
    let extra_buttons = options["ex_buttons"] ? options["ex_buttons"] : "";
    let delete_text = options['delete_text'] ? options['delete_text'] : "Delete";
    let edit_text = options['edit_text'] ? options['edit_text'] : "edit";
    if (!options["no_action_nutton"]) {
        let buttons = '';
        if (!options["not_edit_able"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="edit" class="btn btn-sm btn-light-primary btn-hover-text-primary btn-icon mx-2 edit_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M12.2674799,18.2323597 L12.0084872,5.45852451 C12.0004303,5.06114792 12.1504154,4.6768183 12.4255037,4.38993949 L15.0030167,1.70195304 L17.5910752,4.40093695 C17.8599071,4.6812911 18.0095067,5.05499603 18.0083938,5.44341307 L17.9718262,18.2062508 C17.9694575,19.0329966 17.2985816,19.701953 16.4718324,19.701953 L13.7671717,19.701953 C12.9505952,19.701953 12.2840328,19.0487684 12.2674799,18.2323597 Z" fill="#000000" fill-rule="nonzero" transform="translate(14.701953, 10.701953) rotate(-135.000000) translate(-14.701953, -10.701953) "></path><path d="M12.9,2 C13.4522847,2 13.9,2.44771525 13.9,3 C13.9,3.55228475 13.4522847,4 12.9,4 L6,4 C4.8954305,4 4,4.8954305 4,6 L4,18 C4,19.1045695 4.8954305,20 6,20 L18,20 C19.1045695,20 20,19.1045695 20,18 L20,13 C20,12.4477153 20.4477153,12 21,12 C21.5522847,12 22,12.4477153 22,13 L22,18 C22,20.209139 20.209139,22 18,22 L6,22 C3.790861,22 2,20.209139 2,18 L2,6 C2,3.790861 3.790861,2 6,2 L12.9,2 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"></path></g></svg></span></button>';
        }
        if (!options["not_delete_able"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete"  class="btn btn-sm btn-light-primary btn-hover-text-primary btn-icon delete_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"></path><path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"></path></g></svg></span></button>';
        }
        window_options["columns"].push(
            {
                data: null,
                className: "text-center",
                orderable: false,
                defaultContent: extra_buttons + buttons
            });

        if (!options["no_loading"]) {
            $(options['datable_id']).parent().prepend(defaultLoader)
        }
    }
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
    if (!window_options["columnDefs"])
        window_options["columnDefs"] = [];
    if (!options['show_id']) {
        window_options["columnDefs"].push({
            "targets": [0],
            "visible": false,
            "searchable": false
        });
    }
    // create datatable
    var oTable = $(options['datable_id']).DataTable(window_options);
    // a returns id of a column
    if (!options["no_action_nutton"]) {
        var action_url = options['ac_url'];
        var delete_url = options['del_url'];
        delete_url = delete_url.substr(0, delete_url.length - 1);
    }
    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {
        // edit button
        $('.filters button.spinner').removeClass('spinner spinner-white spinner-right spinner-left')
        if (!options["no_loading"]) {
            loadingFormDISABLE(`.loading-1-custom`, [], true)
        }
        $(options['datable_id'] + " " + '.edit_button').on('click', function (e) {
            if (!options["no_loading"]) {
                loadingFormENABLE(`.loading-1-custom`, [], true)
            }
            e.preventDefault();
            var id = getId(oTable, $(this));
            window.location.href = options['up_url'] + id;
        });
        // action button
        $(options['datable_id'] + " " + '.action_button').on('click', function (e) {

            if (!options["no_loading"]) {
                loadingFormENABLE(`.loading-1-custom`, [], true)
            }
            e.preventDefault();

            var id = getId(oTable, $(this));
            window.location.href = action_url + id;

        });
        // delete button
        if (options['do_before_initializing']) {
            options['do_before_initializing'](oTable);
        }
        $('.dataTables_filter').parent().parent().addClass('modal-header').css({
            "margin-left": "0px",
            "margin-right": "0px"
        });
        $('.dataTables_filter input').parent().parent().parent().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6')
            .siblings().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6');
        $(options['datable_id'] + " " + '.delete_button').on('click', function (e) {
            e.preventDefault();
            var id = getId(oTable, $(this));
            var deleting_process = function (callback) {
                if (options['extra_del_params']) {
                    if (!options['disable_extra_del_params']) {
                        $.ajax(delete_url + id, {
                            method: 'delete',
                            headers: {
                                "Authorization": localStorage.getItem('session_key')
                            },
                            error: (options['deleteError']) ? options['deleteError'] : () => {
                                swalFireError('قابل Delete نمی باشد!')
                            }
                        }).done(function (res) {
                            oTable.draw();
                            if (callback) callback();
                        });
                        return
                    }
                }
                if (callback) callback();
                window.location.href = delete_url + id;
            };
            if (options["modal_id"]) {
                $(options["modal_id"]).modal('show');
                $(options['modal_id'] + " " + '.yes_button').click(function () {
                    $(options["modal_id"]).modal('toggle');
                    deleting_process()
                });
            } else {
                swal.fire({
                    title: 'Are you sure?',
                    text: "Record will lose after Delete !",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Yes! delete it',
                    cancelButtonText: 'No',

                }).then(function (result) {
                    if (result.value) {
                        deleting_process(function () {
                            toastr.success('Record deleted successfully.')
                        });
                    }
                });
            }
        });
        $(options['datable_id'] + " " + '.load-form').on('click', function (e) {
            e.preventDefault();
            if (options["no_loading"]) {
                $(options['datable_id']).parent().prepend(defaultLoader)
            }
            loadingFormENABLE(`.loading-1-custom`, [], true)
        });
        if (!options['hide_loading_all'])
            $(options['datable_id'] + " " + '.btn:not(.delete_button)').on('click', function (e) {
                if (!document.querySelector('.loading-1-custom')) {
                    $(options['datable_id']).parent().prepend(defaultLoader)
                }
                loadingFormENABLE(`.loading-1-custom`, [], true)
            });

    });

    var timer = null;
    var last_input = null;

    function searcher(type) {
        return function (e) {
            clearTimeout(timer);
            if (last_input !== e.target.value) {
                if (!type)
                    setTimeout(function () {
                        oTable.search(e.target.value);
                        oTable.draw();
                    }, 800);
                else {
                    setTimeout(function () {
                        oTable.search(e.target.value);
                        oTable.draw();
                    }, 35);
                }
            }
        };
    };
    $(options['datable_id'] + '_wrapper input[type="search"]').off().on('keyup', searcher(false))
        .on('click', searcher(true));
    if (options['after_init']) {
        options['after_init'](oTable, options);
    }
    return $.extend(oTable, {
        getId: function (e) {
            return window.getId(oTable, e)
        },
        getData: function (e) {
            return window.getData(oTable, e)
        }
    });
};
let allText = {}

function minimizeText(row, data, id, query = id - 1, sub = 27, classText = "") {
    if (data[id].length > sub + 3) {
        if (!allText[query]) {
            allText[query] = {}
        }
        allText[query][data[0]] = data[id];
        var tdEq = 'td:eq(' + query + ')';
        return $(tdEq, row).html('<span class="' + classText + '" type="button" onclick="showTextMini(' + data[0] + ',' + query + ')" class="text-center">' + data[id].substring(0, sub) + '...' + '</span>')
    } else return null
}


function showTextMini(id, query) {
    swal.fire({
        title: "Full Text:",
        html: allText[query][id],
        confirmButtonText: 'close',
    });
    $('.swal2-popup').css('min-width', '400px')
}

const naviItem = (text = '', icon = '', extraClass = '', href = '#') => {
    return `<li class="navi-item"><a href="${href}" class="navi-link ${extraClass}"><span class="navi-icon"><i class="${icon}"></i></span><span class="navi-text">${text}</span></a></li>`
};

const boldCol = (query, row, data, color = 'primary') => {
    let arg = 'td:eq(' + query + ')';
    try {
        if (isNaN(data[0])) data = data[0].toUpperCase() + data.slice(1);
    } catch (e) {
    }
    return $(arg, row).html(`<div class="font-weight-bolder text-${color} mb-0"> ${data}</div>`);
};
const breakCol = (query, row, data) => {
    return $('td:eq(' + query + ')', row).html(`<div class="break-spaces min-w-200px"> ${data}</div>`);
};
const bolderCol = (query, row, data) => {
    let arg = 'td:eq(' + query + ')';
    return $(arg, row).html(`<div class="font-weight-bolder mb-0"> ${data}</div>`);
};
const dynamic_switch = `<span class="switch switch-outline switch-icon switch-primary"> <label class="m-auto">  <input type="checkbox" name="select"/>  <span></span> </label></span>`;

function switch_ajax(url, pk, table) {
    ApiAjax({
        url: url,
        pk,
        method: 'PUT',
        success: function (result) {
            swalFireSuccess(result.message);
            table.draw()
        },
        error: function (result) {
            swalFireError();
            table.draw()
        }

    });
}

const defaultDrawCallBack = (row, data, table = {}) => {
    for (let value in data) {
        if (data[value]) {
            data[value] = data[value].toString();
            if (data[value].startsWith('switch-')) {
                const switch_data = data[value].split('-');
                var elem = data[value];
                if (switch_data[1] === 'true') {
                    elem = $(dynamic_switch).clone();
                    elem.find('input').prop('checked', true)
                } else if (switch_data[1] === 'false')
                    elem = elem = $(dynamic_switch).clone();
                if (switch_data[2] === 'none')
                    elem.find('input').prop('disabled', true)
                else
                    elem.change(function () {
                        switch_ajax(switch_data[2], data[0], table)
                    });

                $(`td:eq(${value - 1})`, row).html('');
                $(`td:eq(${value - 1})`, row).append(elem);

            } else if (data[value] === "bool-true")
                $(`td:eq(${value - 1})`, row).html(`<label class="label label-xl label-success"><i class="fa text-white fa-check"></i></label>`)
            else if (data[value] === "bool-false")
                $(`td:eq(${value - 1})`, row).html(`<label class="label label-xl label-danger"><i class="fa text-white fa-times"></i></label>`)
            else if (data[value] === "file-null")
                $(`td:eq(${value - 1})`, row).html(`<label class="label label-xl my-4 label-white label-inline">None</label>`)
            else if (data[value].startsWith('/media/')) {
                let split = data[value].split('.');
                let splitElement = split[split.length - 1];
                if (splitElement.isInList('png', 'jpeg', 'jpg', 'webp', 'jfif')) {
                    $(`td:eq(${value - 1})`, row).html(`
                         <a href="#" class="symbol symbol-50 flex-shrink-0">
                              <img src="${data[value]}" class="symbol-datatable" title="" alt=""/>
                         </a>
                    `)
                } else {
                    $(`td:eq(${value - 1})`, row).html(`<a download href="${data[value]}" class="btn btn-primary btn-circle btn-icon btn-sm" title="جهت دریافت فایل کلیک کنید"><i class="fa fa-download"></i></a>`)
                }
            } else {
                $(`td:eq(${value - 1}):not(:last-child)`, row).html(data[value])
            }
        }
    }
};
const makeDatatableProfile = (key, row, table_id, picture, header = '', body = '') => {
    $(`${table_id} th:eq(${key})`).addClass("w-250px").html('')
    let picture_div = ''
    if (!picture || picture === 'file-null') {
        picture_div = `
    <span class="symbol symbol-lg-50 symbol-25 symbol-light-primary">
        <span class="symbol-label text-uppercase">${header[0]}</span>
    </span>`;
    } else {
        picture_div = `
    <span class="symbol symbol-lg-50 symbol-25 symbol-light-primary">
        <span class="symbol-label datatable-symbol" style="background: url(${picture});"></span>
    </span>`;
    }
    $(`td:eq(${key})`, row).html(`
<div class="d-flex">
    ${picture_div}
    <div class="datatable-symbol-info px-3">
        <span class="text-primary font-weight-bolder font-size-h6">${header}</span>
        <span class="text-primary opacity-50 font-weight-bolder font-size-md">${body}</span>
    </div>
</div>
`)
}