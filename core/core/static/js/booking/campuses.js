document.addEventListener('DOMContentLoaded', function() {
    const campuses = document.querySelectorAll('.campuses__item.campus:not(.campus-disabled)');

    // Инициализация: показываем блок с подробной информацией для выбранного корпуса
    campuses.forEach(campus => {
        if (campus.classList.contains('campus-selected')) {
            const selectedCampusId = campus.querySelector('.campus__id').textContent.trim();
            console.log(`Инициализация: выбранный корпус - ${selectedCampusId}`); // Отладка
            
            // Показываем соответствующий блок с подробной информацией
            const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
            );

            if (selectedDetail) {
                console.log(`Показываем блок для: ${selectedCampusId}`); // Отладка
                selectedDetail.classList.remove('campus__detailed-hidden');
            }
        } else {
            // Скрываем все остальные блоки с подробной информацией
            const detail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                detail.querySelector('.campus__id').textContent.trim() === campus.querySelector('.campus__id').textContent.trim()
            );
            if (detail) {
                console.log(`Скрываем блок для: ${detail.querySelector('.campus__id').textContent.trim()}`); // Отладка
                detail.classList.add('campus__detailed-hidden');
            }
        }
    });

    campuses.forEach(campus => {
        campus.addEventListener('click', function() {
            // Получаем полное название корпуса
            const selectedCampusId = this.querySelector('.campus__id').textContent.trim();
            console.log(`Выбранный корпус: ${selectedCampusId}`); // Отладка

            // Проверяем, имеет ли кнопка класс .campus-selected
            if (this.classList.contains('campus-selected')) {
                // Если да, то просто показываем соответствующий блок
                const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                    detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
                );

                if (selectedDetail) {
                    console.log(`Сохраняем отображение блока для: ${selectedCampusId}`); // Отладка
                    selectedDetail.classList.remove('campus__detailed-hidden');
                }
            } else {
                // Если нет, скрываем все блоки с подробной информацией
                document.querySelectorAll('.campus__detailed').forEach(detail => {
                    console.log(`Скрываем блок для: ${detail.querySelector('.campus__id').textContent.trim()}`); // Отладка
                    detail.classList.add('campus__detailed-hidden');
                });

                // И показываем только выбранный блок
                const selectedDetail = Array.from(document.querySelectorAll('.campus__detailed')).find(detail => 
                    detail.querySelector('.campus__id').textContent.trim() === selectedCampusId
                );

                if (selectedDetail) {
                    console.log(`Отображаем блок для: ${selectedCampusId}`); // Отладка
                    selectedDetail.classList.remove('campus__detailed-hidden');
                } else {
                    console.log(`Блок не найден для: ${selectedCampusId}`); // Отладка
                }

                // Убираем класс .campus-selected у всех кнопок и добавляем его только к нажатой
                campuses.forEach(c => c.classList.remove('campus-selected'));
                this.classList.add('campus-selected');
            }
        });
    });
});