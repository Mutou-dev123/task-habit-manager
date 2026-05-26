// タスク一覧画面専用JavaScript

// =====================================
// 進行状況ボタン押下時の状態更新
// =====================================

async function refreshCardGrid(response) {

    const currentUrl = window.location.href;

    const pageResponse = await fetch(currentUrl);

    const pageHtml = await pageResponse.text();

    const parser = new DOMParser();

    const doc = parser.parseFromString(pageHtml, 'text/html');

    const newGrid = doc.querySelector('.card-grid');

    updateCardGrid(newGrid, response);
}

// 進行状況ボタン押下時のスクロールリセット防止 & 並び替え
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

                    await refreshCardGrid(response);

                } else {

                    alert('ステータスの更新に失敗しました。');
                }

            } catch(error) {

                console.error('Error:', error);
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

// =====================================
// 自動無限スクロール
// =====================================

const grid = document.querySelector('.card-grid');
const trigger = document.getElementById('infinite-scroll-trigger');

if (trigger && grid && grid.dataset.hasNext !== 'false') {

    let page = 1;
    let isLoading = false;

    const observer = new IntersectionObserver(async (entries) => {

        if (
            entries[0].isIntersecting &&
            !isLoading &&
            grid.dataset.hasNext === 'true'
        ) {

            isLoading = true;

            page++;

            const currentParams = new URLSearchParams(window.location.search);

            currentParams.set('page', page);

            try {

                const response = await fetch(
                    `${window.location.pathname}?${currentParams.toString()}`,
                    {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }
                );

                if (response.ok) {

                    const html = await response.text();

                    const hasNextHeader = response.headers.get('X-Has-Next');

                    grid.insertAdjacentHTML('beforeend', html);

                    // 次ページなし
                    if (hasNextHeader === 'false' || html.trim() === "") {

                        grid.dataset.hasNext = 'false';

                        if (trigger) {

                            trigger.style.display = 'block';
                            trigger.style.color = '#9e9e9e';

                            trigger.textContent =
                                "すべてのタスクを表示しました";
                        }

                        observer.unobserve(trigger);
                    }
                }

            } catch (error) {

                console.error('Error fetching next page:', error);

            } finally {

                isLoading = false;
            }

        }

    }, {
        rootMargin: '800px'
    });

    observer.observe(trigger);
}

// =====================================
// タスク削除
// =====================================

async function deleteTask(button) {

    const taskTitle = button.dataset.title;

    const isConfirmed = await showConfirmModal({
        title: "削除しますか？",
        targetName: taskTitle,
        confirmText: "削除",
        isDanger: true
    });

    // キャンセル時終了
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

                    await refreshCardGrid(response);

                });

            } else {

                window.location.reload();
            }

        } else {

            alert("削除に失敗しました。ステータス: " + response.status);
        }

    } catch (error) {

        console.error('Error deleting task:', error);
    }
}

// =====================================
// カードグリッド更新
// =====================================

function updateCardGrid(newGrid, response) {

    const grid = document.querySelector('.card-grid');

    if (!newGrid || !grid) return;

    grid.innerHTML = newGrid.innerHTML;

    const cardCount = newGrid.querySelectorAll('.card').length;

    const emptyMessage = document.getElementById('empty-message');

    const trigger = document.getElementById('infinite-scroll-trigger');

    // 0件時
    if (cardCount === 0) {

        if (emptyMessage) {
            emptyMessage.style.display = 'block';
        }

        if (trigger) {
            trigger.style.display = 'none';
        }

        grid.dataset.hasNext = 'false';

    } else {

        if (emptyMessage) {
            emptyMessage.style.display = 'none';
        }

        const hasNextHeader = response.headers.get('X-Has-Next');

        if (trigger) {

            trigger.style.display =
                (hasNextHeader === 'true')
                ? 'block'
                : 'none';
        }
    }
}

// =====================================
// 条件変更時のみリセットボタン表示
// =====================================

(function() {

    // 現在URLの検索条件
    const currentSearch = window.location.search;

    // リセットボタン群
    const resetBtn = document.querySelectorAll('.search-reset-btn');

    // パラメータなし
    if (!currentSearch || currentSearch === '?') {

        resetBtn.forEach(btn => {
            btn.style.display = 'none';
        });

        return;
    }

    const urlParams = new URLSearchParams(currentSearch);

    const qValue = urlParams.get('q');

    const statusValue = urlParams.get('status');

    const sortValue = urlParams.get('sort');

    // 有効条件判定
    const hasActiveFilter =

        (qValue !== null && qValue.trim() !== '') ||

        (statusValue !== null && statusValue.trim() !== '') ||

        (sortValue !== null && sortValue.trim() !== '');

    // ボタン表示切替
    resetBtn.forEach(btn => {

        btn.style.display =
            hasActiveFilter
            ? 'inline-flex'
            : 'none';
    });

})();