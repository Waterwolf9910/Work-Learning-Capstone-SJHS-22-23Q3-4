require("./reg_events")
import utils = require("./utils")
import react = require("react")
import dom = require("react-dom/client")
import err = require("./pages/404")
import pages = require("./pages/page_data.json")
import baseStyle = require("../css/base.scss")

//@ts-ignore
window.utils = utils

let root: dom.Root
let Element: () => JSX.Element
let UpdatePage = () => {
    let page_data = page_map[ location.pathname ]
    Element = page_data?.page || err?.page
    document.title = page_data?.title || err.title
    if (page_data?.styles) {
        document.adoptedStyleSheets = [baseStyle.default, ...page_data.styles]
    } else {
        document.adoptedStyleSheets = [baseStyle.default]
    }
    
    root.render(<react.StrictMode>
        <div className="nav">
            {...header_links}
        </div>
        <div id="content">
            <Element />
        </div>
    </react.StrictMode>)
}

let page_map: { [key: string]: { title: string, page: () => JSX.Element, styles?: CSSStyleSheet[] } } = {}
let header_links: JSX.Element[] = []
for (let file of pages) {
    try {
        let page_data: page = require(`./pages/${file}`)
        if (!page_data.page || !page_data.title || !page_data.urls || page_data.urls.length < 1) {
            continue;
        }
        for (let url of page_data.urls) {
            page_map[url] = {
                page: page_data.page,
                title: page_data.title,
                styles: page_data.styles
            }
        }

        header_links.push(<a onClick={(e) => {e.preventDefault(); e.stopPropagation(); utils.change_page(page_data.urls[0])}} key={`${page_data.title}=${page_data.urls[0]}`}>{page_data.title}</a>)
    } catch {}
}

if (module.hot) {
    root = module.hot?.data?.root || dom.createRoot(document.getElementById("root")!)
    document.title = module.hot?.data?.title || page_map[ location.pathname ]?.title || "Not Found"
    Element = module.hot?.data?.jsx || page_map[ location.pathname ]?.page || err.page
    module.hot.addDisposeHandler((data) => {
        data.root = root
        data.title = document.title
        data.jsx = Element
        utils.removeStatePushListener(UpdatePage)
        window.removeEventListener("popstate", UpdatePage)
    })
    module.hot.accept()
} else {
    root = dom.createRoot(document.getElementById("root")!)
    document.title = page_map[location.pathname]?.title || "Not Found"
    Element = page_map[location.pathname]?.page || err.page
}


/* document.adoptedStyleSheets = [ baseStyle.default ]
root.render(
    <react.StrictMode>
        <div>
            {...header_links}
        </div>
        <Element />
    </react.StrictMode>
) */
UpdatePage()

window.addEventListener("popstate", UpdatePage)
utils.addStatePushListener(UpdatePage)
