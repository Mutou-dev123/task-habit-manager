// 日付詳細画面専用JS

document.addEventListener(
    'click',
    function(e) {

        const link =
            e.target.closest(
                '.day-nav-prev, .day-nav-next'
            );

        if (!link) return;

        e.preventDefault();

        const transitionType =
            link.classList.contains(
                'day-nav-next'
            )
            ? 'slide-next'
            : 'slide-prev';

        replaceContent({
            url: link.href,
            targetId: 'day-detail-content',
            transitionType
        });
    }
);