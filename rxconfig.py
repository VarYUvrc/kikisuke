import reflex as rx

config = rx.Config(
    app_name="kikisuke",
    loglevel=rx.constants.LogLevel.DEBUG,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)