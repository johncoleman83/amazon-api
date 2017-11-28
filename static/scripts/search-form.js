$(window).on('load', function () {
  var searchButton = document.querySelector('.item-search');
  var lookupButton = document.querySelector('.item-lookup');
  var activeElements = document.querySelectorAll('[data-action="animated"]');

  searchButton.addEventListener("click", function(){
    for (let i = 0; i < activeElements.length; i++) {
      activeElements[i].classList.remove('item-lookup-button-active');
      activeElements[i].classList.add('item-search-button-active');
    }
  });
  lookupButton.addEventListener("click", function(){
    for (let i = 0; i < activeElements.length; i++) {
      activeElements[i].classList.remove('item-search-button-active');
      activeElements[i].classList.add('item-lookup-button-active');
    }
  });

});
