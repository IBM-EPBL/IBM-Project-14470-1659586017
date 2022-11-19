let x;
let toast = document.getElementById("toast");
function showToast(){
    clearTimeout(x);
    toast.style.transform = "translateX(40px)";
    x = setTimeout(()=>{
        toast.style.transform = "translateX(450px)"
    }, 4000);
}
window.onload(setTimeout(showToast, 1000));