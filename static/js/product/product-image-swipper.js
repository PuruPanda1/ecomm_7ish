function initSwiper() {
  var swiper = new Swiper("#gallery-swiper-started", {
    slidesPerView: 1,
    spaceBetween: 10,
    loop: true, // Enables looping through images
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
}

document.addEventListener("DOMContentLoaded", function () {
  initSwiper();
});

// Reinitialize Swiper after HTMX swaps content
document.addEventListener("htmx:afterSwap", function (event) {
  if (event.target.id === "gallery-swiper-started") {
    initSwiper();
  }
});
