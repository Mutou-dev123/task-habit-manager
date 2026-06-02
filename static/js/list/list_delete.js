// 一覧画面共通削除処理

async function deleteFromList(button) {

    const card = button.closest('card');
    
    await deleteItem({

        url: button.dataset.url,

        itemName: button.dataset.title,

        successCallback: () => {

            if (!card) return;

            if (document.startViewTransition) {

                document.startViewTransition(() => {

                    acard.remove();

                    updateEmptyState();
                });
            
            } else {

                card.remove();
                
                updateEmptyState();
            }
        }
    });
}