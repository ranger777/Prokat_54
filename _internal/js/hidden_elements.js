const btn_1 = document.querySelector(".btn_1");
const btn_2 = document.querySelector(".btn_2");
const btn_3 = document.querySelector(".btn_3");
const hidden_1 = document.querySelector(".hidden_1");
const hidden_2 = document.querySelector(".hidden_2");
const hidden_3 = document.querySelector(".hidden_3");

hidden_1.style.display = 'block'


btn_1.addEventListener("click", btnClick_1);
btn_2.addEventListener("click", btnClick_2);
btn_3.addEventListener("click", btnClick_3);

function btnClick_1() {
    hidden_1.style.display = 'block'
    hidden_2.style.display = 'none'
    hidden_3.style.display = 'none'
}
function btnClick_2() {
    hidden_1.style.display = 'none'
    hidden_2.style.display = 'block'
    hidden_3.style.display = 'none'
}
function btnClick_3() {
    hidden_1.style.display = 'none'
    hidden_2.style.display = 'none'
    hidden_3.style.display = 'block'
}