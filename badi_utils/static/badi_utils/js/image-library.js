const imgLibraryVue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#image-library',
    data() {
        return {
            images: [],
            selectedImage: {
                id: null,
            },
            src: '',
            alt: '',
            currentPage: 1,
            count: 0,
            limit: 25,
            showForm: true,
        }
    },
    created: function () {
        this.getImages();
    },
    watch: {
        'alt': function (newVal) {
            this.getImages()
        }
    },
    methods: {
        getImages: function (data = {page: null}) {
            this.loading = true;
            console.log('HERE', data['page'])
            let SLUG = 'limit=' + this.limit;
            if (data['page']) {
                this.currentPage = data['page'];
                SLUG += `&page=${data['page']}`
            }
            ApiAjax({
                url: '/api/v1/blogimage/?alt=' + this.alt + '&' + SLUG,
                method: 'GET',
                success_message: false,
                form: false,
                clearForm: false,
                success: (res) => {
                    this.images = res.results;
                    this.count = res.count;
                    this.loading = false;
                }
            })
        },
        deleteProp: function (pk) {
            this.loading = true;
            ApiAjax({
                url: '/api/v1/blogimage/',
                pk,
                method: 'DELETE',
                form: false,
                success_message: 'با موفقیت حذف شد!',
                success: () => {
                    this.getProps();
                },
            })
        },
        addImage: function () {
            this.loading = true;
            ApiAjax({
                url: '/api/v1/blogimage/',
                method: 'POST',
                file: true,
                form: '#image-form',
                success_message: 'با موفقیت آپلود شد!',
                success: () => {
                    this.src = null;
                    this.getImages();
                },
                error: () => {
                    this.loading = false;
                }
            })
        },
        fileSelect: function (e) {
            document.getElementById('id_image_library').click()
        },
        copyToClip: function (e) {
            copyText(e)
        },
        resetForm: function (e) {
            document.getElementById("image-form").reset();
            $('#id_image_library').attr('type', 'text')
            $('#id_image_library').attr('type', 'file')
            this.src = null;
        },
        imageChanged: function (e) {
            const input = document.getElementById('id_image_library')
            if (input.files && input.files[0]) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    let image = new Image();
                    image.src = e.target.result;
                    imgLibraryVue.src = e.target.result;
                };
                reader.readAsDataURL(input.files[0]); // convert to base64 string
            } else {
                imgLibraryVue.src = null;
            }

        },
        setImage: function (e) {
            if (this.selectedImage.id) {
                window['imageSelected'](this.selectedImage);
                $('#image-library-modal').modal('hide');
            }
        },
    },
});