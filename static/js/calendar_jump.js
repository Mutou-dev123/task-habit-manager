// カレンダー画面専用JS

document.addEventListener('DOMContentLoaded', function() {
    
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

    document.body.addEventListener('change', function(e) {
        if (e.target.id === 'month-picker') {
            const dateVal = e.target.value;
            if (dateVal) {
                const [year, month] = dateVal.split('-');
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('year', year);
                urlParams.set('month', parseInt(month, 10));
                
                // アニメーションタイプを 'fade' に指定
                fetchAndReplace(window.location.pathname + '?' + urlParams.toString(), 'fade');
            }
        }
    });

    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('.btn-nav, .btn-today, .filter-item');
        if (link) {
            e.preventDefault(); 
            
            let animType = 'fade'; // デフォルトはふわっと着地
            
            // 修正ポイント：テキストではなく「中のアイコン」で前月・翌月を判定する
            if (link.querySelector('.fa-chevron-left')) {
                animType = 'slide-prev'; // 左向きアイコンなら左スライド
            } else if (link.querySelector('.fa-chevron-right')) {
                animType = 'slide-next'; // 右向きアイコンなら右スライド
            }
            
            fetchAndReplace(link.href, animType);
        }
    });

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
                    
                    // CSSに「この動きをして！」と指示を出す
                    document.documentElement.setAttribute('data-transition', transitionType);
                    
                    const transition = document.startViewTransition(() => {
                        currentContent.innerHTML = newContent.innerHTML;
                        window.history.pushState({}, '', url);
                    });
                    
                    // アニメーションが終わったら指示を消去する
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