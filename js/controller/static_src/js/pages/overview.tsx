import react = require("react")

let page = () => <>
    <p>Hello World</p>
</>

let _: page = {
    title: "Main Page",
    page,
    urls: ["/"]
}

export = _
