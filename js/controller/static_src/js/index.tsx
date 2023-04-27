require("./reg_events")
import react = require("react")
import dom = require("react-dom/client")
import err = require("./pages/404")
import pages = require("./pages/page_data.json")

let root: dom.Root
let Element: () => JSX.Element

let page_map: { [key: string]: { title: string, page: () => JSX.Element } } = {}

for (let file of pages) {
    try {
        let page_data: page = require(`./pages/${file}`)
        
        for (let url of page_data.urls) {
            page_map[url] = {
                page: page_data.page,
                title: page_data.title
            }
        }
    } catch {}
}

// for (const url of overview.urls) {
//     page_map[url] = {
//         page: overview.page,
//         title: overview.title
//     }
// }

if (module.hot) {
    root = module.hot?.data?.root || dom.createRoot(document.getElementById("root"))
    document.title = module.hot?.data?.title || page_map[ location.pathname ]?.title || "Not Found"
    Element = module.hot?.data?.jsx || page_map[ location.pathname ]?.page || err.page
    module.hot.addDisposeHandler((data) => {
        data = {
            root,
            title: document.title,
            jsx: Element
        }
        window.removeEventListener("popstate", pse)
    })
    module.hot.accept()
} else {
    root = dom.createRoot(document.getElementById("root"))
    document.title = page_map[location.pathname]?.title || "Not Found"
    Element = page_map[location.pathname]?.page || err.page
}


root.render(
    <react.StrictMode>
        <Element />
        <p>B</p>
    </react.StrictMode>
)

let pse = (e: PopStateEvent) => {
    let page_data = page_map[ location.pathname ]
    Element = page_data?.page || err?.page
    document.title = e.state?.title || page_data?.title || err.title
    root.render(<react.StrictMode>
        <Element />
    </react.StrictMode>)
}

window.addEventListener("popstate", pse)
