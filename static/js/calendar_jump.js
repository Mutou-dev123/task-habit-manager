// カレンダー画面専用JS

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. 年月タイトルのクリック処理
    document.body.addEventListener('click', function(e) {
        const titleTrigger = e.target.closest('#calendar-header-trigger');
        if (titleTrigger) {
            const monthPicker = document.getElementById('month-picker');
            if (monthPicker) {
                if (typeof monthPicker.showPicker === 'function') {
                    monthPicker.showPicker();
                } else {
                    monthPicker.click();
                }
            }
        }
    });

    // 2. 年月カレンダーで月を選んだ時の処理（ふわっと着地）
    document.body.addEventListener('change', function(e) {
        if (e.target.id === 'month-picker') {
            const dateVal = e.target.value;
            if (dateVal) {
                const [year, month] = dateVal.split('-');
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('year', year);
                urlParams.set('month', parseInt(month, 10));
                
                // 🌟 アニメーションタイプを 'fade' に指定
                fetchAndReplace(window.location.pathname + '?' + urlParams.toString(), 'fade');
            }
        }
    });

    // 3. リンクを押した時の処理（ボタンごとに動きを変える！）
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('.btn-nav, .btn-today, .filter-item');
        if (link) {
            e.preventDefault(); 
            
            // 🌟 押されたボタンのテキストから、どのアニメーションにするか判定する
            let animType = 'fade'; // デフォルトはふわっと着地
            const btnText = link.textContent.trim();
            
            if (btnText.includes('前の月')) {
                animType = 'slide-prev';
            } else if (btnText.includes('次の月')) {
                animType = 'slide-next';
            }
            
            fetchAndReplace(link.href, animType);
        }
    });

    // 4. 魔法の関数（アニメーションの種別を受け取るように進化！）
    async function fetchAndReplace(url, transitionType = 'fade') {
        try {
            const response = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            const html = await response.text();
            
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const newContent = doc.getElementById('calendar-main-area');
            const currentContent = document.getElementById('calendar-main-area');

            if (newContent && currentContent) {
                if (document.startViewTransition) {
                    
                    // 🌟 CSSに「この動きをして！」と指示を出す
                    document.documentElement.setAttribute('data-transition', transitionType);
                    
                    const transition = document.startViewTransition(() => {
                        currentContent.innerHTML = newContent.innerHTML;
                        window.history.pushState({}, '', url);
                    });
                    
                    // 🌟 アニメーションが終わったら指示を消去する
                    transition.finished.finally(() => {
                        document.documentElement.removeAttribute('data-transition');
                    });
                    
                } else {
                    currentContent.innerHTML = newContent.innerHTML;
                    window.history.pushState({}, '', url);
                }
            } else {
                window.location.href = url;
            }
        } catch (error) {
            console.error('Error fetching calendar data:', error);
            window.location.href = url;
        }
    }
});