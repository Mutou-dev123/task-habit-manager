// フォーム入力欄文字数カウンター

document.addEventListener('DOMContentLoaded', function() {

    // カウンターを設置したい入力欄のIDを配列に指定
    const targetFields = ['id_title', 'id_description'];
    
    targetFields.forEach(id => {
        const field = document.getElementById(id);

        // 入力欄が存在し、かつHTML側に「maxlength」が設定されている場合だけ処理する
        if (field && field.hasAttribute('maxlength')) {
            const maxlength = field.getAttribute('maxlength');

            const counter = document.createElement('div');
            counter.className = 'char-counter';

            // 🌟 修正1： field.value.length に変更
            // 初期状態の文字数を表示
            counter.textContent = `${field.value.length} / ${maxlength} 文字`;

            // 入力欄のすぐ後ろ（下）にカウンター挿入
            field.parentNode.appendChild(counter);

            // 文字が入力されるたびに数字をリアルタイム更新
            field.addEventListener('input', function() {
                const currentLength = this.value.length;
                
                // 🌟 修正2＆3： バッククォート（`）に変更し、maxlength を小文字の l に統一
                counter.textContent = `${currentLength} / ${maxlength} 文字`;

                // 上限に達したら警告色（赤）にする
                if (currentLength >= maxlength) {
                    counter.classList.add('is-over');
                } else {
                    counter.classList.remove('is-over');
                }
            });
        }
    });
});