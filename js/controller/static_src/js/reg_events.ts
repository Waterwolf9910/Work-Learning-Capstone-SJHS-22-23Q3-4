/* let pushState = history.pushState
history.pushState = (data, unused: string, url?: string | URL) => {
    statePushedListeners.forEach(async v => v())
    return pushState(data, unused, url)
}

type stateListener = () => any
let statePushedListeners: stateListener[] = []

export = {
    addStatePushListener: (listener: () => any) => { statePushedListeners.push(listener) },
    removeStatePushListener: (listener: () => any) => { statePushedListeners = statePushedListeners.filter(v => v != listener) }
} */
