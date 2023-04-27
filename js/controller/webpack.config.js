let rrt = require("react-refresh-typescript")
let rrwp = require("@pmmmwh/react-refresh-webpack-plugin")
let html = require('html-webpack-plugin')
let path = require('path');
let fs = require('fs')
const webpack = require("webpack");
let isDev = process.env.NODE_ENV != "production"

/* let pathData = {}
let pagedir = path.resolve(__dirname, 'static_src', 'js', 'pages')
for (let filename of fs.readdirSync(pagedir)) {
    let file = fs.readFileSync(path.resolve(pagedir, filename), { encoding: 'utf-8'})

    let exportInfo = /export ?\= ?\{ ?.+ ?\}/.exec(file.replaceAll(/[\r\n]/g, ''))
    
    if (exportInfo) {
        let info = exportInfo[0].replace(/export ?\= ?/, '').replaceAll("'", '"')
        JSON.parse(info)
    }
} */

let pagedir = path.resolve(__dirname, 'static_src', 'js', 'pages')
fs.writeFileSync(path.resolve(__dirname, "static_src/js/pages/page_data.json"), JSON.stringify(fs.readdirSync(pagedir).filter(v => v.endsWith(".tsx")).map(v => v.replace(".tsx", ''))))

/**
 * @type {import('webpack').Configuration}
 */
let config = {
    entry: {
        bundle: ["webpack-hot-middleware/client?path=/__hmr&reload=true", "./js/index.tsx"]
    },
    context: path.resolve(__dirname, "static_src"),
    devtool: isDev ? 'inline-source-map' : false,
    mode: isDev ? "development" : "production",
    output: {
        // filename: "bundle.js",
        path: path.resolve(__dirname, "build/static")
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loader: "ts-loader",
                options: {
                    getCustomTransformers: () => ({
                        before: [isDev && rrt.default()].filter(v => typeof v != "boolean")
                    })
                }
            },
            {
                test: /\.s?css/,
                use: [
                    {
                        loader: "css-loader",
                        options: {
                            modules: {
                                mode: "global",
                                namedExport: true
                            },
                            exportType: "css-style-sheet",
                            sourceMap: isDev
                        }
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sourceMap: isDev,
                            sassOptions: {
                                style: "compressed",
                                outputStyle: "compressed",
                                fiber: false
                            }
                        }
                    }
                ]
            },
            {
                test: /\.(png|jpeg|jpg|jfif|gif|webp|ico|tif|tiff|bmp)$/i,
                dependency: { not: [ 'url' ] },
                type: 'asset/resource'
            },
            {
                test: /\.svg$/i,
                dependency: { not: [ 'url' ] },
                type: 'asset/inline'
            }
        ]
    },
    resolve: {
        extensions: [ '.ts', '.tsx', '.js' ],
        extensionAlias: {
            '.ts': ['.js', '.ts']
        }
    },
    plugins: (() => {
        let plugins = []
        if (isDev) {
            plugins.push(
                new html({
                    inject: "head",
                    template: "./index.html",
                }),
                new webpack.HotModuleReplacementPlugin(),
                new rrwp({overlay: {sockIntegration: 'whm'}})
            )
        }
        return plugins
    })(),
    optimization: !isDev ? {
        minimize: true,
        runtimeChunk: 'single',
        mangleExports: "size",
        concatenateModules: true,
        innerGraph: true,
        providedExports: true,
    } : {
        mangleExports: 'deterministic'
    },
    target: ["web"]
    // plugins: [
    //     (() => isDev ? [] : undefined)()
    // ].filter(v => typeof v != "boolean" && v != undefined)
}

module.exports = config
