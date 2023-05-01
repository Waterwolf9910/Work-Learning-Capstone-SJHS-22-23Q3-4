process.env.WS_NO_UTF_8_VALIDATE="true"
require("../.pnp.cjs").setup()
import express = require("express")
import ews = require("express-ws")
import http = require("http")
import fs = require("fs")
import path = require("path")

let isDev = process.env.NODE_ENV == "development"
let app = express();
let wsRouter = express.Router()
let server = http.createServer(app)

app.use("/ws", wsRouter)

app.use(express.text({type: "*/*"}))

if (isDev) {
    let webpack: typeof import("webpack") = require("webpack")
    let wpdm: typeof import("webpack-dev-middleware") = require("webpack-dev-middleware")
    let wphm: typeof import("webpack-hot-middleware") = require("webpack-hot-middleware")
    let wpconfig: import("webpack").Configuration = require("../webpack.config")
    let compiler = webpack(wpconfig)
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
        
        wpmw.outputFileSystem.readdir(path.join(wpmw.stats.toJson().outputPath), (err) => {
            if (err) {
                return res.status(502).end()
            }

            // Should not get to this if in static or memoryfs
            if (req.path.match(/\..+$/)) {
                return res.status(404).end()
            }

            try {
                res.send(wpmw.outputFileSystem.readFileSync(path.join(wpmw.stats.toJson().outputPath, "index.html"), { encoding: 'utf-8' }))
            } catch {
                res.status(502).send("Internal Error")
            }
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

let wsInstance = ews(app, server, {
    wsOptions: {

    }
})
wsRouter.ws("/data", async (ws, req) => {
    ws.on("message", (_msg) => {
        let msg = _msg.toString('utf-8')
        if (msg == "Ping") {
            ws.send(JSON.stringify({
                type: "ping",
                msg: "Pong"
            }))
        }
    })
    //@ts-ignore
    ws.alive = true
    //@ts-ignore
    ws.on('pong', () => ws.alive = true)
})

wsRouter.ws("/_internal_data_", async (ws, req) => {
    if (req.ip != "127.0.0.1" && req.ip != "::1") {
        return ws.terminate()
    }
})

setInterval(async () => {
    for (let client of wsInstance.getWss().clients) {
        //@ts-ignore
        if (!client.alive) {
            return
        }
        let ran = (max: number, min: number = 0) => {
            return Math.random() * (max - min) + min
        }
        // Send Data from sensers here
        let data = {
            type: "sense",
            temp: ran(100, -100),
            pressure: ran(2405),
            humidity: Math.random()
        }
        client.send(JSON.stringify(data))
    }
}, isDev ? 1000 : 3000)

setInterval(async () => {
    for (let client of wsInstance.getWss().clients) {
        //@ts-ignore
        if (!client.alive) {
            return client.terminate()
        }
        
        //@ts-ignore
        client.alive = false
        client.ping()
    }
}, 30000)


server.listen(isDev ? 3000 : 80, () => {
    console.log("Listening on port", isDev ? 3000 : 80)
})
