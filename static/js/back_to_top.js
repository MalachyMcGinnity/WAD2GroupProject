document.addEventListener("DOMContentLoaded", function(){
    const backToTopButton = document.getElementById("backToTop");
    window.addEventListener("scroll", function(){
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    });
    
    backToTopButton.addEventListener("click", function(){
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
