import { getCookie } from '/static/script/cookies.js'
// console.log('start')
$('document').ready(
    $('#id_category').on('change', function (e) {
        let url = $('#subcat').data('url')
        console.log(url)
        let category_id = e.target.value
        $.ajax({
            type: 'POST',
        url: url,
        headers: {"X-CSRFToken": getCookie('csrftoken')},
    data: {
        id: category_id,
        sign: "not_shoppen"
    },
    success: function (response) {
        let subcategories = response.sub
        console.log(subcategories[1]['name'])

        let subcat = $('#id_subcategory')
        subcat.html('<option value="" selected="">---------</option>')
        for (let i = 0; i< subcategories.length; i++) {
        subcat.append(`<option value="${subcategories[i]['id']}">${subcategories[i]['name']}</option>`)
        }
        // $('#cart').text(response.amount)
        // if ($(document).attr('title') === 'Cart') {
        //     $('#' + item.dataset.id +'s').text(response.item)
        //     cart_content(response)
        // }
    }
    });
})
)