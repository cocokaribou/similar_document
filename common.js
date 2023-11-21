// redirect to main
function goToMain() {
    window.location.href = "index.html"
}

// redirect to sub
function goToSub(index) {
    window.location.href = "sub.html?index=" + index
}

// redirect to search result
function goToSearch(keyword, page=-1) {
    var link = "search.html?query=" + keyword
    if (page != -1) link += "&page=" + page

    window.location.href = link
}