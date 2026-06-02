// 習慣一覧画面専用JS

// 習慣更新
async function updateHabit(button) {
    
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

                    alert('更新に失敗しました。');
                }

            } catch (error) {

                console.error('Error', error);
            }
        });

    } else {

        try {

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {

                window.location.reload();
            }

        } catch (error) {

            console.error('Error:', error);
        }
    }
}