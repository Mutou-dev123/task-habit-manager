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

    const grid =
        document.querySelector('.card-grid');

    if (!newGrid || !grid) return;

    grid.innerHTML = newGrid.innerHTML;

    grid.dataset.hasNext =
        newGrid.dataset.hasNext;

    updateEmptyState();

    const trigger =
        document.getElementById(
            'infinite-scroll-trigger'
        );

    if (trigger) {

        trigger.style.display =
            grid.dataset.hasNext === 'true'
            ? 'block'
            : 'none';
    }

}

// 空状態更新
function updateEmptyState() {
    
    const cards =
        document.querySelectorAll('.card');

    const emptyMessage =
        document.getElementById('empty-message');

    const trigger =
        document.getElementById(
            'infinite-scroll-trigger'
        );

    if (cards.length === 0) {

        if (emptyMessage) {

            emptyMessage.style.display = 'block';
        }

        if (trigger) {

            trigger.style.display = 'none';
        }

    } else {

        if (emptyMessage) {

            emptyMessage.style.display = 'none';
        }
    }
}