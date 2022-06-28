let initalState = 0
let currentState = 0
let endpoint = "/"
async function getInitialState(){
    rsp = await fetch(endpoint).then(r => r.json())
    initalState = rsp['state']
    console.log("Refresh Session:", initalState)
}
async function getCurrentState(){
    rsp =  await fetch(endpoint).then(r => r.json())
    currentState = rsp['state']
    if (initalState !== currentState){
        location.reload()
    }
}
function refresh(e){
    endpoint = e
    getInitialState()
    setInterval(getCurrentState, 500)
}
