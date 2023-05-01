import react = require("react")
import utils = require("../utils")
let _: page = {
    page: () => {
        let [data, setData] = react.useState({
            temp: 0.0,
            pressure: 0.0,
            humidity: 0
        })
        let [inCelsius, setTempMode] = react.useState(true)
        react.useEffect(() => {
            utils.WSConnection.addEventListener("message", (msg) => {
                let data: WSData = JSON.parse(msg.data)
                if (data.type != "sense") {
                    return;
                }
                setData(data)
            })
        }, [])
        return <>
            <p>Temp: {(inCelsius ? data.temp : (data.temp * 9 / 5) + 32).toFixed(2)} {(inCelsius ? 'C' : 'F')}° <button type="button" onClick={() => {setTempMode(!inCelsius)}}>to {(inCelsius ? 'F' : 'C')}</button> </p>
            <p>Humidity: { (parseFloat(data.humidity.toFixed(2)) * 100 ).toFixed(0)}%</p>
            <p>Pressure: { data.pressure.toFixed(2) } Millibars</p>
        </>
    },
    title: "Sensor Data",
    urls: ["/sensor", "/sensor_data"]
}

export = _
