// 詳細画面共通削除処理

async function deleteFromDetail(button, redirectUrl) {

    const itemTitle = button.dataset.title;

    const url = button.dataset.url;

    await deleteItem({

        url: url,

        itemName: itemTitle,

        successCallback: () => {

            window.location.href = redirectUrl;
        }
    });
}