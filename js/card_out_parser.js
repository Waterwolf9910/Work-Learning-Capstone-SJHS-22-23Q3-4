let fs = require("fs")
let path = require("path")
let input = process.argv[ 2 ]
let _id = 0
let out = process.argv[ 3 ] || `cd_parsed${ _id++ }.json`
while (fs.existsSync(out) && process.argv[ 3 ] == undefined) {
    out = `cd_parsed${ _id++ }.txt`
}
if (input == undefined) {
    console.error("Input Path Required")
    process.exit(-1)
}
let data = fs.readFileSync(path.resolve(input), { encoding: 'utf-8' })
    .replaceAll("\r", '')
    .replaceAll("'", '"')
    .split("\n")
/**
 * @type {{chars: string[], str: string, raw: string[]}[]}
 */
let outdata = []
for (let i = 0; i < data.length; ++i) {
    if (i == 0 && data[ i ] != "<Card Outputs>") {
        process.exit(1)
    }
    if (!(data[ i ].startsWith("[") && data[ i ].endsWith("]"))) {
        continue;
    }
    let chars = []
    let str = String.fromCodePoint(...JSON.parse(data[ i ]))
    for (let i of str) {
        chars.push(i)
    }
    outdata.push({
        chars,
        str,
        raw: JSON.parse(data[ i ])
    })
}

fs.writeFileSync(path.resolve(out), JSON.stringify(outdata))
console.log("Done")
