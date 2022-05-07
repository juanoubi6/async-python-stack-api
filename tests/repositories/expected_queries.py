GET_USER_EXPECTED_QUERY = '''SELECT users.id, users.first_name, users.last_name, users.birth_date, users.created, users.updated, users.deleted 
FROM users 
WHERE users.id = :id_1'''

CREATE_USER_EXPECTED_QUERY = '''INSERT INTO users (first_name, last_name, birth_date) VALUES (:first_name, :last_name, :birth_date)'''