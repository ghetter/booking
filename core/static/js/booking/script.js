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


// Логика для отображения подробной информации о нужном корпусе
document.addEventListener('DOMContentLoaded', function() {
    const campuses = document.querySelectorAll('.campuses__item.campus:not(.campus-disabled)');

    campuses.forEach(campus => {
        if (campus.classList.contains('campus-selected')) {
            const selectedCampusId = campus.querySelector('.campus__id').textContent.trim();
            
            const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
            );

            if (selectedDetail) {
                selectedDetail.classList.remove('campus__detailed-hidden');
            }

        } else {
            const detail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                detail.querySelector('.campus__id').textContent.trim() === campus.querySelector('.campus__id').textContent.trim()
            );

            if (detail) {
                detail.classList.add('campus__detailed-hidden');
            }
        }
    });

    campuses.forEach(campus => {
        campus.addEventListener('click', function() {
            const selectedCampusId = this.querySelector('.campus__id').textContent.trim();

            if (this.classList.contains('campus-selected')) {
                const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                    detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
                );

                if (selectedDetail) {
                    selectedDetail.classList.remove('campus__detailed-hidden');
                }

            } else {
                document.querySelectorAll('.campus__detailed').forEach(detail => {
                    detail.classList.add('campus__detailed-hidden');
                });

                const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                    detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
                );

                if (selectedDetail) {
                    selectedDetail.classList.remove('campus__detailed-hidden');
                }

                campuses.forEach(c => c.classList.remove('campus-selected'));
                this.classList.add('campus-selected');
            }
        });
    });
});

// Функционирование поиска аудитории по её номеру: если находится, то подсвечивается этаж и аудитория; иначе - "В корпусе нет данной аудитории"