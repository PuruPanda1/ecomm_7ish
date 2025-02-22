
/**
  * Range Two Price
  * Filter Products
  * Filter Sort 
  * Switch Layout
  * Handle Sidebar Filter
  * Handle Dropdown Filter
 */
(function ($) {
  "use strict";


  // Fixed layout switching
  document.addEventListener("DOMContentLoaded", function () {
    const layoutSwitchButtons = document.querySelectorAll(".tf-view-layout-switch");
    const gridContainer = document.getElementById("gridLayout");
  
      layoutSwitchButtons.forEach(button => {
        button.addEventListener("click", function () {
          // Remove "active" class from all buttons
          layoutSwitchButtons.forEach(btn => btn.classList.remove("active"));
          
          // Add "active" class to the clicked button
          this.classList.add("active");
  
          // Get the new layout class from data attribute
          const newLayout = this.getAttribute("data-value-layout");
  
          // Remove old layout classes (tf-col-2, tf-col-3, tf-col-4)
          gridContainer.classList.remove("tf-col-2", "tf-col-3", "tf-col-4");
  
          // Add the new layout class
          gridContainer.classList.add(newLayout);
        });
    });
  });

  /* Handle Sidebar Filter 
  -------------------------------------------------------------------------------------*/ 
  var handleSidebarFilter = function () {
    $(".filterShop").click(function () {
      if ($(window).width() <= 1150) {
        $(".sidebar-filter,.overlay-filter").addClass("show");
      }
    });
    $(".close-filter ,.overlay-filter").click(function () {
      $(".sidebar-filter,.overlay-filter").removeClass("show");
    });
  };




  $(function () {
    handleSidebarFilter();
  });
})(jQuery);

