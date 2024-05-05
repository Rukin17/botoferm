"""
    Решение профильного задания на стажировку в VK

    Ботоферма для E2E - теста.
"""

написать restful-сервис на python с fastapi, sqlalchemy.
реализовать методы create_user, get_users, acquire_lock(устанавлитвает locktime со значением timestamp) и release_lock(ставит в locktime None).
Сущности:
User:
-id-UUID пользователя;
-created_ad -дата создания пользователя;
-login- почтовый адрес пользователя;
-password-пароль;
-project_id -UUID некоторого проекта;
-env - название окружения(prod, preprodm stage);
-domain - тип пользователя(canary, regular);
-locktime - временная метка(timestamp)




