let button = document.querySelector('.theme-button');
let page = document.querySelector('.page');
button.onclick = function() {
  page.classList.toggle('theme-light');
  page.classList.toggle('theme-dark');
  console.log("Click");
};

