const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
  bar.addEventListener('click', () => {
    nav.classList.add('active');
  })
}

if (close) {
  close.addEventListener('click', () => {
    nav.classList.remove('active');
  })
}

var MainImg = document.getElementById("MainImg");
var smallimg = document.getElementsByClassName("small-img");

for (var i = 0; i < smallimg.length; i++) {
  smallimg[i].onclick = function() {
    MainImg.src = this.src;
  };
}

let token = localStorage.getItem('authToken');
let navLinks = document.querySelectorAll('#navbar li');
if (token === null || token === undefined) {
    let path = window.location.pathname;
    let fileName = path.substring(path.lastIndexOf('/') + 1);
    if (fileName === 'cart.html') {
        window.location.href = 'signin.html'
    }
    for (let navLink of navLinks) {
        let element = navLink.querySelector('a')
        if (element.getAttribute("href") === "cart.html") {
            element.setAttribute("href", "signin.html")
            break;
        }
    }
}
else {
    console.log(navLinks)
    for (let navLink of navLinks) {
        let element = navLink.querySelector('a')
        if (element.getAttribute("href") === "signin.html") {
            navLink.parentNode.removeChild(navLink);
            break;
        }
    }
}



document.addEventListener('DOMContentLoaded', function () {
  var checkoutButton = document.getElementById('checkout-button');

  if (checkoutButton) {
      checkoutButton.addEventListener('click', function () {
          // Redirect to the checkout page
          window.location.href = 'checkout.html';
      });
  }
});
