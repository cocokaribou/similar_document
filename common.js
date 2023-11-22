// redirect to main
function goToMain() {
    window.location.href = "index.html"
}

// redirect to sub
function goToSub(index) {
    window.location.href = "sub.html?index=" + index
}

// redirect to search result
function goToSearch(keyword) {
    window.location.href = "search.html?query=" + keyword
}