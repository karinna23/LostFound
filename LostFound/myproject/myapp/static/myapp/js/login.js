document.addEventListener("DOMContentLoaded", function() {
    var alertElements = document.querySelectorAll('.alert');

    alertElements.forEach(function(alertElement) {
        var delay = 5000; // Delay in milliseconds (5 seconds in this example)

        setTimeout(function() {
            alertElement.style.transition = "opacity 0.5s";
            alertElement.style.opacity = "0";
        setTimeout(function() {
            alertElement.style.display = "none";
        }, 500); // Adjust the time to match the CSS transition duration
      }, delay);
    });
});
