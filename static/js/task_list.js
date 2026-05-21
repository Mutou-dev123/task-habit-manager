// 進行状況ボタン押下時のスクロールリセット防止 & 並び替え
function toggleTaskStatus(button) {
    const url = button.dataset.url;
    const grid = document.querySelector('.card-grid');

    if (document.startViewTransition) {
        document.startViewTransition(async () => {
            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });

                if (response.ok) {
                    const currentUrl = window.location.href;
                    const pageResponse = await fetch(currentUrl);
                    const pageHtml = await pageResponse.text();

                    const parser = new DOMParser();
                    const doc = parser.parseFromString(pageHtml, 'text/html');
                    const newGrid = doc.querySelector('.card-grid');

                    updateCardGrid(newGrid, response);
                } else {
                    alert('ステータスの更新に失敗しました。');
                }
            } catch(error) {
                console.error('Error:', error);
            }
        });
    } else {
        fetch(url, { method: 'GET', headers: {'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => { if (res.ok) window.location.reload(); });
    }
}

// 自動無限スクロール（インフィニットスクロール）
const grid = document.querySelector('.card-grid');
const trigger = document.getElementById('infinite-scroll-trigger');

if (trigger && grid && grid.dataset.hasNext !== 'false') {
    let page = 1;
    let isLoading = false;

    const observer = new IntersectionObserver(async (entries) => {
        if (entries[0].isIntersecting && !isLoading && grid.dataset.hasNext === 'true') {
            isLoading = true;
            page++;

            const currentParams = new URLSearchParams(window.location.search);
            currentParams.set('page', page);

            try {
                const response = await fetch(`${window.location.pathname}?${currentParams.toString()}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });

                if (response.ok) {
                    const html = await response.text();
                    const hasNextHeader = response.headers.get('X-Has-Next');

                    if (document.startViewTransition) {
                        document.startViewTransition(() => {
                            grid.insertAdjacentHTML('beforeend', html);
                        });
                    } else {
                        grid.insertAdjacentHTML('beforeend', html);
                    }

                    // 次がない場合、終了
                    if (hasNextHeader === 'false' || html.trim() === "") {
                        grid.dataset.hasNext = 'false';

                        if (trigger) {
                            trigger.style,display = 'block';
                            trigger.style.color = '#9e9e9e';
                            trigger.textContent = "すべてのタスクを表示しました";
                        }
                        observer.unobserve(trigger);    // センサー停止
                    }
                }
            } catch (error) {
                console.error('Error fetching next page:', error);
            } finally {
                isLoading = false;
            }
        }
    }, { rootMargin: '200px' });

    observer.observe(trigger);
}

// 検索条件を保持しながら、その場でタスクを消滅させる削除機能
async function deleteTask(button) {
    if (!confirm("このタスクを本当に削除しますか？")) {
        return;
    }

    const url = button.dataset.url;
    const grid = document.querySelector('.card-grid');

    let csrfToken = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            csrfToken = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        });

        if (response.ok) {
            if (document.startViewTransition) {
                document.startViewTransition(async () => {
                    const currentUrl = window.location.href;
                    const pageResponse = await fetch(currentUrl);
                    const pageHtml = await pageResponse.text();

                    const parser = new DOMParser();
                    const doc = parser.parseFromString(pageHtml, 'text/html');
                    const newGrid = doc.querySelector('.card-grid');

                    updateCardGrid(newGrid, response);
                });
            } else {
                window.location.reload();
            }
        } else {
            const errorText = await response.text();
            alert("削除に失敗しました。ステータス: " + response.status);
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// カードグリッドの更新と件数チェック（エンプティ状態の制御）
function updateCardGrid(newGrid, response) {
    const grid = document.querySelector('.card-grid');
    if (!newGrid || !grid) return;

    grid.innerHTML = newGrid.innerHTML;

    const cardCount = newGrid.querySelectorAll('.card').length;
    const emptyMessage = document.getElementById('empty-message');
    const trigger = document.getElementById('infinite-scroll-trigger');

    if (cardCount === 0) {
        if (emptyMessage) emptyMessage.style.display = 'block';
        if (trigger) trigger.style.display = 'none';
        grid.dataset.hasNext = 'false';
    } else {
        if (emptyMessage) emptyMessage.style.display = 'none';
        
        const hasNextHeader = response.headers.get('X-Has-Next');
        if (trigger) {
            trigger.style.display = (hasNextHeader === 'true') ? 'block' : 'none';
        }
    }
}

// 条件変更時のみリセットボタンを表示する
(function() {
    // 🌟 現在のアドレスバーのURLを完全にクリーンに取得する
    const currentSearch = window.location.search;

    // querySelectorAllを使って、クラス名で複数のボタンを一気に捕まえる
    const resetBtn = document.querySelectorAll('.search-reset-btn');

    // 🌟 1. そもそもURLに「?」が一切ない、または「?」だけなら絶対に非表示にして即終了
    if (!currentSearch || currentSearch === '?') {
        resetBtn.forEach(btn => btn.style.display = 'none');
        return;
    }

    const urlParams = new URLSearchParams(currentSearch);
    const qValue = urlParams.get('q');
    const statusValue = urlParams.get('status');
    const sortValue = urlParams.get('sort');

    // 🌟 2. 各パラメータが「本当に文字として中身が入っているか」を厳密にチェック
    const hasActiveFilter = (qValue !== null && qValue.trim() !== '') ||
                            (statusValue !== null && statusValue.trim() !== '') ||
                            (sortValue !== null && sortValue.trim() !== '');

    // 捕まえたボタン全部に同じ命令を出す
    resetBtn.forEach(btn => {
        if (hasActiveFilter) {
            btn.style.display = 'inline-flex';   // 条件があれば表示
        } else {
            btn.style.display = 'none';         // なければ非表示
        }
    });
})();