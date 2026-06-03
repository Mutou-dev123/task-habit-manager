// 詳細画面共通削除処理

async function deleteFromDetail(button) {

    await deleteItem({

        url: button.dataset.url,

        itemName: button.dataset.title,

        successCallback: () => {

            window.location.href = button.dataset.redirect;
        }
    });
}


// 削除ボタンイベント登録

document.querySelectorAll('.js-detail-delete').forEach(button => {

    button.addEventListener('click', async () => {

        await deleteFromDetail(button);
    });
});