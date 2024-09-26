const btn = document.getElementById('btn')
const countElement = document.getElementById('count')

let count = 0

btn.addEventListener("click", function() {
    count++;
    countElement.textContent = count;
})