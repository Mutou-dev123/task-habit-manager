// タスク一覧画面専用JS

// ステータス更新
function toggleTaskStatus(button) {

    const url = button.dataset.url;

    if (document.startViewTransition) {

        document.startViewTransition(async () => {

            try {

                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {

                    await refreshCardGrid();
                
                } else {

                    alert('ステータスの更新に失敗しました。');
                }

            } catch (error) {

                console.error('Error', error);
            }
        });

    } else {

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => {

            if (res.ok) {
                window.location.reload();
            }
        });
    }
}