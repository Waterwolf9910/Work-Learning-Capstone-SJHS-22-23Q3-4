let pushState = history.pushState
history.pushState = (data, unused: string, url?: string | URL) => {
    return pushState(data, unused, url)
}

type stateListener = () => any
let statePushedListener: stateListener[] = []

let pse = (e: PopStateEvent) => {
    let state: {
        title: string
        url: string
        data: {}
    } = e.state
    if (state) {
        document.title = state.title
        window.state_data = state.data
    }
}

window.addEventListener("onStateChange", () => {})

window.addEventListener("popstate", pse)
if (module.hot) {
    module.hot.addDisposeHandler(() => {
        console.log("HMR Cleanup")
        window.removeEventListener("popstate", pse)
    })
    console.log("Hello")
}
