// 要素スライドアニメーションJS

async function replaceContent({
    url,
    targetId,
    transitionType = 'fade'
}) {
    
    try {

        const response = await fetch(
            url,
            {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }
        );

        const html = await response.text();

        const parser = new DOMParser();

        const doc = parser.parseFromString(
            html,
            'text/html'
        );

        const currentTarget =
            document.getElementById(targetId);

        const newTarget =
            doc.getElementById(targetId);

        if (!currentTarget || !newTarget) {
            window.location.href = url;
            return;
        }

        if (document.startViewTransition) {

            document.documentElement.setAttribute(
                'data-transition',
                transitionType
            );

            const transition =
                document.startViewTransition(() => {

                    currentTarget.innerHTML =
                        newTarget.innerHTML;

                    history.pushState(
                        {},
                        '',
                        url
                    );
                });

            transition.finished.finally(() => {

                document.documentElement.removeAttribute(
                    'data-transition'
                );

            });

        } else {

            currentTarget.innerHTML =
                newTarget.innerHTML;

            history.pushState(
                {},
                '',
                url
            );

        }

    } catch (error) {

        console.error(error);

        window.location.href = url;
    }
}