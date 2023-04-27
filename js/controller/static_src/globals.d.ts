
declare global {
    interface Window {
        state_data: {}
    }
    export type page = {
        title: string,
        page: () => JSX.Element,
        urls: string[]
    }
}


export {}
