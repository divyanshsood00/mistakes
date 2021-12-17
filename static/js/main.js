// Get search from and page links
let searchForm = document.getElementById('searchForm');
let pageLink = document.getElementsByClassName('page-link')
// ensure search form exist
if (searchForm) {
for (let i = 0; pageLink.length > i; i++) {
    pageLink[i].addEventListener('click', function (e) {
    e.preventDefault();
    let page = this.dataset.page
    // This is genius
    searchForm.innerHTML += `<input value=${page} name="page" hidden />`
    searchForm.submit()
    })
}
}