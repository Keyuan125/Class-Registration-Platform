(
    function () {
        let NetId = document.getElementById("NetId")
        let Password = document.getElementById("Password")
        let btn = document.getElementById("btn")
  
        function checkInput() {
            if(NetId.value != "" && Password.value != ""){
                btn.style.backgroundColor="#5286ed"
                btn.removeAttribute("disabled")
            }else{
                btn.style.backgroundColor="#c8c8c8"
                btn.setAttribute("disabled", true)
            }
        }
  
        function eventClick() {
          
          var success = /^([a-zA-Z]|[0-9]|_)+$/.test(NetId.value + Password.value) ? "success" : "fail"
          alert(success)
        }
  
        btn.addEventListener("click", eventClick)
        NetId.addEventListener("input", checkInput)
        Password.addEventListener("input", checkInput)
    }
  )()
  