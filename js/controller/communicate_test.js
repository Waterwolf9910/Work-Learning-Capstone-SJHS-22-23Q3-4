require("./.pnp.cjs").setup()
let child_process = require("child_process")
let express = require("express")
let ews = require("express-ws")
let http = require("http")

let app = express()
let wsRouter = express.Router()
app.use(wsRouter)
let server = http.createServer(app)
let instance = ews(app, server)

let rl = require('readline').createInterface({
    input: process.stdin,
})

let python = child_process.spawn("python3", ["../../py/communicate_test.py"], {
    shell: true,
    // stdio: 'ignore'
    stdio: ["ignore", "inherit", "inherit"]
})

wsRouter.ws("/ws", async ws => {
    ws.on("message", (_msg) => {
        console.log(_msg)
    })
})

// let stream = require("stream")
let inv = setInterval(() => {
    console.log("Sending Ping")
    instance.getWss().clients.forEach(client => {
        client.send(JSON.stringify({
            msg: "Ping!"
        }))
    })
    // console.log(python.stdin.write(JSON.stringify({
    //     msg: "Ping!"
    // })))
    // python.stdin.uncork()
    // let r = new stream.PassThrough()
    // r.pipe(python.stdin)
    // r.end(JSON.stringify({
    //     msg: "Ping!"
    // })+'\n')
    // r.end(,)
    // python.stdin.write("H")
    // python.stdin.end()

}, 5000)
/* python.stdout.setEncoding("utf-8").on("data", (_data) => {
    try {
        let data = JSON.parse(_data)

        if (data.msg == "Pong!") {
            console.log("Received Pong")
        } else {
            console.log(_data)
        }
    } catch {
        if (_data == " " || _data == "\n") {
            return
        }
        console.log(_data)
    }
}) */

server.listen(9910)

let closing = false

let exit = (c = 0) => {
    closing = true
    clearInterval(inv)
    rl.close()
    for (let client of instance.getWss().clients) {
        client.send(JSON.stringify({
            msg: "quit"
        }))
    }
    setTimeout(() => {
        process.exit(c)
    }, 2000)
}

python.on("close", () => {
    if (closing) {
        return
    }
    console.error("Python has been closed")
    exit(2)
})

rl.on("line", (i) => {
    if (i == 'q') {
        exit(0)
    }
})
