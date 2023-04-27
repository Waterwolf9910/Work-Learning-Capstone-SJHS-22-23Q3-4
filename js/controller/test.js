let fs = require("fs")
let cp = require("child_process")
let path = require("path")


let vid = cp.spawn("libcamera-vid -t 0 -codec libav --libav-format matroska --width 1920 --height 1080 --hdr --denoise cdn_hq --autofocus-mode continuous -n -v 0 -o -", {
    stdio: ["ignore", "pipe", "inherit"],
    shell: true,
})
vid.unref()
// vid.stdout.pause()
setTimeout(() => {
    let http = require("http")
    http.createServer((r, s) => {
        console.log("Connection")
        vid.stdout.pipe(s)
    }).listen(9910)
    // setTimeout(() => {
    //     vid.stdout.pause()
    // }, 3000)
}, 2000)

vid.stdout.on("end", () => {
    inv.unref()
    clearInterval(inv)
    console.log("Done")
})

// console.log(img, img.stderr, img.stdout, img.stderr)
vid.stdout.pipe(fs.createWriteStream("./vid.h264"))

let inv = setInterval(() => {}, 1000)

inv.ref()

