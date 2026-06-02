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

// タスク削除
async function deleteTask(button) {
    
    const taskTitle = button.dataset.title;

    const isConfirmed = await showConfirmModal({
        title: "削除しますか？",
        targetName: taskTitle,
        confirmText: "削除",
        isDanger: true
    });

    if (!isConfirmed) return;

    const url = button.dataset.url;

    try {

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (response.ok) {

            if (document.startViewTransition) {

                document.startViewTransition(async () => {

                    await refreshCardGrid();

                });

            } else {

                window.location.reload();
            }

        } else {

            alert(
                "削除に失敗しました。ステータス: "
                + response.status
            );
        }

    } catch (error) {

        console.error(
            'Error deleting task:',
            error
        );
    }
}