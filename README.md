Запуск воркера

```shell
cd src
taskiq worker core.broker:broker -w 1 --no-configure-logging --fs-discover --tasks-pattern "**/tasks"
```