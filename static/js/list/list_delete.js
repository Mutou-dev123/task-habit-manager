// 一覧画面共通削除処理

async function deleteFromList(button, modalTitle = "削除しますか？") {

    const card = button.closest('.card');

    await deleteItem({

        url: button.dataset.url,

        itemName: button.dataset.title,

        modalTitle: modalTitle,

        successCallback: () => {

            if (!card) return;

            if (document.startViewTransition) {

                document.startViewTransition(() => {

                    card.remove();

                    updateEmptyState();
                });

            } else {

                card.remove();

                updateEmptyState();
            }
        }
    });
}