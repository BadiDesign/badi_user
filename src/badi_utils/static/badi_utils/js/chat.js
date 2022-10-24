const app = new Vue({
    delimiters: ['[[', ']]'],
    data() {
        return {
            loading: true,
            messages: [],
            tickt: {}
        }
    },
    el: '#vue-selector',
    created: function (e) {
        this.getMessages()
    },
    mounted: function () {

    },
    methods: {
        getMessages() {
            this.loading = true;
            ApiAjaxReader({
                url: MESSAGES_API_URL + 'ticket/' + getUrlPk(),
                method: 'GET',
                success: (data) => {
                    console.log(data)
                    this.messages = data.response;
                    this.loading = false;
                    this.tickt = data.ticket;
                },
                error: function (e) {
                    swalFireError();
                }
            })
        },
        sendMessage() {
            const pk = document.getElementById('id_tickt').value;
            this.loading = true;
            ApiAjax({
                url: MESSAGES_API_URL,
                method: 'POST',
                file: true,
                success_message: 'با موفقیت ارسال شد',
                success: (data) => {
                    document.getElementById('id_tickt').value = pk;
                    this.getMessages()
                },
                error: function (e) {
                    swalFireError();
                }
            })
        },
        get(val) {
            if (val === true) {
                return 'بله'
            } else {
                return 'خیر'
            }
        },
        get_list(lis, key) {
            if (lis[key]) {
                return lis[key]
            } else {
                return 'ثبت نشده'
            }
        },
        m2m(lis) {
            let res = '';
            if (lis) {
                for (const obj in lis) {
                    res += lis[obj].title + ' - '
                }
                res = res.slice(0, -3);
                return res
            }
        },
    },
    computed: {}
})
