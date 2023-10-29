import { getCookie } from '/static/script/cookies.js';
const csrf = getCookie('csrftoken')
$(document).ready(function () {
  
  $('.add_button').on('click' ,function () {
    let amount;
    const item = this;
    amount = $('#amount option:selected').text();
    if (amount.length === 0) {
      amount = 1;
    } else if (amount <= 0) {
        alert('Don\'t miss with numbers');
        return;
    }
    // item.dataset.qt compare if exceeded
    $.ajax({
      type: 'POST',
      url: item.dataset.url,
      headers: {"X-CSRFToken": csrf},
      data: {
        id: item.dataset.id,
        amount: amount,
        sign: "not_shoppen"
      },
      success: function (response) {
        $('#cart').text(response.amount)
        if ($(document).attr('title') === 'Cart') {
          $('#' + item.dataset.id +'s').text(response.item)
          cart_content(response)
        }
      }
    });
  });

  $('.dec_button').on('click' ,function () {
      console.log('here1')
      const item = this;
      // item.dataset.qt compare if exceeded
      $.ajax({
        type: 'POST',
        url: item.dataset.url,
        headers: {"X-CSRFToken": csrf},
        data: {
            id: item.dataset.id,
            sign: "not_shoppen"
        },
        success: function (response) {
            console.log(response.amount)
            $('#cart').text(response.amount)
            // console.log(response.amount)
            cart_content(response)
            console.log(response.item)  
            if (response.item  <= 0) {
                $('#' + item.dataset.id).remove();
            } else {
                $('#' + item.dataset.id +'s').text(response.item)
            }
        }
      });
  });

  $('.remove_button').on('click' ,function () {
    console.log('here1')
    const item = this;
    $.ajax({
      type: 'POST',
      url: item.dataset.url,
      headers: {"X-CSRFToken": csrf},
      data: {
          id: item.dataset.id,
          sign: "not_shoppen"
      },
      success: function (response) {
          console.log(response.amount)
          $('#cart').text(response.amount);
          cart_content(response)
          $('div #' + item.dataset.id).remove();
      }
  });
  });

  $('.wishlist').on('click' ,function () {
    const item = this;
    console.log(this.dataset.url)
    console.log(this.dataset.id)
    $.ajax({
      type: 'POST',
      url: item.dataset.url,
      headers: {"X-CSRFToken": csrf},
      data: {
        id: item.dataset.id
      },
      success: function (response) {
        if (response.authenticated) {
          console.log('here loggedin')
          const sym = $('<span/>', {html:'&#9825'});
          const sign = $('#wishlist-sign')
          if (sign.html() === sym.html()) {
            sign.html('&#9829;')
          } else {
            sign.html('&#9825;')
          }
        } else {
          console.log('here not')
          window.location.href=response.login +'?next=' + item.dataset.return
        }
      },
      error: function(response) {
        console.log('Error')
        console.log(response)
      }
    });
  });

})
function cart_content(res) {
    let word = res.amount + ' items';
    $('#total').text('total ' + res.total)
    if (res.amount === 1){
        word = res.amount + ' item';
    } else if (res.amount  <= 0) {
        word = 'Cart is empty';
        $('#cart-footer').remove();
    }
    $('#item-quantity').text(word);
}