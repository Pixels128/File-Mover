/* 
1. Add the script tag below to in the head of HTML:
    <script src="https://combinatronics.com/Pixels128/Toolkit/main/refresh.js"></script>
2. Inside a script tag in the body, call the function: 
    refresh("/path-to-your-api")
3. replace `path-to-your-api` to an API endpoint, which returns JSON in the form of 
    {
        "state": unique-int-or-string
    }
4. `unique-int-or-string` should change only when the application is restarted.
*/

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
