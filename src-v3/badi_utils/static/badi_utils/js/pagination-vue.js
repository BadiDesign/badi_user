Vue.component('pagination', {
    delimiters: ['[[', ']]'],
    template: '#pagination-template',
    filters: {},
    props: ['count', 'limit', 'current'],
    data() {
        return {
            page_count: 0
        }
    },
    created: function () {
    },
    computed: {
        pageList: function () {
            let pageList = []
            this.page_count = Math.ceil(this.count / this.limit)
            for (let index = 1; index <= 1; index++) {
                if (this.page_count > index - 1) {
                    pageList.push({
                        'number': index,
                        'active': true,
                    })
                }
            }
            {
                let index = this.current - 2
                if (index >= 1 && index <= this.page_count && !pageList.find(x => x.number === index)) {
                    pageList.push({
                        'number': '...',
                        'active': false,
                    })
                }
            }
            for (let index = this.current - 1; index <= this.current + 2; index++) {
                if (this.page_count > index - 1 && index >= 1 && !pageList.find(x => x.number === index)) {
                    pageList.push({
                        'number': index,
                        'active': true,
                    })
                }
            }
            if (!pageList.find(x => x.number === this.page_count - 1) && this.page_count > 1) {
                pageList.push({
                    'number': '...',
                    'active': false,
                })
            }
            if (!pageList.find(x => x.number === this.page_count)) {
                pageList.push({
                    'number': this.page_count,
                    'active': true,
                })
            }
            return pageList
        },
    },
    methods: {
        goPage: function (page) {
            this.$emit('page-changed', {
                'page': page
            })
        },
        isPageActive: function (page) {
            return this.page_count >= page && page >= 1
        },
    },
});