CREATE TABLE `users` (
  `id` int(11) NOT NULL COMMENT 'id пользователя',
  `login` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'логин пользователя',
  `hash` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'хэш-пароль пользователя',
)

