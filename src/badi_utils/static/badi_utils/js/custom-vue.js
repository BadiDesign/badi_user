Vue.filter('toSince', function (value) {
        return timeSince(new Date(value).getTime())
    }
)
Vue.filter('separate', function (value) {
        return Number(value).toLocaleString()
    }
)
Vue.filter('InIran', function (value) {
        return {
            '0': 'none',
            '1': 'rare',
            '2': 'common',
        }[value]
    }
)
Vue.mixin({
    methods: {
        isOnline: function (value) {
            return timeSince(new Date(value).getTime()).includes('seconds')
        }
    }
})
Vue.component('range-slider', {
    props: ['title', 'value', 'property', 'priority', 'editable'],
    data() {
        return {
            max: 5,
            min: 1
        }
    },
    methods: {
        getColorValue: function (val) {
            if (val < 1.5)
                return 'bg-light-danger text-danger border-bottom border-top border-2 border-danger'
            if (val < 3.5)
                return 'bg-light-warning text-warning border-bottom border-top border-2 border-warning'
            return 'bg-light-success text-success border-bottom border-top border-2 border-success'
        }
    },
    computed: {
        getPercentOfLeft: function () {
            return ((this.value - 1) * 100 / (this.max - 1))
        },
        getLeft: function () {
            return `calc(${this.getPercentOfLeft}% - 15px)`
        }
    },
    template: `
    <div class="form-group">
        <div class="d-flex justify-content-between align-items-center">
            <label class="col-form-label font-weight-bolder">{{title}}
            <template v-if="priority && priority !== 1">({{priority}}X)</template>:</label>
            <div class="mr-auto" v-if="editable">
                <button class="btn btn-icon btn-light-warning btn-xs" @click.prevent="$emit('edit', property)">
                    <i class="fa fa-pen"></i>
                </button>
                <button class="btn btn-icon btn-light-danger btn-xs" @click.prevent="$emit('delete', property)">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
        </div>
        <div class="bd-range-bar">
            <div class="p-2 text-muted font-size-xs">{{min}}</div>
            <div class="rounded p-2 bd-range-bar-holder">
             <span class="font-size-lg" :class="[getColorValue(value)]" :style="{left: getLeft}" >
                 <span>{{value.toFixed(1)}}</span>
            </span>
             <span class="text-muted mt-7 top-0" :style="{left: 'calc(' + 25 + '% - 15px)'}" >
                 <span class="font-size-xs">2</span>
            </span>
             <span class="text-muted mt-7 top-0" :style="{left: 'calc(' + 50 + '% - 15px)'}" >
                 <span class="font-size-xs">3</span>
            </span>
             
             <span class="text-muted mt-7 top-0" :style="{left: 'calc(' + 75 + '% - 15px)'}" >
                 <span class="font-size-xs">4</span>
            </span>
             
             </div>
            <div class="p-2 text-muted font-size-xs">{{max}}</div>
        </div>
    </div>
`
})
