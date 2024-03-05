const popupLinks = document.querySelectorAll('.popup-link');//находим все объекты с классом popup-link
const body = document.querySelector('body');
const lockPadding = document.querySelectorAll(".lock-padding");

let unlock = true;

const timeout = 20;//время такоеже как в css

//проходим по всем обхектам popup-link
if (popupLinks.length > 0){//проверили что не пусто
    for (let i = 0; i < popupLinks.length; i++){
        const popupLink = popupLinks[i];
        popupLink.addEventListener("click", function (e){
            const popupName = popupLink.getAttribute('href').replace('#', '');//из id уберам # чтоб получить имя окна
            const curentPopup = document.getElementById(popupName);//берем окно с этим имененм
            popupOpen(curentPopup);//запускаем функцию на открытие окна
            e.preventDefault();//запрещаем обновляться странице (потомучто мы же на ссылку нажимаем)
        });
    }
}

const popupCloseIcon = document.querySelectorAll('.popup__close');//ищем все объекты, которые могут закрыть окно
if (popupCloseIcon.length > 0) {//проверяемя что такие объекты есть
    for (let i = 0; i < popupCloseIcon.length; i++){
        const el = popupCloseIcon[i];
        el.addEventListener('click', function (e){
            popupClose(el.closest('.popup'));//ище ближайшего родителя с классом popup, его и закроем
            e.preventDefault();//запрещаем обновляться странице (потомучто мы же на ссылку нажимаем)
        })
    }
}

function popupOpen(curentPopup){//передаем в функцию открытия попапа объект, который надо открыть
    if (curentPopup && unlock) {//проверяем есть ли такой объект и окрыта ли переменная unlock (вначале ее открыли специально)
        const popupActive = document.querySelector('.popup.open');//ищем объект с классом popup у котолрого уже открыто окно
        if (popupActive){//если открытое окно существует - закрываем
            popupClose(popupActive, false);
        } else {
            bodyLock();//если нет, то блокируем скрол
        }
        curentPopup.classList.add('open');//далее на открываемый объект добавляем класс open
        curentPopup.addEventListener("click", function (e){//и сразу вешаем функцию на него
            if (!e.target.closest('.popup__content')){//если у нажатого объекта нет класса popup__content (другими словами выбираем всю область за пределами попапа)
                popupClose(e.target.closest('.popup'))//то закрываем попап с ближайшим родителем popap
            }
        });
    }
}
function popupClose(popupActiv, doUnlock = true) {//тут если из однго попапа переходим во второй, то скрол по новой блочить не надо
    if (unlock) {
        popupActiv.classList.remove('open');//убираем клас open
        if (doUnlock) {
            bodyUnlock();
        }
    }
}
function bodyLock(){//тут мы высчитываем размер скрола, и, чтоб контент не скакал, подменяет его падингами
        const lockPaddingValue = window.innerWidth// - document.querySelector('body').offsetWidth + 'px';//в моем случае это не требуется

        if (lockPadding.length > 0) {
            for (let i = 0; i < lockPadding.length; i++){
                const el = lockPadding[i]
                el.style.paddingRight = lockPaddingValue;
            }
        }
        body.style.paddingRight = lockPaddingValue;
        body.classList.add('lock');

        unlock = false;
        setTimeout(function (){
            unlock = true;
        }, timeout);
    }

function bodyUnlock(){
    setTimeout(function (){
        if (lockPadding.length > 0){
            for (let i=0; i<lockPadding.length; i++){
                const el = lockPadding[i];
                el.style.paddingRight='0px';
            }
        }
        body.style.paddingRight = '0px';
        body.classList.remove('lock');
    }, timeout);

    unlock = false;
    setTimeout(function (){
        unlock = true;
    }, timeout)
}

//блок для корректного отображения в ебаных браузерах
(function (){
    if (!Element.prototype.closest) {
        Element.prototype.closest = function (css) {
            var node = this;
            while (node) {
                if (node.matches(css)) return node;
                else node = node.parentElement;
            }
            return null;
        };
    }
})();
(function (){
    if (!Element.prototype.matches){
        Element.prototype.matches = Element.prototype.matchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector;
    }
})();