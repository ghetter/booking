document.addEventListener("DOMContentLoaded", function() {
    // Получаем текст из элемента с id 'form__speaker'
    const speakerElement = document.getElementById('form__speaker');
    const speakerName = speakerElement.textContent; // или innerHTML, если нужно сохранить HTML

    // Отладочная информация
    console.log('Имя спикера получено:', speakerName);

    // Устанавливаем этот текст в value инпута с id 'id_speaker'
    const speakerInput = document.getElementById('id_speaker');
    speakerInput.value = speakerName;

    // Отладочная информация
    console.log('Значение инпута "id_speaker" установлено:', speakerInput.value);

    // Получаем элемент с классом 'period__date'
    const dateElement = document.querySelector('.period__date');

    // Извлекаем текст интервала
    let dateText = dateElement.textContent;

    // Заменяем английские названия месяцев на русские
    const monthMap = {
        "January": "января",
        "February": "февраля",
        "March": "марта",
        "April": "апреля",
        "May": "мая",
        "June": "июня",
        "July": "июля",
        "August": "августа",
        "September": "сентября",
        "October": "октября",
        "November": "ноября",
        "December": "декабря"
    };

    // Заменяем названия месяцев
    for (const [en, ru] of Object.entries(monthMap)) {
        dateText = dateText.replace(new RegExp(en, 'g'), ru);
    }

    // Заменяем символ '–' на '-'
    dateText = dateText.replace(' – ', ' - ');

    // Убираем ведущие нули из дат
    dateText = dateText.replace(/\b0(\d)/g, '$1');

    // Обновляем текст элемента
    dateElement.textContent = dateText;

    // Вычисляем номер учебной недели
    const currentYear = new Date().getFullYear();
    const startOfSchoolYear = new Date(currentYear, 8, 2); // 2 сентября текущего года

    // Извлекаем первую дату интервала
    const [startDateStr] = dateText.split(' - ');

    // Преобразуем дату в формат YYYY-MM-DD
    const normalizedStartDateStr = startDateStr.replace(/(\d{1,2})\s([а-я]+)\s(\d{4})/, (match, day, month, year) => {
        const monthNumber = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12'
        }[month];
        return `${year}-${monthNumber}-${day}`;
    });

    // Создаем объект даты
    const startDate = new Date(normalizedStartDateStr);

    // Проверяем корректность даты
    if (isNaN(startDate.getTime())) {
        console.error("Некорректная дата:", normalizedStartDateStr);
        return; // Выходим из функции, если дата некорректна
    }

    // Вычисляем разницу в миллисекундах между датами
    const diffTime = startDate - startOfSchoolYear;

    // Вычисляем номер учебной недели
    const weekNumber = Math.floor(diffTime / (1000 * 60 * 60 * 24 * 7)) + 1;

    // Получаем элемент с классом 'period__week' и выводим номер учебной недели
    const weekElement = document.querySelector('.period__week');
    if (weekElement) {
        weekElement.textContent = `${weekNumber}-я неделя`;
    }

    // Функция для преобразования времени в 24-часовой формат
    function formatTimeTo24Hour(timeStr) {
        const parts = timeStr.split(' ');
        let [hours, minutes] = parts[0].split(':');
        const modifier = parts[1];

        if (!minutes) {
            minutes = '00'; // Если минут нет, устанавливаем их в 00
        }

        if (modifier === 'p.m.' && hours !== '12') {
            hours = parseInt(hours, 10) + 12;
        } else if (modifier === 'a.m.' && hours === '12') {
            hours = '00';
        }

        return `${hours}:${minutes}`;
    }

    // Обрабатываем все элементы '.ct__timestamp-from' и '.ct__timestamp-to'
    document.querySelectorAll('.ct__timestamp-from').forEach(fromElement => {
        fromElement.textContent = formatTimeTo24Hour(fromElement.textContent.trim());
    });

    document.querySelectorAll('.ct__timestamp-to').forEach(toElement => {
        toElement.textContent = formatTimeTo24Hour(toElement.textContent.trim());
    });

    // Получаем все элементы с классом '.table__heading-weekday'
    const weekdays = document.querySelectorAll('.table__heading-weekday');

    // Массив с названиями дней недели
    const daysOfWeek = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"];

    // Заполняем каждый элемент соответствующим днем недели
    weekdays.forEach((element, index) => {
        if (index < daysOfWeek.length) { // Проверяем, что индекс не превышает длину массива
            element.textContent = daysOfWeek[index];
        }
    });

    // Функция для форматирования дат в '.table__heading-date'
    function formatTableHeadingDate(dateStr) {
        const [monthAbbrev, day] = dateStr.split(' ');
        
        const monthMapShort = {
            "Jan.": "янв.",
            "Feb.": "фев.",
            "Mar.": "мар.",
            "April": "апр.",
            "May": "май",
            "June": "июн.",
            "July": "июл.",
            "Aug.": "авг.",
            "Sept.": "сен.",
            "Oct.": "окт.",
            "Nov.": "нояб.",
            "Dec.": "дек."
        };

        return `${day.replace(',', '')} ${monthMapShort[monthAbbrev]}`; // Убираем запятую и заменяем месяц
    }

    
    // Обрабатываем все элементы '.table__heading-date'
    document.querySelectorAll('.table__heading-date').forEach(dateElem => {
        dateElem.textContent = formatTableHeadingDate(dateElem.textContent.trim());
    });

    document.querySelectorAll('.bookNow').forEach(button => {
        button.addEventListener('click', function(event) {
            // Предотвращаем всплытие события
            event.stopPropagation();
            // Находим родительский элемент '.table__field'
            const parentField = this.closest('.table__field');
            // Получаем значения атрибутов
            const dateDay = parentField.getAttribute('date-day');
            const timeStart = parentField.getAttribute('time-start');
            const timeEnd = parentField.getAttribute('time-end');
            // Преобразуем дату и время в нужный формат
            const formattedDateStart = formatDateTime(dateDay, timeStart);
            const formattedDateEnd = formatDateTime(dateDay, timeEnd);
            // Заполняем инпуты
            document.getElementById('id_time_start').value = formattedDateStart;
            document.getElementById('id_time_end').value = formattedDateEnd;
        
            // Преобразуем время для видимых элементов времени в форме
            const formattedTimeStart = formatTimeVisible(timeStart);
            const formattedTimeEnd = formatTimeVisible(timeEnd);
            // Заполняем видимые элементы
            document.getElementById('form__time-start_visible').innerHTML = formattedTimeStart;
            document.getElementById('form__time-end_visible').innerHTML  = formattedTimeEnd;
        
            const userInfo = document.getElementById('form__speaker');
            const speaker = userInfo.innerHTML;
            document.getElementById('id_speaker').value = speaker;
            console.log('id_time_end:', document.getElementById('id_speaker').value);
        
            document.getElementById('id_title').placeholder = 'Введите название предмета';
        
            // Добавляем класс '.active' к элементу '.pop-ups'
            const popUpsElement = document.querySelector('.pop-ups');
            const popUpElement = document.querySelector('.pop-up');
            const popUpCloseBtn = document.querySelector('.form__header-CloseBtn');
            if (popUpsElement) {
                popUpsElement.classList.add('active');
                console.log('.pop-ups элемент активирован.');
        
                // Убираем класс '.active' при клике вне '.pop-up'
                const removeActiveClass = (event) => {
                    if (popUpsElement.classList.contains('active') && !popUpElement.contains(event.target)) {
                        popUpsElement.classList.remove('active');
                        console.log('.active класс убран.');
                        document.removeEventListener('click', removeActiveClass); // Удаляем обработчик после первого срабатывания
                    };

                    if (popUpCloseBtn.contains(event.target)) {
                        popUpsElement.classList.remove('active');
                    }
                };
        
                document.addEventListener('click', removeActiveClass);
            }
        });
        });
        
        // Функция для форматирования даты и времени
        function formatDateTime(dateDay, time) {
        const dateParts = dateDay.split(' ');
        const month = new Date(Date.parse(dateParts[0] + " 1, 2021")).getMonth() + 1;
        const day = dateParts[1].replace(',', '');
        const year = dateParts[2];
        
        const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        const timeParts = time.split(' ');
        let hours, minutes;
        
        if (timeParts[0].includes(':')) {
            [hours, minutes] = timeParts[0].split(':');
        } else {
            hours = timeParts[0];
            minutes = '00';
        }
        
        if (timeParts[1] === 'p.m.' && hours !== '12') {
            hours = String(Number(hours) + 12);
        } else if (timeParts[1] === 'a.m.' && hours === '12') {
            hours = '00';
        }
        
        const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:00`;
        
        return `${formattedDate} ${formattedTime}`;
        };
        
        
        function formatTimeVisible(time) {
        const timeParts = time.split(' ');
        let hours, minutes;
        
        if (timeParts[0].includes(':')) {
            [hours, minutes] = timeParts[0].split(':');
        } else {
            hours = timeParts[0];
            minutes = '00';
        }
        
        if (timeParts[1] === 'p.m.' && hours !== '12') {
            hours = String(Number(hours) + 12);
        } else if (timeParts[1] === 'a.m.' && hours === '12') {
            hours = '00';
        }
        
        const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
        
        return `${formattedTime}`;
        }





        const customSelect = document.querySelector('.custom-select');
        const selectedOptionBody = customSelect.querySelector('.custom-select__sfield');
        const selectedOption = customSelect.querySelector('.custom-select__soption');
        const optionsContainer = customSelect.querySelector('.custom-select__list');
        const selectedOptionIcon = customSelect.querySelector('.custom-select__soption-icon');
    
        // Открытие/закрытие выпадающего списка
        selectedOptionBody.addEventListener('click', () => {
            optionsContainer.classList.toggle('show'); // Переключаем класс show
            selectedOptionIcon.classList.toggle('active');
            
        });
    
        // Обработка выбора опции
        const options = optionsContainer.querySelectorAll('.custom-select__option');
    
        options.forEach(option => {
            option.addEventListener('click', () => {
                selectedOption.textContent = option.textContent; // Обновляем текст выбранной опции// Копируем классы для стилизации
                document.getElementById('id_type').value = option.getAttribute('data-value'); // Устанавливаем значение в скрытый select
                optionsContainer.classList.remove('show'); // Закрываем выпадающий список
                selectedOptionIcon.classList.remove('active');
            });
        });
    
        // Закрытие выпадающего списка при клике вне него
        document.addEventListener('click', (event) => {
            if (!customSelect.contains(event.target)) {
                optionsContainer.classList.remove('show'); // Закрываем выпадающий список
                selectedOptionIcon.classList.remove('active');
            }
        });

});



// Работа списка в форме
document.addEventListener('DOMContentLoaded', () => {

});
