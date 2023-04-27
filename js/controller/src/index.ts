require("../.pnp.cjs").setup()
import express = require("express")
import webpack = require("webpack")
import wpdm = require("webpack-dev-middleware")
import wphm = require("webpack-hot-middleware")
import http = require("http")
import fs = require("fs")
import path = require("path")
let wpconfig: webpack.Configuration | undefined
let isDev = process.env.NODE_ENV == "development"
try {
    wpconfig = require("../webpack.config")
} catch {}

let app = express();
let server = http.createServer(app)

app.use(express.text({type: "*/*"}))

if (isDev) {
    let compiler= webpack(wpconfig)
    app.use(wpdm(compiler, {
        // methods: "GET",
        serverSideRender: true,
        writeToDisk: false
    }))
    app.use(wphm(compiler, {
        path: '/__hmr'
    }))
}

app.use(express.static("./static", {dotfiles: "ignore", extensions: ["html"]}))

app.get("*", (req, res) => {
    if (isDev) {
        let wpmw: import('webpack-dev-middleware').Context<import('http').IncomingMessage, import('http').ServerResponse & import("webpack-dev-middleware").ExtendedServerResponse> = res.locals.webpack.devMiddleware
        
        wpmw.outputFileSystem.readdir(path.join(wpmw.stats.toJson().outputPath), (err, data) => {
            if (err) {
                return res.status(502).end()
            }
            if (req.path.match(/\..+$/)) {
                return res.status(404).end()
            }
            wpmw.outputFileSystem.readFile(path.join(wpmw.stats.toJson().outputPath, "index.html"), (err, data) => {
                if (err) {
                    res.status(502).send("Internal Error")
                }
                res.send(data)
            })
            // res.send("Hello World")
        })
    } else {
        if (req.path.match(/\..+$/)) {
            return res.status(404).end()
        }
        res.send(fs.readFileSync(path.resolve("./static/index.html"), { encoding: 'utf-8' }))
    }
    // let urlPath = path.dirname(path.resolve("./static", req.path))
    // if (!fs.existsSync(urlPath)) {
    //     return res.status(404).sendFile(path.resolve("./static/index.html"))
    // }
    // let files = fs.readdirSync(urlPath)
    // if (files.filter(v => v.startsWith(path.basename(req.path))).length < 1) {
    //     return res.status(404).sendFile(path.resolve("./static/index.html"))
    // }
})

server.listen(isDev ? 3000 : 80, () => {
    console.log("Listening on port", isDev ? 3000 : 80)
})
