#передать в ссылке id пользователя, timestamp валидности ссылки, хэш(id_user, timespamp+salt)
#проверка id_user, timestamp>= current_date, хэш(id_user, timestamp+salt)