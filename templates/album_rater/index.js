document.getElementById("create_album_button").addEventListener("click", function() {
    window.location.href = "{% url 'my_django_view' %}";
    console.log("AAA");
});