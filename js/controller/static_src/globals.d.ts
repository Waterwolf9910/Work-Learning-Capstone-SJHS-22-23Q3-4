interface BaseWSData {
    type: string
}
interface SenserWSData extends BaseWSData {
    type: "sense",
    temp: number,
    pressure: number,
    humidity: number
}
interface PingWSData extends BaseWSData {
    type: "ping",
    msg: "Pong"
}
declare global {
    interface Window {
        state_data: {}
    }
    export type page = {
        title: string,
        page: () => JSX.Element,
        urls: string[],
        styles?: CSSStyleSheet[]
    }
    export type WSData = SenserWSData | PingWSData
}


export {}
