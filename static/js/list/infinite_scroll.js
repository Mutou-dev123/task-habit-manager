// 自動無限スクロール

function initInfiniteScroll(){

    const grid = document.querySelector('.card-grid');
    const trigger = document.getElementById('infinite-scroll-trigger');

    if (!trigger || !grid || grid.dataset.hasNext !== 'true') {
        return;
    }

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

            const currentParams = new URLSearchParams(
                window.location.search
            );

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

                    const hasNextHeader =
                        response.headers.get('X-Has-Next');

                    grid.insertAdjacentHTML(
                        'beforeend',
                        html
                    );

                    // 次ページなし
                    if (
                        hasNextHeader === 'false' ||
                        html.trim() === ''
                    ) {

                        grid.dataset.hasNext = 'false';

                        trigger.style.display = 'block';
                        trigger.style.color = '#9e9e9e';

                        trigger.textContent =
                            'すべて表示しました';

                        observer.unobserve(trigger);
                    }
                }
            } catch (error) {

                console.error(
                    'Error fetching next page',
                    error
                );

            } finally {

                isLoading = false;
            }
        }
    }, {
        rootMargin: '800px'
    });

    observer.observe(trigger);
}

document.addEventListener(
    'DOMContentLoaded',
    initInfiniteScroll
);