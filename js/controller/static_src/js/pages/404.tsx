
let page = () => {

    return <>
        <p>This Page Does Not Exist</p>
        <p>Click <a href="#" onClick={history.back}>here</a> to go back</p>
    </>
}

let _: page = {
    page,
    title: "Not Found",
    urls: []
}

export = _
