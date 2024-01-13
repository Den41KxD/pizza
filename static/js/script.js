document.addEventListener("DOMContentLoaded", function () {
    init_lang_selector()
    init_menu_header()
    hideAllArrowUp()
    init_burger_menu()
    init_mobile_menu_header()


});


function init_mobile_menu_header() {
    let menuLinks = document.querySelectorAll('.mobile__menu__link.has-children');

    menuLinks.forEach(menuLink => {
        const submenu = menuLink.querySelector('.submenu_mobile');

        menuLink.addEventListener('click', (event) => {
            if (event.target.classList.contains('submenu_mobile__link') || event.target.parentElement.classList.contains('submenu_mobile__link')){
                return
            }
            event.preventDefault(); // Отменяем стандартное действие ссылки


            if (submenu) {
                // Переключаем видимость подменю при клике
                if (submenu.style.display === 'flex') {
                    submenu.style.display = 'none';

                } else {
                    submenu.style.display = 'flex';
                }
                const rect = document.querySelector('.mobile__menu__link').parentElement.getBoundingClientRect();

                // Применим координаты к дочернему элементу

                submenu.style.top = rect.top + 'px';
                submenu.style.left = rect.left + 2 + 'px';
                submenu.style.width = rect.right - rect.left + 'px';
                submenu.style.height = '100%';
            }
        });
    });
}

function init_burger_menu() {
    const burgerButton = document.querySelector('.burger__mobile__header');
    const mobileMenu = document.querySelector('.mobile_menu');
    const closeButton = document.querySelector('.close_button');

    burgerButton.addEventListener('click', function () {
        mobileMenu.classList.toggle('open'); // Добавляем/удаляем класс open при клике на бургер

        // Добавляем обработчик для кнопки закрытия
        closeButton.addEventListener('click', function () {
            mobileMenu.classList.remove('open'); // Закрываем меню при клике на кнопку закрытия
        });
    });
}

function hideAllArrowUp() {
    document.querySelectorAll('.arrow_up').forEach(item => item.style.display = 'none')
    document.querySelectorAll('.arrow_down').forEach(item => item.style.display = '')
    document.querySelectorAll('.menu__item').forEach(item => item.classList.remove('highlighted'))

}

function init_lang_selector() {
    const languageSelect = document.getElementById("language-select");
    const languageSelect_mobile = document.getElementById("language-select__mobile");

    languageSelect.addEventListener("change", function () {
        const selectedValue = this.value;
        changeLanguage(selectedValue);
    });
    languageSelect_mobile.addEventListener("change", function () {
        const selectedValue = this.value;
        changeLanguage(selectedValue);
    });
}

function changeLanguage(selectedValue) {
    let newUrl = new URL(window.location.href).pathname.split('/')
    newUrl[1] = selectedValue
    history.replaceState(null, "", newUrl.join('/'));
    window.location.reload();
}

function add_overlay() {
    document.querySelector('.overlay').style.display = 'block'
}


function close_overlay() {
    document.querySelector('.overlay').style.display = 'none'
}

function show_arrow_up(item) {
    item.querySelector('.arrow_down').style.display = 'none'
    item.querySelector('.arrow_up').style.display = ''
}

function show_arrow_down(item) {
    item.querySelector('.arrow_down').style.display = ''
    item.querySelector('.arrow_up').style.display = 'none'
}

function init_menu_header() {
    const menuItemsWithChildren = document.querySelectorAll('.menu__item.has-children');
    let submenuTimeout;

    menuItemsWithChildren.forEach(item => {
        const submenu = item.nextElementSibling;

        item.addEventListener('mouseenter', function () {
            clearTimeout(submenuTimeout);
            add_overlay()
            show_arrow_up(item)

            closeAllSubmenus(); // Закрываем все открытые подменю
            submenu.style.display = 'flex';
            // item.parentElement.classList.add('highlighted');

            const rect = item.parentElement.parentElement.getBoundingClientRect();
            submenu.style.top = rect.bottom + 'px';
            submenu.style.left = rect.left + 'px';

        });

        item.addEventListener('mouseleave', function () {
            submenuTimeout = setTimeout(function () {
                submenu.style.display = 'none';
                item.classList.remove('highlighted');
                close_overlay()
                hideAllArrowUp()
                item.classList.remove('highlighted');
            }, 200); // Задержка в миллисекундах перед закрытием
        });

        submenu.addEventListener('mouseenter', function () {
            clearTimeout(submenuTimeout);
        });

        submenu.addEventListener('mouseleave', function () {
            submenuTimeout = setTimeout(function () {
                submenu.style.display = 'none';
                close_overlay()
                hideAllArrowUp()
                item.classList.remove('highlighted');

            }, 200); // Задержка в миллисекундах перед закрытием
        });
    });

    function closeAllSubmenus() {
        const allSubmenus = document.querySelectorAll('.submenu');
        allSubmenus.forEach(submenu => {
            submenu.style.display = 'none';
        });
        document.querySelectorAll('.menu__item').forEach(item => item.classList.remove('highlighted'))
    }
}


