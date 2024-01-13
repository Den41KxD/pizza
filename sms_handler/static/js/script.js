document.addEventListener("DOMContentLoaded", function () {
    init_lang_selector()
    init_menu_header()
    hideAllArrowUp()
    init_burger_menu()
    init_mobile_menu_header()
    initSizeChanger()
    initAddProductToCart()
    initRemoveProductFromCart()
    initCart()
    initLoginButton()
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

function activate_product_card_wrap(status = true){
    let index = 1
    if (!status){
        index = -1
    }
    document.querySelectorAll('.product_card_wrap').forEach(item => item.style.zIndex = index)
}


function init_burger_menu() {
    const burgerButton = document.querySelector('.burger__mobile__header');
    const mobileMenu = document.querySelector('.mobile_menu');
    const closeButton = document.querySelector('.close_button');

    burgerButton.addEventListener('click', function () {
        mobileMenu.classList.toggle('open'); // Добавляем/удаляем класс open при клике на бургер
        if (mobileMenu.classList.contains('open')){
            activate_product_card_wrap(false)
        }else {
            activate_product_card_wrap()
        }

        // Добавляем обработчик для кнопки закрытия
        closeButton.addEventListener('click', function () {
            mobileMenu.classList.remove('open'); // Закрываем меню при клике на кнопку закрытия
            setTimeout(activate_product_card_wrap,300)

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
    activate_product_card_wrap(false)
}


function close_overlay() {
    document.querySelector('.overlay').style.display = 'none'
    activate_product_card_wrap(true)
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

function initSizeChanger() {
    document.querySelectorAll('.product_size').forEach(item => item.addEventListener('click', function (event) {
        event.preventDefault()
        const button = event.target
        if (button.classList.contains('active')) {
            return
        } else {
            for (let element = 0; element < button.parentElement.children.length; element++) {
                button.parentElement.children[element].classList.remove('active')
                button.classList.add('active')
            }
            const product_id = button.dataset.id
            $.ajax({
                url: '/en/linked_prod_info',
                data: {
                    'product_id': product_id,
                },
                success: function (data) {
                    console.log(data)
                    button.parentNode.parentNode.querySelector('.product_weight_value').innerHTML = data['weight'] + ' '
                    button.parentNode.parentNode.querySelector('.product_price_value').innerHTML = data['price']
                },
            });
        }
    }))

}


function initAddProductToCart() {document.querySelectorAll('.add_product_to_cart').forEach(item => item.addEventListener('click', addProductToCart))}

function addProductToCart(event) {
    event.preventDefault()
    const product_id = event.target.dataset.id

    document.querySelector('.cart_desc').style.display = 'block'

    $.ajax({
        url: '/en/cart/add',
        method: 'post',
        data: {
            'product_id': product_id,
        },
        success: function (data) {
            update_cart_info(data)

        },
    });
}

function initRemoveProductFromCart(){
        document.querySelectorAll('.subtract_product_from_cart')
            .forEach(item => item.addEventListener('click',subtractProductFromCart))
}

function subtractProductFromCart(event) {
    event.preventDefault()
    const product_id = event.target.dataset.id
    let currentInput = event.target.parentElement.querySelector('.quantity__select__count')
    if(currentInput.value === '1'){
        return
    }
    $.ajax({
        url: '/en/cart/subtract',
        method: 'post',
        data: {
            'product_id': product_id,
        },
        success: function (data) {
            update_cart_info(data)

        },
    });
}

function initCart(){
    document.querySelector('.card__mobile').addEventListener('click', function (){
        console.log('qwerqwer')
    })

    document.querySelectorAll('.quantity__select__add').forEach(item => item.addEventListener('click', cart_counter_add))
    document.querySelectorAll('.quantity__select__subtract').forEach(item => item.addEventListener('click', cart_counter_subtract))
    document.querySelectorAll('.cart_item__trash').forEach(item => item.addEventListener('click', cart_item_delete))
}


function check_active_selector(event){
    let currentInput = event.target.parentElement.querySelector('.quantity__select__count')

    if(currentInput.value === '1'){
        event.target.classList.add('disabled')
        return false
    }else {
        event.target.parentElement.querySelector('.quantity__select__subtract').classList.remove('disabled')
        return true
    }
}


function cart_counter_add(event){
    let currentInput = event.target.parentElement.querySelector('.quantity__select__count')
    currentInput.value = parseInt(currentInput.value) + 1
    check_active_selector(event)
}

function cart_counter_subtract(event){
    if (!check_active_selector(event)){
        return
    }
    let currentInput = event.target.parentElement.querySelector('.quantity__select__count')
    currentInput.value = parseInt(currentInput.value) - 1

}

function update_cart_info(response_data){
    console.log(response_data)
    document.querySelector('.cart_len').innerText = response_data['products_count']
    document.querySelector('.total_price_sum').innerText = response_data['total_price']
    if (response_data['new_item']){
        create_cart_item(response_data['new_item'])
    }
}


function cart_item_delete(event) {
    const product_id = event.target.dataset.id

    $.ajax({
        url: '/en/cart/remove',
        method: 'post',
        data: {
            'product_id': product_id,
        },
        success: function (data) {
            update_cart_info(data)
            const productContainer = event.target.closest('.cart__product');
            if (productContainer) {
                productContainer.remove();
            }

        },
    });
}


function create_cart_item(new_item) {
    // Создаем элемент <div> и добавляем классы
    const cartProduct = document.createElement('div');
    cartProduct.classList.add('cart__product');

// Создаем элемент <img> для изображения товара
    const productImage = document.createElement('img');
    productImage.classList.add('cart_product_image');
    productImage.src = window.location.origin + new_item.product.image; // Замените на реальный URL изображения
    console.log(productImage.src)
    productImage.alt = 'Alt текст изображения';

// Создаем контейнер <div> для информации о товаре
    const productInfo = document.createElement('div');
    productInfo.classList.add('cart__product__info');

// Создаем элемент <div> для названия товара
    const productName = document.createElement('div');
    productName.classList.add('cart_item');
    productName.textContent = new_item.product.name; // Замените на реальное название товара

// Создаем элемент <div> для веса и единиц измерения
    const productWeight = document.createElement('div');
    productWeight.classList.add('cart_item');
    productWeight.textContent = new_item.product.weight; // Замените на реальный вес и единицы измерения

// Создаем элемент <div> для цены и валюты
    const productPrice = document.createElement('div');
    productPrice.classList.add('cart_item');
    productPrice.innerHTML = `${new_item.product.get_price} <span class="currency">uah</span>`; // Замените на реальную цену

// Создаем контейнер <div> для управления количеством товара
    const quantitySelect = document.createElement('div');
    quantitySelect.classList.add('quantity__select');

// Создаем кнопку "Уменьшить"
    const subtractButton = document.createElement('div');
    subtractButton.classList.add('quantity__select__subtract', 'quantity__item', 'subtract_product_from_cart');
    subtractButton.textContent = '-';
    subtractButton.setAttribute('data-id', new_item.product.id); // Замените на реальный ID товара
    subtractButton.addEventListener('click', subtractProductFromCart)
    subtractButton.addEventListener('click', cart_counter_subtract)

// Создаем input для количества товара
    const quantityInput = document.createElement('input');
    quantityInput.type = 'number';
    quantityInput.disabled = true;
    quantityInput.classList.add('quantity__select__count');
    quantityInput.value = new_item.quantity; // Замените на реальное количество товара

// Создаем кнопку "Увеличить"
    const addButton = document.createElement('div');
    addButton.classList.add('quantity__select__add', 'quantity__item', 'add_product_to_cart');
    addButton.textContent = '+';
    addButton.setAttribute('data-id', new_item.product.id); // Замените на реальный ID товара
    addButton.addEventListener('click', addProductToCart)
    addButton.addEventListener('click', cart_counter_add)

// Создаем кнопку удаления товара
    const trashButton = document.createElement('img');
    trashButton.classList.add('cart_item__trash');
    trashButton.src = window.location.origin+'/static/icons/trash.svg'; // Замените на реальный URL изображения корзины
    trashButton.alt = 'Удалить товар';
    trashButton.setAttribute('data-id',  new_item.product.id); // Замените на реальный ID товара
    trashButton.addEventListener('click', cart_item_delete)

// Добавляем все созданные элементы в DOM
    cartProduct.appendChild(productImage);
    cartProduct.appendChild(productInfo);
    productInfo.appendChild(productName);
    productInfo.appendChild(productWeight);
    productInfo.appendChild(productPrice);
    productPrice.appendChild(quantitySelect);
    quantitySelect.appendChild(subtractButton);
    quantitySelect.appendChild(quantityInput);
    quantitySelect.appendChild(addButton);
    productPrice.appendChild(trashButton);
    document.querySelector('.cart_items').appendChild(cartProduct)


}


function openLoginMenu() {
    document.querySelector('.login_menu').classList.add('opened');
}

function closeLoginMenu() {
    document.querySelector('.login_menu').classList.remove('opened');
}

function initLoginButton() {
    document.querySelector('.login_reg').addEventListener('click', function (event) {
        event.preventDefault();
        openLoginMenu();
    });
    document.querySelector('.close_button_login').addEventListener('click', closeLoginMenu);
}
