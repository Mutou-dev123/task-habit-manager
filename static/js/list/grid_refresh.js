// 進行状況ボタン押下時の状態更新

// カードグリッド再読み込み
async function refreshCardGrid() {

    const currentUrl = window.location.href;

    const pageResponse = await fetch(currentUrl);

    const pageHtml = await pageResponse.text();

    const parser = new DOMParser();

    const doc = parser.parseFromString(pageHtml, 'text/html');

    const newGrid = doc.querySelector('.card-grid');

    updateCardGrid(newGrid);
}

// カードグリッド更新
function updateCardGrid(newGrid) {

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

        return;
    }

    // カードあり
    if (emptyMessage) {
        emptyMessage.style.display = 'none';
    }

    if (trigger) {

        trigger.style.display =
            grid.CDATA_SECTION_NODE.hasNext === 'true'
            ? 'block'
            : 'none';
    }
}
