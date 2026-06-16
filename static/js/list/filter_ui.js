// 一覧画面で検索条件を変更したときのみリセットボタンを表示するJS

// q, status, state, sort, 将来追加のカラムにも全部自動対応

function initFilterUI() {

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

    let hasActiveFilter = false;

    for (const [key, value] of urlParams.entries()) {

        if (
            key !== 'page' &&
            value.trim() !== ''
        ) {
            hasActiveFilter = true;
            break;
        }
    }

    resetBtn.forEach(btn => {

        btn.style.display =
            hasActiveFilter
            ? 'inline-flex'
            : 'none';
    });
}

document.addEventListener(
    'DOMContentLoaded',
    initFilterUI
);