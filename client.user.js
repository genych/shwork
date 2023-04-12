// ==UserScript==
// @name         workshop downloader
// @namespace    gnch
// @version      0.2
// @description  weird way to download specific workshop items in bulk
// @author       genych
// @match        https://steamcommunity.com/*/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=steamcommunity.com
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';
    const get_anch = x => x.querySelector('a.item_link') || x.getElementsByTagName('a')[0];
    const get_id = x => x.attributes.href.nodeValue.match(/\?id=(\d*).*/)[1];

    let header = document.querySelectorAll(':is(.workshopItemDescriptionTitle, .game_area_purchase_margin)');
    header = header.item(header.length - 1);
    let collection = document.querySelectorAll(':is(.collectionItemDetails, .workshopItem)');

    let items = [];
    for (let c of collection) {
        let a = get_anch(c);
        let name = a.innerText;
        let id = get_id(a);
        let pair = {id, name};
        items.push(pair);

        let button = document.createElement('button');
        c.append(button);
        button.innerHTML = 'скачать этот';
        button.onclick = () => {
            console.log(pair);
            GM_xmlhttpRequest({
                method: "POST",
                url: "http://localhost:5000",
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify([pair]),
                onload: function(response) {
                    console.log(response.responseText);
                }
            });
            button.disabled = true;
        };
    }

    let button = document.createElement('button');
    if (!header) {
        console.log('not a collection?');
        return;
    }
    if (items.length === 0) {
        let name = document.querySelector('.workshopItemTitle').innerText;
        let id = window.location.search.match(/\?id=(\d*).*/)[1];
        items.push({id, name});
    }
    header.append(button);
    button.innerHTML = 'скачать';
    button.onclick = () => {
        console.log(items);
        GM_xmlhttpRequest({
            method: "POST",
            url: "http://localhost:5000",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify(items),
            onload: function(response) {
                console.log(response.responseText);
            }
        });
        button.disabled = true;
    };
})();
