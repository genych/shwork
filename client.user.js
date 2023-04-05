// ==UserScript==
// @name         workshop downloader
// @namespace    gnch
// @version      0.1
// @description  weird way to download workshop items in bulk
// @author       genych
// @match        https://steamcommunity.com/workshop/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=steamcommunity.com
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';
    let header = document.getElementsByClassName('subscribeCollection')[0];
    let collection = Array.from(document.getElementsByClassName('collectionItemDetails'));
    let func = x => x.getElementsByTagName('a')[0].attributes.href.nodeValue.replace(/^.*id=/,'');
    let ids = collection.map(func);

    let button = document.createElement('button');
    header.append(button);

    button.innerHTML = 'скачать все';
    button.onclick = () => {
        GM_xmlhttpRequest({
            method: "POST",
            url: "http://localhost:5000",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify(ids),
            onload: function(response) {
                console.log(response.responseText);
            }
        });

        button.disabled = true;
    }

})();
