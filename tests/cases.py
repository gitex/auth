INVALID_EMAILS = [
    ('plainaddress', 'missing @'),
    ('@example.com', 'missing local part'),
    ('john.doe@', 'missing domain'),
    ('john..doe@example.com', 'double dot in local'),
    ('.john@example.com', 'local starts with dot'),
    ('john.@example.com', 'local ends with dot'),
    ('jo hn@example.com', 'space in local'),
    ('john,doe@example.com', 'comma in local'),
    ('john@exa mple.com', 'space in domain'),
    ('john@-example.com', "label starts with '-'"),
    ('john@example-.com', "label ends with '-'"),
    ('john@example..com', 'double dot in domain'),
    ('john@example', 'no public TLD'),
    ('john@123', 'numeric host, no TLD'),
]


INVALID_PASSWORDS = [
    ('a', 'too short'),
    # TODO: добавить примеры после Password Policy
]
