CREATE TABLE `users` (
    `id` int(11) NOT NULL COMMENT 'id пользователя',
    `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'логин пользователя',
    `hash` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'хэш-пароль пользователя'
)

CREATE TABLE `chats` (
    `chat_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `f_user_id` int(11) NOT NULL,
    `s_user_id` int(11) NOT NULL
)

CREATE TABLE `messages` (
    `chat_id` int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `text` text
)
