
let change_page = (url: `/${string}` | `./${string}`, data: {title: string, url: string, data?: {}}) => {
    let _url: string = url
    if (url.startsWith("./")) {
        _url = url.replace("./", location.pathname.replace(/\/$/, '') + '/')
    }
    document.title = data.title
    if (!data.data) {
        data.data = {};
    }
    window.history.pushState(data, '', _url)
}


export = {
    change_page
}
