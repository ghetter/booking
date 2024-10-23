document.addEventListener('DOMContentLoaded', function() {
    // Для пустых полей активна функция "Забронировать"
    const scheduleElements = document.querySelectorAll('.table__field');
    scheduleElements.forEach(field => {
        if (field.hasChildNodes()) {
            field.classList.remove('empty');
        } else {
            field.classList.add('empty');
            field.innerHTML += `
                <a href="#" class="bookNow">
                    <div class="bookNow__inner">
                        <img src="{% static 'img/booking/bookingPlusIcon.svg'%}" alt="">
                        <p>Забронировать</p>
                    </div>
                </a>
            `;
        }
    });




});

// Функционирование поиска аудитории по её номеру: если находится, то подсвечивается этаж и аудитория; иначе - "В корпусе нет данной аудитории"

// Функционирование pop-up окна. 
// !Версия №1: По нажатию на "Забронировать" открывается всплывающая форма с бронью. В этом окне по нажатию на крестик само окно закрывается.
// Версия №2: В форме заранее учитывается временной промежуток и день под которые бронируется аудитория
// Версия №3: Функционирует вместе с б/д
document.addEventListener('DOMContentLoaded', function() {
    const bookNowBtns = document.querySelectorAll('.bookNow');
    const bookingPopForm = document.querySelector('.pop-ups');
    const closeBtn = document.querySelector('.form__header-CloseBtn');

    bookNowBtns.forEach(bookNowBtn => {
        bookNowBtn.addEventListener('click', () => {
            bookingPopForm.classList.add('active');
        })
    });

    closeBtn.addEventListener('click', () => {
        bookingPopForm.classList.remove('active');
    });
});
