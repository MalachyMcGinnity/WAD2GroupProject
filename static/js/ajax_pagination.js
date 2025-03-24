document.addEventListener("DOMContentLoaded", function(){
    function attachAjaxPagination(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.addEventListener("click", function(event){
                const target = event.target;
                if (target.tagName === "A" && target.classList.contains("ajax-pagination")) {
                    event.preventDefault();
                    if (container.dataset.ajaxLoading === "true") {
                        return;
                    }
                    container.dataset.ajaxLoading = "true";
                    fetch(target.href, {headers: {"X-Requested-With": "XMLHttpRequest"}})
                        .then(response => response.text())
                        .then(html => {
                            container.innerHTML = html;
                            attachAjaxPagination(containerId);
                            if (containerId === "commentsContainer" && typeof applyReadMore === 'function') {
                                applyReadMore();
                            }
                        })
                        .catch(error => console.error("AJAX pagination error:", error))
                        .finally(() => {
                            container.dataset.ajaxLoading = "false";
                        });
                }
            });
        }
    }
    // Attach AJAX pagination to all necessary containers
    attachAjaxPagination("todays_albums_container");
    attachAjaxPagination("uploaded_albums_container");
    attachAjaxPagination("rated_albums_container");
    attachAjaxPagination("albums_search_container");
    attachAjaxPagination("users_search_container");
    attachAjaxPagination("commentsContainer");
});
