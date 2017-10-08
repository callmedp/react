function redirectToSearch(e) {
    location.href = '/search/results/?q='+encodeURI($('#id_q').val())
}
