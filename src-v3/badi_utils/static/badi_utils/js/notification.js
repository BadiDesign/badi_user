const vueNotifApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#notification-vue',
    data() {
        return {
            notifications: [],
        }
    },
    created: function () {
        this.getNotifications();
    },
    methods: {
        getNotifications: function () {
            ApiAjaxReader({
                url: NOTIFICATION_SELF_API_URL,
                method: 'GET',
                success_message: false,
                success: (res) => {
                    this.notifications = res
                }
            })
        },
        seenNotif: function (notif) {
            ApiAjaxReader({
                method: 'GET',
                url: NOTIFICATION_SEEN_API_URL,
                pk: notif.id,
                success_message: 'Done Successfully',
                success: () => {
                    this.getNotifications()
                },
            });
        },
    },
});
