async function getStatus(){
            let serverData = new Promise(function(resolve) {
            let req = new XMLHttpRequest();
            req.open('GET', "/getStatusajax");
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        req.onload = function() {
            if (req.status == 200) {
                resolve(req.response);
            } else {
                resolve("Server Unreachable");
            }
        };
            req.send();
        });
        return serverData;
        }

        window.onload = async function(){
            $('#state').on("click",async () => {
                let status = await getStatus();
                status = JSON.parse(status)
                $('#statusdisplay').text(status.data);
            })
        }