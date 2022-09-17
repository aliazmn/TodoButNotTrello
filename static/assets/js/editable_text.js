const elements = document.getElementsByClassName("editable-test");

for (let elm of elements) {
    elm.addEventListener("click", (e) => {
        e.target.removeAttribute("readyonly");
    });
    elm.addEventListener("blur", (e) => {
        const att = document.createAttribute("readyonly");
        e.target.setAttributeNode(att);
        let value = e.target.value
        let _id = e.target.parentElement.dataset.id
        const model_name = e.target.parentElement.dataset.name
        console.log(_id)
        fetch("http://127.0.0.1:8000/change_name/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: _id,
                name: value,
                model_name: model_name
            }),
        }).then(() => {
            console.log("caption has been set")
        })
            .catch(() => {
                console.error("Error in set caption API")
            })
    });
}