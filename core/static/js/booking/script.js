// Отображение времени в <header>
function updateTime() {
    const optionsDate = { timeZone: 'Asia/Krasnoyarsk', year: 'numeric', month: '2-digit', day: '2-digit' };
    const optionsTime = { timeZone: 'Asia/Krasnoyarsk', hour: '2-digit', minute: '2-digit', hour12: false };

    const now = new Date();
    const date = new Intl.DateTimeFormat('ru-RU', optionsDate).format(now);
    const time = new Intl.DateTimeFormat('ru-RU', optionsTime).format(now);

    document.getElementById('current-date').textContent = date;
    document.getElementById('current-time').textContent = time;
}

setInterval(updateTime, 1000);
window.onload = updateTime;