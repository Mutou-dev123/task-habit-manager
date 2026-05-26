// ==============================
// 汎用確認モーダル
// ==============================

async function showConfirmModal({
    title = "実行しますか？",
    targetName = "",
    confirmText = "実行",
    isDanger = false
}) {
    return new Promise((resolve) => {

        const modal = document.getElementById('custom-delete-modal');

        const titleEl = document.getElementById('modal-title');
        const targetEl = document.getElementById('modal-target-name');

        const confirmBtn = document.getElementById('confirm-delete-btn');
        const cancelBtn = document.getElementById('cancel-delete-btn');

        // タイトル・対象名・ボタン名を差し替え
        titleEl.textContent = title;
        targetEl.textContent = targetName || "対象項目";
        confirmBtn.textContent = confirmText;

        // 危険操作なら赤色
        if (isDanger) {
            confirmBtn.classList.add('danger');
        } else {
            confirmBtn.classList.remove('danger');
        }

        modal.showModal();

        const onConfirm = () => {
            cleanup();
            resolve(true);
        };

        const onCancel = () => {
            cleanup();
            resolve(false);
        };

        const cleanup = () => {
            modal.close();

            confirmBtn.removeEventListener('click', onConfirm);
            cancelBtn.removeEventListener('click', onCancel);
        };

        confirmBtn.addEventListener('click', onConfirm);
        cancelBtn.addEventListener('click', onCancel);
    });
}

// ==============================
// CSRF取得
// ==============================

function getCsrfToken() {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }

    return null;
}

// ==============================
// 汎用削除処理
// ==============================

async function deleteItem({
    url,
    itemName = "",
    successCallback = null
}) {

    const isConfirmed = await showConfirmModal({
        title: "削除しますか？",
        targetName: itemName,
        confirmText: "削除",
        isDanger: true
    });

    if (!isConfirmed) return false;

    try {

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (!response.ok) {
            alert("削除に失敗しました");
            return false;
        }

        // 成功時コールバック
        if (successCallback) {
            successCallback(response);
        }

        return true;

    } catch (error) {
        console.error(error);
        return false;
    }
}