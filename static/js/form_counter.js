// static/js/form_counter.js

document.addEventListener('DOMContentLoaded', function() {
    // Djangoが自動で付与するID「id_description」を探す
    const memoField = document.getElementById('id_description');
    
    if (memoField) {
        // 1. カウンター用のdiv要素を新しく作る
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        
        // 2. 最大文字数を設定（例として500文字）
        const maxLength = 500; 
        
        // 3. 初期状態の文字数を表示
        counter.textContent = `${memoField.value.length} / ${maxLength} 文字`;
        
        // 4. メモ入力欄のすぐ後ろにカウンターを挿入
        memoField.parentNode.appendChild(counter);

        // 5. 文字が入力されるたびに数字を更新する
        memoField.addEventListener('input', function() {
            const currentLength = this.value.length;
            counter.textContent = `${currentLength} / ${maxLength} 文字`;
            
            // 最大文字数を超えたら文字を赤くする
            if (currentLength > maxLength) {
                counter.classList.add('is-over');
            } else {
                counter.classList.remove('is-over');
            }
        });
    }
});